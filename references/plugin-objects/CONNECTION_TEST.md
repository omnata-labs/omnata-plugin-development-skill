# CONNECTION_TEST

The CONNECTION_TEST procedure is used by the Sync Engine during the connection configuration process to check that the provided credentials work against the target system.

When creating a connection, the user initially chooses a connectivity option - see the `ConnectivityOption` enum in `../data-structures.md` for valid values
The available connectivity options are listed in the SUPPORTED_CONNECTIVITY_OPTIONS array column in the PLUGINS table.

Then, CONNECTION_FORM is invoked to detemine what connection methods are available for that connectivity option. For example, OAuth may be available for direct connections over the internet, but API keys may be used when accessing via Privatelink.

Once the connection form has been completed, the NETWORK_ADDRESSES procedure is called to determine which endpoints must be permitted access via network rules attached to an external access integration.

Finally, once all of this information is gathered and an administrator has approved the external access, the CONNECTION_TEST procedure performs the test. The connection test can also be performed any time after a connection has been created.

## Stored Procedure signature
The Stored Procedure must contain a single OBJECT column named PARAMETERS.
This single argument will be unpacked by the `omnata_plugin_runtime.decorators.connection_test_handler` wrapper in order to provide the correct python handler arguments.

## Stored Procedure return value
An `OBJECT` value using the standard stored proc convention:
- A successful operation will have `{"success":true,"data":(handler result)}`
- A failed operation will have `{"success":false,"error":(exception message)}`
The `connection_test_handler` is responsible for converting results/exceptions to this format.

## Python handler implementation
The python handler will be decorated with `@connection_test_handler`, and the function name itself should always be `run`
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
from omnata_plugin_runtime.omnata_plugin import (
    ConnectResponse
)
from omnata_plugin_runtime.configuration import (
    ConnectionConfigurationParameters
)
from snowflake.snowpark import Session
import requests

@connection_test_handler
def run(self, session: Session, parameters: ConnectionConfigurationParameters) -> ConnectResponse
    if parameters.connection_method == "api_key":
        api_key = parameters.get_connection_secret("api_key").value
        domain = parameters.get_connection_parameter("domain").value
        response = requests.get(f"https://{domain}/v2/account_info")
        response.raise_for_error()
        return ConnectResponse()
    raise ValueError(f"Unknown connection method {parameters.connection_method}")
```
