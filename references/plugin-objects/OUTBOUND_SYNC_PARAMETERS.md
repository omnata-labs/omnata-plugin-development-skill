# OUTBOUND_SYNC_PARAMETERS

The OUTBOUND_SYNC_PARAMETERS procedure is used by the Sync Engine UI during outbound sync
configuration to determine which form fields should be shown to the user before selecting the
outbound destination. These field values become the sync's `sync_parameters` and are passed to
`APPLY_RECORD_BATCH` at run time.

**Important:** `OUTBOUND_SYNC_PARAMETERS` is the procedure name the engine calls for this step.
Do not create a *procedure* named `OUTBOUND_CONFIGURATION_FORM` — that procedure name is never
invoked by the engine. Note that the handler is nonetheless decorated with
`@outbound_configuration_form_handler`: the decorator name refers to the `outbound_configuration_form`
operation it implements, not to the procedure name.

## Stored Procedure signature

The Stored Procedure must contain a single OBJECT column named PARAMETERS. This single argument is
unpacked by the `omnata_plugin_runtime.decorators.outbound_configuration_form_handler` wrapper in
order to provide the correct python handler arguments.

```sql
OUTBOUND_SYNC_PARAMETERS(PARAMETERS OBJECT)
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
- A successful operation will have `{"success":true,"data":(serialized OutboundSyncConfigurationForm)}`
- A failed operation will have `{"success":false,"error":(exception message)}`

The `outbound_configuration_form_handler` is responsible for converting results/exceptions to this
format, so your handler simply returns an `OutboundSyncConfigurationForm` (or raises).

## The mandatory "object" field

Every outbound sync-parameter form **must include a field named `object`** that identifies which
destination object the records are synced to (e.g. `contacts`, `companies`). Outbound is not tied
to a first-class "target object" concept in the sync engine, so this field is the convention by
which the destination is selected. At run time `APPLY_RECORD_BATCH` reads it from
`parameters.get_sync_parameter('object')`, and the **field mapper** uses it to know which target
fields are available. A `FormDropdownField` (populated from the destination's object list) or a
`FormInputField` are both fine.

## Python handler implementation

The python handler is decorated with `@outbound_configuration_form_handler`, and the function name
itself should always be `run`. The following function parameters will be expected:

| Name | Python data type | Description |
|------|------------------|-------------|
| `parameters` | `omnata_plugin_runtime.configuration.ConnectionConfigurationParameters` | The resolved connection parameters and secrets entered by the user |

The handler returns an `OutboundSyncConfigurationForm` whose `fields` is a list of form fields (see
`../data-structures.md` for `OutboundSyncConfigurationForm` and the `FormField` types like
`FormInputField`, `FormCheckboxField`, `FormDropdownField`, etc.).

```python
from omnata_plugin_runtime.decorators import outbound_configuration_form_handler
from omnata_plugin_runtime.forms import FormDropdownField, OutboundSyncConfigurationForm
from omnata_plugin_runtime.configuration import ConnectionConfigurationParameters
from snowflake.snowpark import Session


@outbound_configuration_form_handler
def run(session: Session, parameters: ConnectionConfigurationParameters) -> OutboundSyncConfigurationForm:
    # The destination object every outbound sync must choose.
    return OutboundSyncConfigurationForm(fields=[
        FormDropdownField(
            name="object",
            label="Object",
            required=True,
            reload_on_change=True,
            help_text="The destination object to sync records to.",
            # values could be fetched from the destination using the resolved connection/secrets
            values=[{"value": "contacts", "label": "Contacts"}, {"value": "companies", "label": "Companies"}],
        )
    ])
```

If your form fields depend on connection parameters, read them from the resolved
`ConnectionConfigurationParameters`. Guard for optional values, since a parameter may not be
present:

```python
from omnata_plugin_runtime.decorators import outbound_configuration_form_handler
from omnata_plugin_runtime.forms import FormDropdownField, FormInputField, OutboundSyncConfigurationForm
from omnata_plugin_runtime.configuration import ConnectionConfigurationParameters
from snowflake.snowpark import Session


@outbound_configuration_form_handler
def run(session: Session, parameters: ConnectionConfigurationParameters) -> OutboundSyncConfigurationForm:
    fields = [
        FormDropdownField(
            name="object",
            label="Object",
            required=True,
            reload_on_change=True,
            help_text="The destination object to sync records to.",
            values=[{"value": "contacts", "label": "Contacts"}, {"value": "companies", "label": "Companies"}],
        )
    ]
    region_param = parameters.get_connection_parameter("region")
    if region_param is not None and region_param.value == "eu":
        fields.append(FormInputField(
            name="external_id_field",
            label="External ID Field",
            required=False,
            help_text="Field on the target object used to match existing records for updates.",
        ))
    return OutboundSyncConfigurationForm(fields=fields)
```

## Reload-on-change

A field can set `reload_on_change=True` so that changing its value re-invokes
`OUTBOUND_SYNC_PARAMETERS`. This is how a form can react to earlier answers.

## Testing

Once deployed, test directly via:
```sql
CALL <plugin database>.<plugin schema>.OUTBOUND_SYNC_PARAMETERS(OBJECT_CONSTRUCT(
    'connectivity_option', '<value from SUPPORTED_CONNECTIVITY_OPTIONS>',
    'connection_method', '<chosen connection method>',
    'connection_parameters', { (non-secret parameters from the connection form) },
    'oauth_secret', '<name of the OAuth secret, if applicable>',
    'other_secrets', '<name of the generic string secret for secret parameter values>'
));
```

The result uses the standard `{"success":true,"data":...}` convention. Verify the `data` field is a
valid form object with a `fields` array that includes the mandatory `object` field, e.g. via a
Pydantic validation:
```python
TypeAdapter(OutboundSyncConfigurationForm).validate_python(result['data'])
```

## How it's invoked

- **Sync configuration (consumer):** when a consumer configures an outbound sync with the plugin,
  the engine calls `OUTBOUND_SYNC_PARAMETERS` to render the parameter form. The values collected
  become the sync's `sync_parameters`.
- **Development wizard:** the plugin developer authors this procedure in the Sync Configuration
  step, and the wizard always ensures the `object` field is present.
- **At run time:** `APPLY_RECORD_BATCH` receives the collected `sync_parameters` (including
  `object`).
