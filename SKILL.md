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
- The `OMNATA_PLUGIN_DEVELOPMENT` database must exist for locally developed plugins

## Setup

**Load** [references/data-structures.md](references/data-structures.md) for the Python data structures (Pydantic models and Enums).

**Load** [references/plugin-objects/*](references/plugin-objects/*) for detailed procedure signatures.

## Workflow

### Step 1: Discover Existing Plugins

**Goal:** Understand what plugins exist and identify the target plugin.

**Actions:**

1. **Query** the plugin inventory:
   ```sql
   SELECT PLUGIN_FQN, NAME, DOCS_URL, SCHEMA, DATABASE
   FROM OMNATA_SYNC_ENGINE.DATA_VIEWS.PLUGIN
   WHERE DATABASE = 'OMNATA_PLUGIN_DEVELOPMENT'
   ORDER BY NAME;
   ```

2. **Present** the list to the user and ask which plugin to work on (or if creating a new one).

3. If working with an existing plugin, **list its procedures**:
   ```sql
   SHOW USER PROCEDURES IN SCHEMA <schema_from_plugin_view>;
   ```

4. To **read an existing procedure body**:
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

1. For **CONNECTION_FORM**, test by calling:
   ```sql
   CALL OMNATA_SYNC_ENGINE.API.GET_CONNECTION_FORM('<PLUGIN_FQN>');
   ```
   Verify the returned connection methods and form options are correct.

2. For other procedures, call them directly or through the appropriate API procedure.

3. **Check response format** — should be `{"success": true, "data": ...}` for success.

4. If errors occur:
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
