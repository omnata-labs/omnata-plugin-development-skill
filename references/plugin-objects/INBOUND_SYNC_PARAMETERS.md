# INBOUND_SYNC_PARAMETERS

The INBOUND_SYNC_PARAMETERS procedure is used by the Sync Engine UI during inbound sync
configuration to determine which form fields should be shown to the user before selecting
inbound streams. These field values are then available during stream listing and the sync process.

**Important:** `INBOUND_SYNC_PARAMETERS` is the procedure name the engine calls for this step.
Do not create a *procedure* named `INBOUND_CONFIGURATION_FORM` — that procedure name is never
invoked by the engine. Note that the handler is nonetheless decorated with
`@inbound_configuration_form_handler`: the decorator name refers to the internal
`inbound_configuration_form` operation, not to the procedure name.

## Stored Procedure signature

The Stored Procedure must contain a single OBJECT column named PARAMETERS. This single argument is
unpacked by the `omnata_plugin_runtime.decorators.inbound_configuration_form_handler` wrapper in
order to provide the correct python handler arguments.

```sql
INBOUND_SYNC_PARAMETERS(PARAMETERS OBJECT)
RETURNS OBJECT
HANDLER = 'run'
```

The `PARAMETERS` object carries the keys the wrapper reads: `connectivity_option`,
`connection_method`, `connection_parameters`, `oauth_secret`, `other_secrets`, and
`connection_secrets_direct`. The decorator resolves the secrets and builds a
`ConnectionConfigurationParameters` instance before your handler runs, so at this step your handler
has the connection details and secrets available (but not the sync parameters, which are not yet
finalised).

## Stored Procedure return value

An `OBJECT` value using the standard stored proc convention:
- A successful operation will have `{"success":true,"data":(serialized InboundSyncConfigurationForm)}`
- A failed operation will have `{"success":false,"error":(exception message)}`

The `inbound_configuration_form_handler` is responsible for converting results/exceptions to this
format, so your handler simply returns an `InboundSyncConfigurationForm` (or raises).

## Python handler implementation

The python handler is decorated with `@inbound_configuration_form_handler`, and the function name
itself should always be `run`. The following function parameters will be expected:

| Name | Python data type | Description |
|------|------------------|-------------|
| `parameters` | `omnata_plugin_runtime.configuration.ConnectionConfigurationParameters` | The resolved connection parameters and secrets entered by the user |

The handler returns an `InboundSyncConfigurationForm` whose `fields` is a list of form fields (see
`../data-structures.md` for `InboundSyncConfigurationForm` and the `FormField` types like
`FormInputField`, `FormCheckboxField`, `FormDropdownField`, etc.). An empty `fields` list is valid
when no additional parameters are needed.

```python
from omnata_plugin_runtime.decorators import inbound_configuration_form_handler
from omnata_plugin_runtime.forms import InboundSyncConfigurationForm
from omnata_plugin_runtime.configuration import ConnectionConfigurationParameters
from snowflake.snowpark import Session


@inbound_configuration_form_handler
def run(session: Session, parameters: ConnectionConfigurationParameters) -> InboundSyncConfigurationForm:
    """Return the inbound sync-parameter form fields."""
    return InboundSyncConfigurationForm(fields=[])
```

If your form fields depend on connection parameters, read them from the resolved
`ConnectionConfigurationParameters`. Guard for optional values, since a parameter may not be
present:

```python
from omnata_plugin_runtime.decorators import inbound_configuration_form_handler
from omnata_plugin_runtime.forms import FormDropdownField, InboundSyncConfigurationForm
from omnata_plugin_runtime.configuration import ConnectionConfigurationParameters
from snowflake.snowpark import Session


@inbound_configuration_form_handler
def run(session: Session, parameters: ConnectionConfigurationParameters) -> InboundSyncConfigurationForm:
    fields = []
    region_param = parameters.get_connection_parameter("region")
    if region_param is not None and region_param.value == "eu":
        fields.append(FormDropdownField(
            name="data_residency",
            label="Data Residency Zone",
            required=True,
            values=[
                {"label": "EU West", "value": "eu-west-1"},
                {"label": "EU Central", "value": "eu-central-1"},
            ],
        ))
    return InboundSyncConfigurationForm(fields=fields)
```

## Reload-on-change

A field can set `reload_on_change=True` so that changing its value re-invokes
`INBOUND_SYNC_PARAMETERS` with the updated values. This is how a form can react to earlier answers.

## Testing

Once deployed, test directly via:
```sql
CALL <plugin database>.<plugin schema>.INBOUND_SYNC_PARAMETERS(OBJECT_CONSTRUCT(
    'connectivity_option', '<value from SUPPORTED_CONNECTIVITY_OPTIONS>',
    'connection_method', '<chosen connection method>',
    'connection_parameters', { (non-secret parameters from the connection form) },
    'oauth_secret', '<name of the OAuth secret, if applicable>',
    'other_secrets', '<name of the generic string secret for secret parameter values>'
));
```

The result uses the standard `{"success":true,"data":...}` convention. The correct behaviour can be
verified by taking the `data` result field value and performing a Pydantic validation:
```python
TypeAdapter(InboundSyncConfigurationForm).validate_python(result['data'])
```

## Procedure body examples

### Minimal (no parameters needed)

```python
@inbound_configuration_form_handler
def run(session: Session, parameters: ConnectionConfigurationParameters) -> InboundSyncConfigurationForm:
    return InboundSyncConfigurationForm(fields=[])
```

### With a checkbox field

```python
from omnata_plugin_runtime.forms import FormCheckboxField, InboundSyncConfigurationForm


@inbound_configuration_form_handler
def run(session: Session, parameters: ConnectionConfigurationParameters) -> InboundSyncConfigurationForm:
    return InboundSyncConfigurationForm(fields=[
        FormCheckboxField(
            name="use_bulk_api",
            label="Use Bulk API",
            required=True,
            reload_on_change=True,
            help_text="Check this box to use the high-throughput bulk API for this sync. Uncheck to use the standard API.",
        )
    ])
```
