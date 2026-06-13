# OUTBOUND_CONFIGURATION_FORM

A **stored procedure** that a plugin implements to describe the form a consumer fills in when
configuring an **outbound** sync with the plugin. It returns an `OutboundSyncConfigurationForm` —
the set of fields (and their types, defaults, help text, etc.) that make up the sync's parameters.
These values become the sync's `sync_parameters` and are passed to `APPLY_RECORD_BATCH` at run time.

It lives in the plugin's schema (for interactive plugins:
`OMNATA_PLUGIN_DEVELOPMENT.<PLUGIN_ID>.OUTBOUND_CONFIGURATION_FORM`) and is generated with the
`@outbound_configuration_form_handler` decorator from `omnata_plugin_runtime.decorators`.

This is the outbound counterpart of `INBOUND_CONFIGURATION_FORM`; the shape is the same, only the
parameter/return types and the mandatory `object` field differ.

## Signature

```sql
OUTBOUND_CONFIGURATION_FORM(parameters object)
RETURNS object
```

The single `parameters` object carries `operation` (`'outbound_configuration_form'`),
`connectivity_option`, `connection_method`, `connection_parameters`, the secret names
`oauth_secret` / `other_secrets`, `sync_parameters` (the values entered so far), and `target_type`.
The `@outbound_configuration_form_handler` decorator resolves the secrets and converts this into an
`OutboundSyncConfigurationParameters` instance before your handler runs.

## Return value

An `OutboundSyncConfigurationForm` (serialised to an object), whose `fields` is a list of form
fields. The available field types are the same as elsewhere in the plugin SDK
(`FormInputField`, `FormDropdownField`, `FormCheckboxField`, `FormRadioField`, `FormTextAreaField`,
information fields, etc.).

## The mandatory "object" field

Every outbound configuration form **must include a field named `object`** that identifies which
destination object the records are synced to (e.g. `contacts`, `companies`). Outbound is not tied
to a first-class "target object" concept in the sync engine, so this field is the convention by
which the destination is selected. `APPLY_RECORD_BATCH` reads it from
`parameters.get_sync_parameter('object')`, and the **field mapper** uses it to know which target
fields are available. A `FormDropdownField` (populated from the destination's object list) or a
`FormInputField` are both fine.

## Reload-on-change

As with the inbound form, a field can set `reload_on_change=True` so that changing its value
re-invokes `OUTBOUND_CONFIGURATION_FORM` with the updated `sync_parameters`. This is how a form can
react to earlier answers — for example, fetching the list of fields available on the chosen
`object` once it has been selected.

## Example

```python
from omnata_plugin_runtime.forms import (
    FormDropdownField,
    FormInputField,
    OutboundSyncConfigurationForm,
)
from omnata_plugin_runtime.configuration import OutboundSyncConfigurationParameters
from omnata_plugin_runtime.decorators import outbound_configuration_form_handler
from snowflake.snowpark import Session


@outbound_configuration_form_handler
def outbound_configuration_form(session: Session, parameters: OutboundSyncConfigurationParameters):
    # The destination object every outbound sync must choose.
    object_field = FormDropdownField(
        name='object',
        label='Target Object',
        required=True,
        reload_on_change=True,
        help_text='The destination object that records are synced to.',
        # values could be fetched from the destination using the resolved connection/secrets
        values=[{'value': 'contacts', 'label': 'Contacts'}, {'value': 'companies', 'label': 'Companies'}],
    )
    fields = [object_field]

    # Additional parameters can depend on the chosen object.
    if parameters.sync_parameter_exists('object'):
        fields.append(FormInputField(
            name='external_id_field',
            label='External ID Field',
            required=False,
            help_text='Field on the target object used to match existing records for updates.',
        ))

    return OutboundSyncConfigurationForm(fields=fields)
```

## How it's invoked

- **Sync configuration (consumer):** when a consumer configures an outbound sync with the plugin,
  the engine calls `OUTBOUND_CONFIGURATION_FORM` to render the parameter form. The values collected
  become the sync's `sync_parameters`.
- **Development wizard:** the plugin developer authors this procedure in the Sync Configuration step
  (the same way `INBOUND_CONFIGURATION_FORM` is authored for inbound), and the wizard always ensures
  the `object` field is present.
- **At run time:** `APPLY_RECORD_BATCH` receives the collected `sync_parameters` (including
  `object`) on its `connection_parameters` argument.
