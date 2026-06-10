# FETCH_RECORD_PAGE

The FETCH_RECORD_PAGE UDTF is used by the Sync Engine during syncing, to fetch pages of records.

The UDTF is invoked repeatedly until all records have been returned for the stream.

## UDTF signature
The UDTF must contain a single OBJECT column named PARAMETERS.
This single argument will be unpacked by the `omnata_plugin_runtime.decorators.inbound_sync_rest_paginated_handler` wrapper in order to provide the correct python handler arguments.

## UDTF return columns
The 'returns' clause is:
`table(RECORD object,NEW_STATE object,RUN_VARIABLES object)`
Where:
- RECORD: the data record as a dict
- NEW_STATE: updated cursor/checkpoint state (or None to keep existing)
- RUN_VARIABLES: variables for next page request (not persisted as state)
The `inbound_sync_rest_paginated_handler` yields whatever it is given by the wrapped function, so the UDTF must yield results to this format.
Unlike the stored procedures, errors are simply thrown by the UDTF and will be caught by the sync engine.

## Python handler implementation
The python handler class will be decorated with `@inbound_sync_rest_paginated_handler`, and it will be a standard UDTF python class with a `process` function.
The following function parameters will be expected:
| Name | Python data type | Description |
|--------|-------|-------------|
| `parameters` | `omnata_plugin_runtime.configuration.InboundSyncConfigurationParameters` | The connection and sync parameters provided by the user |
| `stream_name` | `str` | The name of the stream |
| `stream_state` | `Dict[str,Any]` | The current stream state |
| `current_run_variables` | `Dict[str,any]` | Non-state variables used in the current run |
| `page_size` | `int` | The number of records to return |


## Testing
This procedure cannot be invoked unless:
1) A connection has been created
2) Streams have been selected and configured by the user.

Afterwards, the procedure can be invoked directly via:
```
select * from table(<plugin database>.<plugin schema>.FETCH_RECORD_PAGE(OBJECT_CONSTRUCT(
    'connectivity_option','<value connectivity option from SUPPORTED_CONNECTIVITY_OPTIONS>',
    'connection_method','<chosen connection method>',
    'connection_parameters',{ (non-secret parameters from the connection form) },
    'oauth_secret','<name of the OAuth secret to use for secrets, if applicable>',
    'other_secret','<name of the generic string secret to use for all secret parameter values>',
    'stream_name','<stream name>',
    'stream_state', {},
    'current_run_variables',{},
    'page_size',100
));
```

The SAVE_PLUGIN_STORED_PROCEDURE procedure automatically grants usage of the proc to the application role OMNATA_SYNC_ENGINE.OMNATA_ADMINISTRATOR.

## Procedure body examples

```
from omnata_plugin_runtime.configuration import (
    InboundSyncConfigurationParameters,
    StreamConfiguration,
    InboundSyncStrategy
)
from omnata_plugin_runtime.decorators import (
    inbound_sync_rest_paginated_handler
)
@inbound_sync_rest_paginated_handler
class MyUDTF:
    def process(self,
        parameters: InboundSyncConfigurationParameters,
        stream_name: str,
        stream_state: Dict[str, Any],
        current_run_variables: Dict[str, Any],
        page_size: int) -> Iterable[Tuple[dict, dict, dict]]:
            # Fetch one page of records from the external API
            # Yield tuples of (record, new_state, run_variables)
            # - record: the data record as a dict
            # - new_state: updated cursor/checkpoint state (or None to keep existing)
            # - run_variables: variables for next page request (not persisted as state)
            # Fetch records from the remote endpoint
            api_domain = connection_parameters.get_connection_parameter('api_domain').value
            url = f"https://{api_domain}/objects/{stream_name}"
            token = connection_parameter.get_connection_secret('api_key').value
            request_body = {'limit':page_size, 'order_by':'updated_date'}
            if 'updated_after' in run_variables:
                request_body['updated_after'] = stream_state['last_updated_date']
            if 'offset' in run_variables:
                request_body['offset'] = run_variables['offset']
            responses = requests.post(
                url=url,
                json=request_body,
                headers={'Authorization': f'Bearer {token}'}
            )
            response.raise_for_status()
            results = response.json()['records']
            run_variables['offset'] = run_variables['offset'] + page_size
            new_state['updated_after'] = max([r['updated_date'] for r in results])
            for result in results:
                yield (result, stream_state, current_run_variables)
```
