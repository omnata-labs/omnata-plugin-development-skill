# CONNECTION_FORM

The CONNECTION_FORM procedure is used by the Sync Engine during the connection configuration process to provide the user with a set of options for how to connect and authenticate to the remote system, and to define what information must be gathered.

When creating a connection, the user initially chooses a connectivity option - see the `ConnectivityOption` enum in `../data-structures.md` for valid values
The available connectivity options are listed in the SUPPORTED_CONNECTIVITY_OPTIONS array column in the PLUGINS table.

Then, CONNECTION_FORM is invoked to detemine what connection methods are available for that connectivity option. For example, OAuth may be available for direct connections over the internet, but API keys may be used when accessing via Privatelink.

## Stored Procedure signature
The Stored Procedure must contain a single OBJECT column named PARAMETERS.
This single argument will be unpacked by the `omnata_plugin_runtime.decorators.connection_form_handler` wrapper in order to provide the correct python handler arguments.

## Stored Procedure return value
An `OBJECT` value using the standard stored proc convention:
- A successful operation will have `{"success":true,"data":(handler result)}`
- A failed operation will have `{"success":false,"error":(exception message)}`
The `connection_form_handler` is responsible for converting results/exceptions to this format.

## Python handler implementation
The python handler will be decorated with `@connection_form_handler`
The following function parameters will be expected:
| Name | Python data type |Description |
|--------|-------|-------------|
| `connectivity_option` | `omnata_plugin_runtime.configuration.ConnectivityOption` | The Connectivity option chosen by the user |

The function will return a list of ConnectionMethod objects which offer the user various ways to authenticate, along with the associated form options. See `../data-structures.md` for the structure of these objects.

## Testing
This procedure can be invoked directly via:
```
call <plugin database>.<plugin schema>.CONNECTION_FORM('<value connectivity option from SUPPORTED_CONNECTIVITY_OPTIONS>');
```
(values from the PLUGINS record)

The SAVE_PLUGIN_STORED_PROCEDURE procedure automatically grants usage of the proc to the application role OMNATA_SYNC_ENGINE.OMNATA_ADMINISTRATOR.

The correct behaviour of the stored proc can be verified by taking the 'data' result field value and performing a Pydantic validation:
```
TypeAdapter(List[ConnectionMethod]).validate_python(result['data'])
```

## Procedure body examples

### OAuth over internet, API key over privatelink

```
from omnata_plugin_runtime.decorators import (
    connection_form_handler
)
from omnata_plugin_runtime.configuration import (
    ConnectivityOption
)
from omnata_plugin_runtime.forms import (
    ConnectionMethod,
    FormInputField
)
from typing import List

@connection_form_handler
def connection_form(connectivity_option:ConnectivityOption) -> List[ConnectionMethod]:
    if connectivity_option == ConnectivityOption.DIRECT:
        return [
            ConnectionMethod(
                name="OAuth (Client Credentials)",
                fields=[
                    FormInputField(
                        name="domain",
                        label="Domain",
                        required=True,
                        help_text="The domain of the application instance"
                    ),
                    FormInputField(
                        name="consumer_key",
                        label="Consumer Key",
                        required=True,
                        help_text="The Consumer Key for the OAuth App"
                    ),
                    FormInputField(
                        name="consumer_secret",
                        label="Consumer Secret",
                        required=True,
                        secret=True,
                        help_text="The Consumer Secret for the OAuth App"
                    )
                ]
            )
        ]
    elif connectivity_option == ConnectivityOption.PRIVATELINK:
        return [
            ConnectionMethod(
                name="API Key",
                fields=[
                    FormInputField(
                        name="api_key",
                        label="API Key",
                        required=True,
                        help_text="The API Key for connecting over privatelink"
                    )
                ]
            )
        ]
    else:
        raise ValueError(f"Unsupported Connectivity Option: {connectivity_option})
```
