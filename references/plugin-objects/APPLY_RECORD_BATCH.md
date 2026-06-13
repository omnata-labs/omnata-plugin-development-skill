# APPLY_RECORD_BATCH

A **table function (UDTF)** that a plugin implements to support outbound syncs using the
`batched_rest` ("Batched REST") sync style. The Omnata sync engine feeds the records that need to
be applied to the destination through this UDTF; the UDTF **accumulates** them in `process()` and
performs the actual upload in `end_partition()`, yielding one result row per record (success flag,
external identifier, result object).

This mirrors the traditional plugin `apply()` / `enqueue_results` pattern, but the engine drives
the UDTF directly (`OVER (PARTITION BY 1)`) instead of a `SYNC` procedure coordinating the run.

It lives in the plugin's schema (for interactive plugins:
`OMNATA_PLUGIN_DEVELOPMENT.<PLUGIN_ID>.APPLY_RECORD_BATCH`) and is generated with the
`@outbound_sync_batched_handler` decorator from `omnata_plugin_runtime.decorators`, applied to a
handler class named `ApplyRecordBatch`.

## Signature

```sql
APPLY_RECORD_BATCH(
    connection_parameters object,
    identifier varchar,
    sync_action varchar,
    transformed_record object
)
RETURNS TABLE (
    identifier varchar,
    app_identifier varchar,
    result object,
    success boolean
)
```

## Parameters

| Argument | Type | Description |
|---|---|---|
| `parameters` | object | A connection-configuration object built by the engine. It carries `operation` (always `'outbound_sync_batched'`), `connectivity_option`, `connection_method`, `connection_parameters`, the secret names `oauth_secret` / `other_secrets`, and `sync_parameters`. The `@outbound_sync_batched_handler` decorator resolves the secrets and converts this into an `OutboundSyncConfigurationParameters` instance before your `process()` runs (same constant value on every row of the batch). |
| `identifier` | varchar | The Snowflake-side primary key of the source record. Echo it back unchanged in the result so the engine can match the outcome to the source record. |
| `sync_action` | varchar | What to do with this record, derived from the sync strategy: `Create`, `Update`, `Delete`, `Send`, or `Recreate`. |
| `transformed_record` | object | The record to send to the destination, after field mapping. For `Delete` it may contain only the identifying fields. |

## Return columns

Yield one row per input record (from `end_partition`):

| Column | Description |
|---|---|
| `identifier` | The same `identifier` that was passed in — used to map the result back to the source record. |
| `app_identifier` | The destination system's ID for the record (e.g. the ID returned by a create). May be `NULL`. |
| `result` | A free-form object with diagnostic detail about the apply (echoed into the record's last result). |
| `success` | `TRUE` -> the engine records `APPLY_STATE = 'SUCCESS'`; `FALSE` -> `'DESTINATION_FAILURE'`. |

## The mandatory "object" sync parameter

Outbound is not tied to a first-class "target object" concept in the sync engine, so this pattern
**requires the plugin's outbound sync parameters to include a field named `object`** that
identifies which destination object the records are being synced to (e.g. `contacts`, `companies`).
Your `process()` / `end_partition()` reads it from the resolved parameters:

```python
target_object = parameters.get_sync_parameter('object').value
```

The development wizard always presents this field, and the **field mapper** relies on it to know
which target fields are available. Always declare and use it.

## How `process()` / `end_partition()` work

The `@outbound_sync_batched_handler` decorator passes the resolved
`OutboundSyncConfigurationParameters` as the first argument to `process()`. `process()` should
accumulate records and yield nothing; the upload and per-record results happen in `end_partition()`
(Snowflake's per-partition finalize hook), which the engine triggers once per batch (it calls the
UDTF `OVER (PARTITION BY 1)`).

```python
from typing import Any, Dict, Iterable, List, Tuple
from omnata_plugin_runtime.configuration import OutboundSyncConfigurationParameters
from omnata_plugin_runtime.decorators import outbound_sync_batched_handler

@outbound_sync_batched_handler
class ApplyRecordBatch:
    def __init__(self):
        self._parameters = None
        self._records: List[Tuple[str, str, dict]] = []

    def process(
        self,
        parameters: OutboundSyncConfigurationParameters,
        identifier: str,
        sync_action: str,
        transformed_record: dict,
    ):
        # Accumulate; yield nothing here.
        self._parameters = parameters
        self._records.append((identifier, sync_action, transformed_record))

    def end_partition(self) -> Iterable[Tuple[str, str, dict, bool]]:
        target_object = self._parameters.get_sync_parameter('object').value
        api_domain = self._parameters.get_connection_parameter('api_domain').value
        token = self._parameters.get_connection_secret('api_key').value

        # Group by action and call the destination's batch endpoints, then map results back by id.
        creates = [(i, r) for (i, a, r) in self._records if a == 'Create']
        # response = requests.post(
        #     url=f"https://{api_domain}/objects/{target_object}/batch",
        #     json={'records': [r for (_i, r) in creates]},
        #     headers={'Authorization': f'Bearer {token}'},
        # )
        # response.raise_for_status()
        # ... build {identifier: (app_identifier, result, success)} from the response ...

        for identifier, sync_action, record in self._records:
            app_identifier = f"app_{identifier}"      # the destination id
            yield (identifier, app_identifier, {"action": sync_action}, True)
```

`sync_action` lets a single implementation honour the chosen `OutboundSyncStrategy` (Create / Upsert
/ Update / Delete / Mirror / Send / Replace): branch on it in `end_partition` to call the
appropriate create / update / delete endpoint.

## How it's invoked

- **Sync preview (UI):** the development console runs the UDTF over a small sample of records you
  build in a grid, applying them in batches of the configured batch size and showing the per-record
  `success` / `app_identifier` / apply state so you can exercise the create -> update -> delete
  lifecycle.
- **Real sync run:** the engine stages the source records (with their `SYNC_ACTION` and
  `TRANSFORMED_RECORD`), then runs `APPLY_RECORD_BATCH` over them and merges the per-record results
  back into the sync's record state (`APPLY_STATE`, `APP_IDENTIFIER`).
