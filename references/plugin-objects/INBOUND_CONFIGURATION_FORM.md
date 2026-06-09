# INBOUND_CONFIGURATION_FORM

The INBOUND_CONFIGURATION_FORM procedure is used by the Sync Engine during the sync configuration process for inbound syncs, to determine which configuration form fields should be shown to the user before selecting inbound streams.

These field values are then available during stream listing and the sync process.

## Stored Procedure signature
The Stored Procedure must contain a single OBJECT column named PARAMETERS.
This single argument will be unpacked by the `omnata_plugin_runtime.decorators.inbound_configuration_form_handler` wrapper in order to provide the correct python handler arguments.

## Stored Procedure return value
An `OBJECT` value using the standard stored proc convention:
- A successful operation will have `{"success":true,"data":(handler result)}`
- A failed operation will have `{"success":false,"error":(exception message)}`
The `inbound_configuration_form_handler` is responsible for converting results/exceptions to this format.

## Python handler implementation
The python handler will be decorated with `@inbound_configuration_form_handler`, and the function name itself should always be `run`
The following function parameters will be expected:
| Name | Python data type |Description |
|--------|-------|-------------|
| `parameters` | `omnata_plugin_runtime.configuration.ConnectionConfigurationParameters` | The connection parameters entered by the user |

The function will raise an exception if the connection test fails, with a helpful message. If the connection test succeeds, the function returns a `omnata_plugin_runtime.omnata_plugin.ConnectResponse` object (see `../data-structures.md`)

## Testing
This procedure cannot be invoked until the external access integration is in place and approved by an administrator.
Afterwards, the procedure can be invoked directly via:
```
call <plugin database>.<plugin schema>.CONNECTION_FORM(OBJECT_CONSTRUCT(
    'connectivity_option','<value connectivity option from SUPPORTED_CONNECTIVITY_OPTIONS>',
    'connection_method','<chosen connection method>',
    'connection_parameters',{ (non-secret parameters from the connection form) },
    'oauth_secret','<name of the OAuth secret to use for secrets, if applicable>',
    'other_secret','<name of the generic string secret to use for all secret parameter values>'
));
```

The SAVE_PLUGIN_STORED_PROCEDURE procedure automatically grants usage of the proc to the application role OMNATA_SYNC_ENGINE.OMNATA_ADMINISTRATOR.

The correct behaviour of the stored proc can be verified by taking the 'data' result field value and performing a Pydantic validation:
```
TypeAdapter(ConnectResponse).validate_python(result['data'])
```

## Procedure body examples

```
from omnata_plugin_runtime.decorators import (
    connection_test_handler
)
import requests

@connection_test_handler
def run(self, parameters: ConnectionConfigurationParameters) -> ConnectResponse
    if parameters.connection_method == "api_key":
        api_key = parameters.get_connection_secret("api_key").value
        domain = parameters.get_connection_parameter("domain").value
        response = requests.get(f"https://{domain}/v2/account_info")
        response.raise_for_error()
        return ConnectResponse()
    raise ValueError(f"Unknown connection method {parameters.connection_method}")
```
