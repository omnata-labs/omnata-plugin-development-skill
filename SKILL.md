---
name: omnata-plugin-development
description: "Guide for building plugins/connectors for the Omnata Sync Engine on Snowflake. Use when: creating a new Omnata plugin, modifying an existing plugin procedure, debugging plugin behavior, deploying plugin changes. Triggers: omnata plugin, omnata connector, build plugin, create plugin, plugin development, omnata procedure, connection form, sync engine plugin."
---

# Omnata Plugin Development

## When to Use

Use this skill when the user wants to:

- Create a new Omnata plugin procedure (CONNECTION_FORM, NETWORK_ADDRESSES, CONNECTION_TEST, etc.)
- Modify an existing locally developed plugin procedure
- Understand the structure of an existing plugin
- Debug or test plugin behavior
- Look up the target system's API documentation for a plugin

## Prerequisites

- Active Snowflake connection with access to `OMNATA_SYNC_ENGINE` application. The user may advise that the application is installed under a different name, but this is the default.
- There are a series of initial setup steps before any plugin development can be done. The status of these can be checked by calling this proc:
```
call OMNATA_SYNC_ENGINE.API.CHECK_PLUGIN_DEVELOPMENT_SETUP();
```
It returns a structure like so:
```
{
  "success": true,
  "checks": {
    "database_accessible": true,    # if false, create a database named OMNATA_PLUGIN_DEVELOPMENT and grant usage to the OMNATA_SYNC_ENGINE application
    "database_role_exists": true,   # if false, create a database role named OMNATA_PLUGIN_DEVELOPMENT.OMNATA_PLUGIN_DEVELOPMENT_ROLE
    "role_granted_to_app": true,    # if false, grant usage of the database role OMNATA_PLUGIN_DEVELOPMENT.OMNATA_PLUGIN_DEVELOPMENT_ROLE to the OMNATA_SYNC_ENGINE application
    "create_schema_grant": true,    # if false, `GRANT CREATE SCHEMA ON DATABASE OMNATA_PLUGIN_DEVELOPMENT TO DATABASE ROLE OMNATA_PLUGIN_DEVELOPMENT`
    "future_schema_grant": true,    # if false, `GRANT OWNERSHIP ON FUTURE SCHEMAS IN DATABASE OMNATA_PLUGIN_DEVELOPMENT TO DATABASE ROLE OMNATA_PLUGIN_DEVELOPMENT.OMNATA_PLUGIN_DEVELOPMENT_ROLE`
    "future_procedure_grant": true, # if false, `GRANT OWNERSHIP ON FUTURE PROCEDURES IN DATABASE OMNATA_PLUGIN_DEVELOPMENT TO DATABASE ROLE OMNATA_PLUGIN_DEVELOPMENT.OMNATA_PLUGIN_DEVELOPMENT_ROLE`
    "future_function_grant": true, # if false, `GRANT OWNERSHIP ON FUTURE FUNCTIONS IN DATABASE OMNATA_PLUGIN_DEVELOPMENT TO DATABASE ROLE OMNATA_PLUGIN_DEVELOPMENT.OMNATA_PLUGIN_DEVELOPMENT_ROLE`
    "future_secret_grant": true,   # if false, `GRANT OWNERSHIP ON FUTURE SECRETS IN DATABASE OMNATA_PLUGIN_DEVELOPMENT TO DATABASE ROLE OMNATA_PLUGIN_DEVELOPMENT.OMNATA_PLUGIN_DEVELOPMENT_ROLE`
    "pypi_repository_user_granted": true # if false, `GRANT DATABASE ROLE SNOWFLAKE.PYPI_REPOSITORY_USER TO APPLICATION OMNATA_SYNC_ENGINE`
  },
  "allReady": true
}
```
If locally developed plugins already exist, there is no need to run the checks up-front as the setup is already complete.

## Setup

This skill is under active development and may change frequently. Always perform an update at the start of each session to ensure you have the latest version:
```
cortex skill update omnata-labs/omnata-plugin-development-skill
```

**Load** [references/data-structures.md](references/data-structures.md) for the Python data structures (Pydantic models and Enums).

**Load** [references/plugin-objects/*](references/plugin-objects/*) for detailed procedure signatures.

## Workflow

### Step 1: Discover Existing Plugins

**Goal:** Understand what plugins exist and identify the target plugin.

**Actions:**

1. **Query** the plugin inventory:
   ```sql
   SELECT *
   FROM OMNATA_SYNC_ENGINE.DATA_VIEWS.PLUGIN
   WHERE DATABASE = 'OMNATA_PLUGIN_DEVELOPMENT'
   ORDER BY NAME;
   ```

2. **Present** the list to the user and ask which plugin to work on (or if creating a new one).

3. If creating a new plugin, **gather details**:
   - Plugin name
   - Description
   - Vendor Docs URL (if available)
   - Supported connectivity options (see ConnectivityOption Enum in data-structures.md). Note that very few SaaS applications support privatelink. Do not assume Privatelink support unless explicitly stated in the vendor docs.

You can derive the plugin id from the name by converting to lowercase, removing non-alphanumeric characters and replacing spaces with underscores.

Call the `CONFIGURE_DEVELOPMENT_PLUGIN` procedure to create a new plugin record:
   ```sql
   CALL OMNATA_SYNC_ENGINE.API.CONFIGURE_DEVELOPMENT_PLUGIN(
      PLUGIN_ID => '<derived_plugin_id>',
      PLUGIN_NAME => '<PLUGIN_NAME>',
      DESCRIPTION => '<DESCRIPTION>',
      DOCS_URL => '<DOCS_URL>',
      SUPPORTED_CONNECTIVITY_OPTIONS => PARSE_JSON('["direct"]')
   );
   ```
This procedure can be called multiple times as details are refined, and it will update the existing record rather than creating duplicates.

4. If working with an existing plugin, **list its procedures**:
   ```sql
   SHOW USER PROCEDURES IN SCHEMA <schema_from_plugin_view>;
   ```

5. To **read an existing procedure body**:
   ```sql
   SELECT GET_DDL('PROCEDURE', '<fully_qualified_procedure_name>(<arg_types>)');
   ```

**Output:** Selected PLUGIN_FQN, plugin name, docs_url, and list of existing procedures.

**⚠️ STOP**: Confirm which plugin and which procedure to work on before proceeding.

Note: You do not need to call the `REGISTER_PLUGIN` procedure, that is for external plugins developed outside of the local environment.

### Step 2: Gather Requirements

**Goal:** Understand what the user wants to build or change.

**Actions:**

1. **Determine the procedure type** — which procedure is being created or modified:
   - `CONNECTION_FORM` — See [references/plugin-objects/CONNECTION_FORM.md](references/plugin-objects/CONNECTION_FORM.md) for details on expected parameters, return values, and handler implementation.
   - `NETWORK_ADDRESSES` — See [references/plugin-objects/NETWORK_ADDRESSES.md](references/plugin-objects/NETWORK_ADDRESSES.md) for details on expected parameters, return values, and handler implementation.
   - `CONNECTION_TEST` — See [references/plugin-objects/CONNECTION_TEST.md](references/plugin-objects/CONNECTION_TEST.md) for details on expected parameters, return values, and handler implementation.
   - Other procedure types as documented in the plugin spec

2. **Fetch external docs** if needed — use the plugin's `docs_url` from Step 1 to understand the target system's API:
   ```
   web_fetch(url=<docs_url>)
   ```

3. **Clarify requirements** with the user:
   - What authentication methods are needed? (for CONNECTION_FORM)
   - What API endpoints does the plugin connect to? (for NETWORK_ADDRESSES)
   - What validation logic should run? (for CONNECTION_TEST)

**⚠️ STOP**: Confirm requirements before writing any code.

### Step 3: Implement the Procedure

**Goal:** Write the Python procedure body as described in the reference doc.

**Present the implementation to the user for review.**

**⚠️ STOP**: Get approval on the procedure body before deploying.

### Step 4: Deploy the Procedure

**Goal:** Register/update the procedure via the Omnata API.

**Actions:**

1. **Call SAVE_PLUGIN_STORED_PROCEDURE** to create or update:
   ```sql
   CALL OMNATA_SYNC_ENGINE.API.SAVE_PLUGIN_STORED_PROCEDURE(
       '<PLUGIN_FQN>',
       '<PROCEDURE_NAME>',
       '<python_body>',
       '<packages_json>'
   );
   ```
   Where:
   - `PLUGIN_FQN` — from the PLUGIN view (Step 1)
   - `PROCEDURE_NAME` — e.g., 'CONNECTION_FORM', 'CONNECTION_TEST'
   - `python_body` — the Python code string from Step 3
   - `packages_json` — JSON array of Snowflake Anaconda packages, e.g., `'["requests","omnata-plugin-runtime"]'`

2. **Check the response** for success/failure.

3. **Verify deployment** by listing procedures again:
   ```sql
   SHOW USER PROCEDURES IN SCHEMA <schema>;
   ```

### Step 5: Test the Procedure

**Goal:** Validate the deployed procedure works correctly.

**Actions:**

Check the Testing section in the procedure reference doc for specific validation steps.

If errors occur:
- Read the error message from `{"success": false, "error": ...}`
- Read the procedure body to debug: `SELECT GET_DDL('PROCEDURE', '...');`
- Fix and redeploy (return to Step 3)

**Output:** Working, tested procedure.

## Stopping Points

- ✋ After Step 1: Plugin and procedure selection confirmed
- ✋ After Step 2: Requirements confirmed
- ✋ After Step 3: Procedure body approved
- ✋ After Step 5: Testing complete, user satisfied

## Output

A deployed and tested Omnata plugin procedure registered with the Sync Engine.

## Troubleshooting

### Common Issues

1. **"success": false in response** — Read the error message. Common causes:
   - Missing or incorrect package in the packages JSON
   - Import errors in the procedure body
   - Parameter type mismatches

2. **Procedure not appearing after save** — Verify:
   - The PLUGIN_FQN is correct
   - You have sufficient privileges
   - Check `SHOW USER PROCEDURES IN SCHEMA <schema>`

3. **Decorator errors** — Ensure `omnata-plugin-runtime` is included in the packages JSON

## Notes

- Procedures are not created directly with CREATE PROCEDURE — always use `SAVE_PLUGIN_STORED_PROCEDURE` since external access integrations and secrets must be attached
- The `omnata-plugin-runtime` package is available from PyPi
