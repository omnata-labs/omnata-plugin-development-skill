# NETWORK_ADDRESSES

The NETWORK_ADDRESSES procedure is used by the Sync Engine during the connection configuration process to determine which domains/ports need to be added to network rules linked to the connection's External Access Integration.

NETWORK_ADDRESSES is invoked after the connection method has been chosen and the parameters have been provided.

## Stored Procedure signature
The Stored Procedure must contain a single OBJECT column named PARAMETERS.
This single argument will be unpacked by the `omnata_plugin_runtime.decorators.network_addresses_handler` wrapper in order to provide the correct python handler arguments.

## Stored Procedure return value
An `OBJECT` value using the standard stored proc convention:
- A successful operation will have `{"success":true,"data":(handler result)}`
- A failed operation will have `{"success":false,"error":(exception message)}`
The `network_addresses_handler` is responsible for converting results/exceptions to this format.

## Python handler implementation
The python handler will be decorated with `@network_addresses_handler`, and the function name itself should always be `run`
The following function parameters will be expected:
| Name | Python data type |Description |
|--------|-------|-------------|
| `parameters` | `omnata_plugin_runtime.configuration.ConnectionConfigurationParameters` | The connection parameters entered by the user |

The function will return a list of NetworkAddresses objects, each of which provide domain names as well as whether or not privatelink should be used. See `../data-structures.md` for the structure of these objects.

## Testing
This procedure can be invoked directly via:
```
call <plugin database>.<plugin schema>.NETWORK_ADDRESSES(OBJECT_CONSTRUCT(
    'connectivity_option','<value connectivity option from SUPPORTED_CONNECTIVITY_OPTIONS>'
    'connection_method','<name of the connection method>'
    'connection_parameters',OBJECT_CONSTRUCT(
        'parameter_a',OBJECT_CONSTRUCT('value','abcdefg'),
        'parameter_b',OBJECT_CONSTRUCT('value','123456')
    )
));
```

The SAVE_PLUGIN_STORED_PROCEDURE procedure automatically grants usage of the proc to the application role OMNATA_SYNC_ENGINE.OMNATA_ADMINISTRATOR.

The correct behaviour of the stored proc can be verified by taking the 'data' result field value and performing a Pydantic validation:
```
TypeAdapter(List[NetworkAddresses]).validate_python(result['data'])
```

## Procedure body examples

### Simple static value

```
from omnata_plugin_runtime.decorators import (
    network_addresses_handler
)
from omnata_plugin_runtime.configuration import (
    ConnectionConfigurationParameters,
    NetworkAddresses
)
from omnata_plugin_runtime.forms import (
    ConnectionMethod,
    FormInputField
)
from typing import List

@network_addresses_handler
def run(parameters:ConnectionConfigurationParameters) -> List[NetworkAddresses]:
    return [
        NetworkAddresses(direct=['api.saasproduct.com'])
    ]
```
