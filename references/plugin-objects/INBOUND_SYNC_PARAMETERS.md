# INBOUND_SYNC_PARAMETERS

The INBOUND_SYNC_PARAMETERS procedure is used by the Sync Engine UI during inbound sync
configuration to determine which form fields should be shown to the user before selecting
inbound streams. These field values are then available during stream listing and the sync process.

**Important:** This is the only procedure name the engine calls for this step. Do NOT create a
procedure named `INBOUND_CONFIGURATION_FORM` — that name is never invoked by the engine.

## Stored Procedure signature

```sql
INBOUND_SYNC_PARAMETERS(sync_slug VARCHAR, connection_parameters OBJECT)
RETURNS OBJECT
HANDLER = 'run'
```

| Argument | Type | Description |
|----------|------|-------------|
| `sync_slug` | VARCHAR | An identifier for the sync being configured. |
| `connection_parameters` | OBJECT | The connection's stored field values (e.g. `{"api_token": "..."}` or `{}`). This is **not** the full runtime payload — it does not contain `connectivity_option`, `connection_method`, or secret names. Do not attempt to read those keys. |

## Return value

A plain dict/object with a `fields` key containing an array of form field objects:

```json
{"fields": []}
```

An empty fields list is valid when no additional parameters are needed.

Each field object follows the form-field schema (see `../data-structures.md` for `FormField` types
like `FormInputField`, `FormCheckboxField`, `FormSelectField`, etc.).

## Python handler implementation

Use a plain `run` function — no decorator is needed for this procedure. The function receives the
two SQL arguments directly:

```python
def run(session, sync_slug: str, connection_parameters: dict) -> dict:
    """Return the inbound sync-parameter form fields."""
    return {"fields": []}
```

If your form fields depend on connection parameters, use `.get()` guards since the dict may be
empty:

```python
def run(session, sync_slug: str, connection_parameters: dict) -> dict:
    region = connection_parameters.get("region")
    fields = []
    if region == "eu":
        fields.append({
            "name": "data_residency",
            "label": "Data Residency Zone",
            "type": "select",
            "required": True,
            "options": [
                {"label": "EU West", "value": "eu-west-1"},
                {"label": "EU Central", "value": "eu-central-1"}
            ]
        })
    return {"fields": fields}
```

## Testing

Once deployed, test directly via:
```sql
CALL <plugin database>.<plugin schema>.INBOUND_SYNC_PARAMETERS(
    'test_sync',
    OBJECT_CONSTRUCT('api_token', 'your_token_here')
);
```

Verify the result is a valid form object with a `fields` array.

## Procedure body examples

### Minimal (no parameters needed)

```python
def run(session, sync_slug: str, connection_parameters: dict) -> dict:
    return {"fields": []}
```

### With a checkbox field

```python
def run(session, sync_slug: str, connection_parameters: dict) -> dict:
    return {"fields": [
        {
            "name": "use_bulk_api",
            "label": "Use Bulk API",
            "type": "checkbox",
            "required": True,
            "reload_on_change": True,
            "help_text": "Check this box to use the high-throughput bulk API for this sync."
        }
    ]}
```
