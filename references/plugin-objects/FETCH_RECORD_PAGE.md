# FETCH_RECORD_PAGE

A **table function (UDTF)** that a plugin implements to support inbound syncs using the
`rest_api_pagination` sync style. The Omnata sync engine calls it repeatedly, one call per page,
until a call returns no records. Each call fetches a single page of records from the external
system and yields them along with the updated stream state.

It lives in the plugin's schema (for interactive plugins:
`OMNATA_PLUGIN_DEVELOPMENT.<PLUGIN_ID>.FETCH_RECORD_PAGE`) and is generated with the
`@inbound_sync_rest_paginated_handler` decorator from `omnata_plugin_runtime.decorators`, applied
to a handler class named `FetchRecordPage`.

## Signature

```sql
FETCH_RECORD_PAGE(
    connection_parameters object,
    stream_name varchar,
    cursor_field_name varchar,
    stream_state object,
    current_run_variables object,
    page_size integer,
    sync_run_start_time timestamp_ltz
)
RETURNS TABLE (
    record object,
    new_state object,
    run_variables object
)
```

## Parameters

| Argument | Type | Description |
|---|---|---|
| `parameters` | object | A connection-configuration object built by the caller. It carries `operation` (always `'inbound_sync_rest_paginated'`), `connectivity_option`, `connection_method`, `connection_parameters`, and the secret names `oauth_secret` / `other_secrets`. The `@inbound_sync_rest_paginated_handler` decorator resolves the secrets and converts this into an `InboundSyncConfigurationParameters` instance before your `process()` runs. |
| `stream_name` | varchar | The stream (object) being fetched, e.g. `companies`. |
| `cursor_field_name` | varchar | The cursor field for incremental syncs, or an empty string for full refresh / when the stream has no cursor. |
| `stream_state` | object | The persisted state for this stream (the `new_state` your plugin last returned). Empty (`{}`) on the first run or a full refresh. Use it to resume from the last cursor position. |
| `current_run_variables` | object | Transient, per-run pagination variables (e.g. an offset or next-page token). Empty (`{}`) on the first page of a run; thereafter it is the `run_variables` your plugin returned for the previous page. Not persisted across runs. |
| `page_size` | integer | The number of records to request per page. Sourced from the plugin's `PLUGIN_BUILDER_SETTINGS.paginated_rest_page_size` (default `1000`). |
| `sync_run_start_time` | timestamp_ltz | **The time the sync run started.** Use it as a stable upper bound so pagination terminates deterministically: stop emitting records once you reach data at or after this point. This argument was added so that incremental, time-ordered sources don't chase a moving tail. |

## Return columns

Yield one row per record. All three columns are objects:

| Column | Description |
|---|---|
| `record` | The data record, as an object. |
| `new_state` | The updated cursor/checkpoint state to persist for the stream. Return the same value on every row of a page (the engine takes the last non-null value). Return `None` to leave the existing state unchanged. |
| `run_variables` | Updated transient pagination variables to feed into the next page's `current_run_variables` (e.g. an incremented offset or a next-page token). Not persisted as stream state. |

## Pagination and termination

The engine drives pagination by calling `FETCH_RECORD_PAGE` in a loop, feeding the `new_state`
and `run_variables` from each page into the next call's `stream_state` and
`current_run_variables`. **It stops when a call returns zero record rows.** Your plugin must
therefore yield no records once the stream is exhausted — for example, once the external API
returns an empty page, or once you have paged past `sync_run_start_time`.

## How `process()` receives the arguments

The `@inbound_sync_rest_paginated_handler` decorator passes the resolved
`InboundSyncConfigurationParameters` as the first argument, then forwards the remaining UDTF
arguments positionally. `sync_run_start_time` is the trailing argument:

```python
from typing import Iterable, Tuple
from omnata_plugin_runtime.configuration import InboundSyncConfigurationParameters
from omnata_plugin_runtime.decorators import inbound_sync_rest_paginated_handler

@inbound_sync_rest_paginated_handler
class FetchRecordPage:
    def process(
        self,
        connection_parameters: InboundSyncConfigurationParameters,
        stream_name: str,
        cursor_field_name: str,
        stream_state: dict,
        current_run_variables: dict,
        page_size: int,
        sync_run_start_time,        # the sync run's start time (TIMESTAMP_LTZ)
    ) -> Iterable[Tuple[dict, dict, dict]]:
        api_domain = connection_parameters.get_connection_parameter('api_domain').value
        token = connection_parameters.get_connection_secret('api_key').value
        offset = current_run_variables.get('offset', 0)

        response = requests.get(
            url=f"https://{api_domain}/objects/{stream_name}",
            params={'limit': page_size, 'offset': offset},
            headers={'Authorization': f'Bearer {token}'},
        )
        response.raise_for_status()
        results = response.json()['records']

        # Stop once we've paged past the run start time (deterministic termination)
        results = [r for r in results if r['updated_at'] < sync_run_start_time]
        if not results:
            return  # yield nothing -> the engine stops paging this stream

        new_state = {'last_updated': max(r['updated_at'] for r in results)}
        run_variables = {'offset': offset + page_size}
        for record in results:
            yield (record, new_state, run_variables)
```

## How it's invoked

- **Sync preview (UI):** the development console calls `FETCH_RECORD_PAGE` one page at a time so
  you can inspect records, the returned `new_state`, and `run_variables` while building the
  plugin. `sync_run_start_time` is passed as the current timestamp during preview.
- **Real sync run:** the sync engine's interactive inbound processor pages `FETCH_RECORD_PAGE`
  until an empty page is returned, stages each page's records into the run's results table, and
  checkpoints `new_state` after every page. `sync_run_start_time` is the timestamp the sync run
  began.
