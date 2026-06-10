# INBOUND_STREAM_LIST

The INBOUND_STREAM_LIST procedure is used by the Sync Engine during the sync configuration process for inbound syncs, to provide a list of streams (objects from the source application) for the user to choose from.

## Stored Procedure signature
The Stored Procedure must contain a single OBJECT column named PARAMETERS.
This single argument will be unpacked by the `omnata_plugin_runtime.decorators.inbound_stream_list_handler` wrapper in order to provide the correct python handler arguments.

## Stored Procedure return value
An `OBJECT` value using the standard stored proc convention:
- A successful operation will have `{"success":true,"data":(handler result)}`
- A failed operation will have `{"success":false,"error":(exception message)}`
The `inbound_stream_list_handler` is responsible for converting results/exceptions to this format.

## Python handler implementation
The python handler will be decorated with `@inbound_configuration_form_handler`, and the function name itself should always be `run`
The following function parameters will be expected:
| Name | Python data type |Description |
|--------|-------|-------------|
| `parameters` | `omnata_plugin_runtime.configuration.InboundSyncConfigurationParameters` | The connection parameters and sync parameters entered by the user |

The function will raise an exception if an error is encountered, with a helpful message. Otherwise the function returns a list of `omnata_plugin_runtime.configuration.StreamConfiguration` objects (see `../data-structures.md`)

## Testing
This procedure cannot be invoked until the external access integration is in place and approved by an administrator.
Afterwards, the procedure can be invoked directly via:
```
call <plugin database>.<plugin schema>.INBOUND_STREAM_LIST(OBJECT_CONSTRUCT(
    'connectivity_option','<value connectivity option from SUPPORTED_CONNECTIVITY_OPTIONS>',
    'connection_method','<chosen connection method>',
    'connection_parameters',{ (non-secret parameters from the connection form) },
    'oauth_secret','<name of the OAuth secret to use for secrets, if applicable>',
    'other_secret','<name of the generic string secret to use for all secret parameter values>',
    'sync_parameters', { (sync parameters from the sync configuration form) }
));
```

The SAVE_PLUGIN_STORED_PROCEDURE procedure automatically grants usage of the proc to the application role OMNATA_SYNC_ENGINE.OMNATA_ADMINISTRATOR.

The correct behaviour of the stored proc can be verified by taking the 'data' result field value and performing a Pydantic validation:
```
TypeAdapter(List[StreamConfiguration]).validate_python(result['data'])
```

## Procedure body examples

```
from omnata_plugin_runtime.decorators import (
    inbound_stream_list_handler
)
from omnata_plugin_runtime.configuration import (
    InboundSyncConfigurationParameters,
    StreamConfiguration,
    InboundSyncStrategy
)
import requests

@inbound_stream_list_handler
def run(session: Session, parameters: InboundSyncConfigurationParameters):
    return [
        StreamConfiguration(stream_name='leads',
            supported_sync_strategies=[InboundSyncStrategy.FULL_REFRESH,InboundSyncStrategy.INCREMENTAL],
            source_defined_cursor=True,
            default_cursor_field='last_updated',
            source_defined_primary_key='id',
            json_schema={
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": ["null", "object"],
                "additionalProperties": True,
                "properties": {
                    "id": {"type": ["null", "string"]},
                    "created_at": {"type": ["null", "string"], "format": "date-time","description":"The date and time the object was created"},
                    "email": {"type": ["null", "string"],"description":"The email address of the lead"},
                    "first_name": {"type": ["null", "string"],"description":"The first name of the lead"},
                    "last_name": {"type": ["null", "string"],"description":"The last name of the lead"},
                    "last_updated": {"type": ["null", "string"], "format": "date-time","description":"The date and time the object was last updated."}
                },
            }
        )
    ]
```
