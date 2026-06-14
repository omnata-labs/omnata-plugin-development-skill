# INBOUND_SYNC_PARAMETERS

The INBOUND_SYNC_PARAMETERS procedure is used by the Sync Engine during the sync configuration process for inbound syncs, to determine which configuration form fields should be shown to the user before selecting inbound streams.

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

The function will raise an exception if the connection test fails, with a helpful message. If the connection test succeeds, the function returns a `omnata_plugin_runtime.forms.InboundSyncConfigurationForm` object (see `../data-structures.md`)

## Testing
This procedure cannot be invoked until the external access integration is in place and approved by an administrator.
Afterwards, the procedure can be invoked directly via:
```
call <plugin database>.<plugin schema>.INBOUND_SYNC_PARAMETERS(OBJECT_CONSTRUCT(
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
TypeAdapter(InboundSyncConfigurationForm).validate_python(result['data'])
```

## Procedure body examples

```
from omnata_plugin_runtime.forms import (
    FormCheckboxField,
    InboundSyncConfigurationForm
)
from omnata_plugin_runtime.decorators import (
    inbound_configuration_form_handler
)
from omnata_plugin_runtime.configuration import (
    ConnectionConfigurationParameters,
)

@inbound_configuration_form_handler
def run(session: Session, parameters: ConnectionConfigurationParameters):
    return InboundSyncConfigurationForm(fields=[
        FormCheckboxField(name='use_bulk_api',
            label='Use Bulk API',
            required=True,
            reload_on_change=True,
            help_text='Check this box to use the high-throughput bulk API for this sync. Uncheck to use the standard API.')
    ])
```
