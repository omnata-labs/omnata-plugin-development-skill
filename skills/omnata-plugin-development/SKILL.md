---
name: omnata-plugin-development
description: "Guide for building plugins/connectors for the Omnata Sync Engine on Snowflake. Use when: creating a new Omnata plugin, modifying an existing plugin procedure, debugging plugin behavior, deploying plugin changes, building a plugin end to end, iterating on sync errors. Triggers: omnata plugin, omnata connector, build plugin, create plugin, plugin development, omnata procedure, connection form, sync engine plugin, one-shot plugin, autonomous plugin, build plugin end to end, iterate sync, configure sync, development mode."
---

# Omnata Plugin Development

## When to Use

Use this skill when the user wants to:

- Create a new Omnata plugin procedure (CONNECTION_FORM, NETWORK_ADDRESSES, CONNECTION_TEST, etc.)
- Modify an existing locally developed plugin procedure
- Build an entire plugin end-to-end (one-shot mode)
- Understand the structure of an existing plugin
- Debug or test plugin behavior
- Create a test sync and iterate until it works
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

## Development Modes

This skill supports two development modes. After identifying the target plugin (Step 1), ask the user which mode they prefer.

### Step-by-step mode

CoCo follows the Omnata plugin builder UI stages. The user prompts CoCo for each section (CONNECTION_FORM, NETWORK_ADDRESSES, CONNECTION_TEST, then sync procedures). At each step where design decisions are needed, CoCo stops and asks the user how to approach the design (see Design Decision Prompt below).

Best for users who want to guide each choice and work interactively with both CoCo and the Omnata UI.

### One-shot mode

CoCo builds all plugin procedures end-to-end without stopping between them. Before starting, CoCo asks the user how to handle design decisions (see below). After all procedures are built, CoCo advises the user to create a Connection via the Omnata UI, then offers to create a test sync and iterate changes until it works.

Best for users who want CoCo to build the whole plugin, then test it end-to-end.

## Design Decision Prompt

At steps where design decisions are needed (e.g., what authentication methods to support, which streams to expose, how to paginate API calls), present the user with the following options.

**In Step-by-step mode**, ask at each design point:

1. **CoCo recommends** -- CoCo researches the vendor API docs, presents common patterns, explains tradeoffs, and lets the user choose.
2. **I have a reference to share** -- The user provides context for CoCo to base the design on. This can be:
   - Code from an existing solution (pasted or uploaded)
   - A documentation site URL for CoCo to read
   - An image or screenshot (e.g., of an existing integration's config)
   - A specific open source project to reference

**In One-shot mode**, ask once before building begins:

1. **Stop for CoCo recommendations at each design point** -- CoCo builds autonomously but pauses at each design decision to present options and let the user choose. Building resumes after each decision.
2. **CoCo makes all decisions** -- CoCo reads the vendor API docs and makes reasonable choices autonomously. CoCo documents what was chosen and why. The user can revise later.
3. **I have a reference to share** -- Same as above. CoCo uses the provided reference as the basis for all design decisions. Can be combined with option 1 or 2.

Store the chosen mode and design approach as context for all subsequent steps.

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
      SUPPORTED_CONNECTIVITY_OPTIONS => PARSE_JSON('["direct"]'),
      ICON_SOURCE => '<ICON_SOURCE>'
   );
   ```
This procedure can be called multiple times as details are refined, and it will update the existing record rather than creating duplicates. All parameters other than `PLUGIN_ID` are optional; omitted parameters are left unchanged on an existing plugin.

`ICON_SOURCE` sets the plugin's icon. It is stored as raw SVG markup (the literal `<svg>...</svg>` string, not a URL or base64 data URI) and rendered directly in the UI. Keep it small (a few KB — well under the 256 KB ceiling) and avoid scriptable content (`<script>`, `<foreignObject>`, inline `on*` handlers, `javascript:` URLs), as such content is stripped before display. Omit this parameter if you don't have an icon yet — it can be added on a later call.

The outer <svg> element should have width="100%" and height="100%" so it scales to fit wherever it's shown. Omit this parameter to use a placeholder icon.

4. If working with an existing plugin, **list its procedures**:
   ```sql
   SHOW USER PROCEDURES IN SCHEMA <schema_from_plugin_view>;
   ```

5. To **read an existing procedure body**:
   ```sql
   SELECT GET_DDL('PROCEDURE', '<fully_qualified_procedure_name>(<arg_types>)');
   ```

**Output:** Selected PLUGIN_FQN, plugin name, docs_url, and list of existing procedures.

**STOP**: Confirm which plugin to work on before proceeding.

Note: You do not need to call the `REGISTER_PLUGIN` procedure, that is for external plugins developed outside of the local environment.

### Step 1b: Choose Development Mode

**Goal:** Determine how the user wants to work.

**Actions:**

1. Ask the user to choose a development mode: **Step-by-step** or **One-shot** (see Development Modes above).

2. Based on the chosen mode, ask the design decision question (see Design Decision Prompt above).

3. Record the choices as context for all subsequent steps.

**In Step-by-step mode:** Proceed to Step 2. The user will prompt CoCo for each procedure they want to work on.

**In One-shot mode:** Proceed through Steps 2-5 for each procedure in the standard implementation order:
1. CONNECTION_FORM
2. NETWORK_ADDRESSES
3. CONNECTION_TEST
4. INBOUND_SYNC_PARAMETERS (if inbound plugin)
5. LIST_STREAMS (if inbound plugin)
6. FETCH_RECORD_PAGE (if inbound plugin)
7. OUTBOUND_SYNC_PARAMETERS (if outbound plugin)
8. APPLY_RECORD_BATCH (if outbound plugin)

After completing all procedures, proceed to Step 6 (Connection handoff).

### Step 2: Gather Requirements

**Goal:** Understand what the user wants to build or change.

**Actions:**

1. **Determine the procedure/function type** -- which procedure is being created or modified:
   a) Connection Creation:
     - `CONNECTION_FORM` -- See [references/plugin-objects/CONNECTION_FORM.md](references/plugin-objects/CONNECTION_FORM.md) for details on expected parameters, return values, and handler implementation.
     - `NETWORK_ADDRESSES` -- See [references/plugin-objects/NETWORK_ADDRESSES.md](references/plugin-objects/NETWORK_ADDRESSES.md) for details on expected parameters, return values, and handler implementation.
     - `CONNECTION_TEST` -- See [references/plugin-objects/CONNECTION_TEST.md](references/plugin-objects/CONNECTION_TEST.md) for details on expected parameters, return values, and handler implementation.
     - Other procedure types as documented in the plugin spec
   b) Inbound Sync Configuration:
     - `INBOUND_SYNC_PARAMETERS` -- See [references/plugin-objects/INBOUND_SYNC_PARAMETERS.md](references/plugin-objects/INBOUND_SYNC_PARAMETERS.md) for details on expected parameters, return values, and handler implementation.
     - `LIST_STREAMS` -- See [references/plugin-objects/LIST_STREAMS.md](references/plugin-objects/LIST_STREAMS.md) for details on expected parameters, return values, and handler implementation.
   c) Inbound Sync Execution:
     - `FETCH_RECORD_PAGE` -- For streams of type "simple_pagination". See [references/plugin-objects/FETCH_RECORD_PAGE.md](references/plugin-objects/FETCH_RECORD_PAGE.md) for details on expected parameters, return values, and handler implementation.
   d) Outbound Sync Configuration:
     - `OUTBOUND_SYNC_PARAMETERS` -- See [references/plugin-objects/OUTBOUND_SYNC_PARAMETERS.md](references/plugin-objects/OUTBOUND_SYNC_PARAMETERS.md) for details on expected parameters, return values, and handler implementation. Must include the mandatory `object` field identifying the destination object.
   e) Outbound Sync Execution:
     - `APPLY_RECORD_BATCH` -- For the "batched_rest" outbound style. See [references/plugin-objects/APPLY_RECORD_BATCH.md](references/plugin-objects/APPLY_RECORD_BATCH.md) for details on expected parameters, return values, and handler implementation.

Note: During initial implementation, the ideal order is to implement connection creation procedures (CONNECTION_FORM, NETWORK_ADDRESSES, CONNECTION_TEST) first, and test CONNECTION_FORM and NETWORK_ADDRESSES via direct invocation. Then have the user test CONNECTION_TEST via the plugin builder UI, creating a connection.
After this, the sync-related procedures can be implemented and tested, using the connection created in the previous step.

2. **Fetch external docs** if needed -- use the plugin's `docs_url` from Step 1 to understand the target system's API:
   ```
   web_fetch(url=<docs_url>)
   ```

3. **Estimate sync throughput** -- While reading the vendor API docs, look for:
   - Maximum page size for list/pagination endpoints (e.g., 100, 200, 1000)
   - Published rate limits (e.g., "5 requests per second", "100 requests per 15 seconds")
   - Any pagination-specific limits (e.g., "max offset 50,000")

   If found, present a throughput estimate to the user. Each sync run has a fixed overhead of approximately 90 seconds for sync engine orchestration (Python runtime startup, table staging, checkpointing, per-stream processing). This is based on observed data and dominates for small-to-medium syncs. API call time is additional.

   Calculate using: `pages_needed = records / max_page_size`, `api_time = pages_needed / requests_per_second`, `total = ~90 sec + api_time`.

   Present as a table at various record volumes, for example:

   > **Estimated initial sync time (guide only)**
   >
   > Based on the vendor API docs: max page size is 100 records, rate limit is 5 requests/second.
   >
   > | Records | Pages | API time | Total estimate |
   > |---|---|---|---|
   > | 500 | 5 | ~1 sec | ~90 sec |
   > | 5,000 | 50 | ~10 sec | ~100 sec |
   > | 50,000 | 500 | ~100 sec | ~3 min |
   > | 500,000 | 5,000 | ~17 min | ~18 min |
   >
   > For small volumes, the fixed overhead dominates. API rate limits become the main factor above ~10,000 records. These estimates are a rough guide. Actual times depend on warehouse size, API response times, payload sizes, and whether the API throttles more aggressively under sustained load.

   If the vendor docs do not publish rate limits or page sizes, note that throughput is unknown and the first sync run will reveal actual performance. Skip the table in this case.

4. **Design decisions** -- If this step involves design choices (e.g., authentication methods for CONNECTION_FORM, which streams to expose for LIST_STREAMS, pagination approach for FETCH_RECORD_PAGE), apply the Design Decision Prompt:
   - **Step-by-step mode**: Present the design decision options and wait for the user's choice.
   - **One-shot + stop for recommendations**: Present options at this design point. Resume building after the user decides.
   - **One-shot + CoCo decides**: Read the vendor docs, make reasonable choices, and document what was chosen and why. Proceed without stopping.
   - **Reference provided**: Use the provided reference material to inform the design choices.

5. **Clarify requirements** with the user (Step-by-step mode only):
   - What authentication methods are needed? (for CONNECTION_FORM)
   - What API endpoints does the plugin connect to? (for NETWORK_ADDRESSES)
   - What validation logic should run? (for CONNECTION_TEST)

**Step-by-step mode**: STOP -- confirm requirements before writing any code.

**One-shot mode**: Proceed to Step 3 (unless stopping for a design decision as described above).

### Step 3: Implement the Procedure

**Goal:** Write the Python procedure body as described in the reference doc.

**Step-by-step mode**: Present the implementation to the user for review. STOP -- get approval on the procedure body before deploying.

**One-shot mode**: Implement the procedure and proceed directly to Step 4.

### Step 4: Deploy the Procedure

**Goal:** Register/update the procedure via the Omnata API.

**Actions:**

1. **Prerequisite: The plugin must be registered first.** `SAVE_PLUGIN_STORED_PROCEDURE` will fail
   with "Plugin not found" unless the plugin has already been registered via
   `CONFIGURE_DEVELOPMENT_PLUGIN` (Step 1). Always register/configure the plugin before saving
   procedures.

2. **Call SAVE_PLUGIN_STORED_PROCEDURE** to create or update:
   ```sql
   CALL OMNATA_SYNC_ENGINE.API.SAVE_PLUGIN_STORED_PROCEDURE(
       '<PLUGIN_FQN>',
       '<PROCEDURE_NAME>',
       '<python_body>',
       '<packages_json>'
   );
   ```
   Where:
   - `PLUGIN_FQN` -- the **logical** plugin FQN from the PLUGIN view (e.g. `OMNATA__NOTION_V2`). This is NOT the database.schema path (`OMNATA_PLUGIN_DEVELOPMENT.NOTION_V2`) -- it is the value from the `FQN` column in `OMNATA_SYNC_ENGINE.DATA_VIEWS.PLUGIN`.
   - `PROCEDURE_NAME` -- e.g., 'CONNECTION_FORM', 'CONNECTION_TEST', 'INBOUND_SYNC_PARAMETERS'
   - `python_body` -- the Python code string from Step 3
   - `packages_json` -- JSON array of Snowflake Anaconda packages, e.g., `'["requests","omnata-plugin-runtime"]'`

3. **Check the response** for success/failure.

4. **Verify deployment** by listing procedures again:
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

Once you have a definitive result, **record the test outcome** so it shows in the plugin builder UI:
```sql
CALL OMNATA_SYNC_ENGINE.API.SET_PLUGIN_OBJECT_DEVELOPMENT_STATE(
    '<PLUGIN_FQN>', '<OBJECT_NAME>', 'ai_test_state', 'passed');  -- use 'failed' if it did not pass
```
Where `<OBJECT_NAME>` is the procedure/function name being tested (e.g. `CONNECTION_TEST`,
`FETCH_RECORD_PAGE` -- the names from Step 2). You do not need to set `creation_state`:
`SAVE_PLUGIN_STORED_PROCEDURE` marks the object as `created` automatically when you deploy it.

**Step-by-step mode**: STOP -- report results to the user.

**One-shot mode**: If the test passes, proceed to the next procedure (loop back to Step 2). If the test fails, attempt to fix and retry up to 3 times per procedure. If still failing after 3 attempts, stop and report the issue to the user. After all procedures are built and tested, proceed to Step 6.

**Output:** Working, tested procedure.

### Step 6: Create Connection (User Handoff)

**Goal:** Ensure a connection exists so that end-to-end sync testing can proceed.

This step applies primarily to **One-shot mode** after all procedures are built. In **Step-by-step mode**, the user is typically managing connections via the Omnata UI alongside the plugin builder, so this step is informational.

**Actions:**

1. **Advise the user** that a Connection must be created through the Omnata UI:

   > All plugin procedures are built and tested. To proceed with end-to-end testing, you need to create a Connection using the Omnata UI. This is because each connection requires External Access Integrations, Security Integrations, Network Rules, and Secrets, all of which need Account Admin privileges and a guided setup flow. Open the Omnata UI and use the connection wizard for this plugin.

2. **Wait for the user** to confirm the connection is ready. Do not poll or query automatically.

3. **Find the connection** once the user confirms:
   ```sql
   SELECT
       CONNECTION_ID,
       CONNECTION_NAME,
       CONNECTION_SLUG,
       CONNECTION_METHOD,
       IS_PRODUCTION_ENVIRONMENT
   FROM OMNATA_SYNC_ENGINE.DATA_VIEWS.CONNECTION
   WHERE PLUGIN_FQN = '<plugin_fqn>'
   ORDER BY CONNECTION_ID DESC
   LIMIT 5;
   ```

4. **Present** the connection details and ask: "Do you want me to create a test sync and iterate changes until it works?"

5. If the user agrees, proceed to Step 7. If not, the workflow is complete.

### Step 7: Run-Fix-Iterate Loop (Inbound)

**Goal:** Create a test sync, run it, diagnose failures, fix plugin code, and repeat until the sync works end-to-end.

**Prerequisites:**
- A connection must exist (from Step 6).
- The `omnata-sync-administration-skill` should be installed for deeper diagnostics. If it is not installed, advise the user to install it. CoCo can still perform basic iteration without it, but error classification and event table diagnostics will be limited.

**Actions:**

#### 7a: Create the Test Sync

Use `CONFIGURE_OMNATA_INBOUND_SYNC` to create a sync for testing. Derive parameters from the plugin context:

```sql
CALL OMNATA_SYNC_ENGINE.API.CONFIGURE_OMNATA_INBOUND_SYNC(
    SYNC_SLUG => '<plugin_id>-dev-test',
    SYNC_NAME => '<Plugin Name> (Dev Test)',
    CONNECTION_SLUG => '<connection_slug from Step 6>',
    STREAM_NAMES => ARRAY_CONSTRUCT(<stream names from LIST_STREAMS output>),
    SYNC_STRATEGY => 'auto',
    STORAGE_BEHAVIOUR => 'merge',
    SYNC_PARAMETERS => OBJECT_CONSTRUCT(<from INBOUND_SYNC_PARAMETERS defaults, or empty>),
    SYNC_SCHEDULE => OBJECT_CONSTRUCT(
        'main', OBJECT_CONSTRUCT(
            'mode', 'manual',
            'warehouse', '<available warehouse>',
            'time_limit_mins', 60
        )
    )
);
```

Notes:
- `STREAM_NAMES`: invoke the plugin's LIST_STREAMS procedure to get available streams, then include all of them (or ask the user if in step-by-step mode).
- `SYNC_STRATEGY`: `'auto'` lets the engine choose based on what each stream supports.
- `SYNC_SCHEDULE`: manual mode with a 60-minute time limit for development.
- This procedure is idempotent. Re-calling with the same `SYNC_SLUG` updates the existing sync.

#### 7b: Iterate Loop

Repeat the following cycle up to 5 times:

**1. Run the sync:**
```sql
CALL OMNATA_SYNC_ENGINE.API.RUN_SYNC(
    NULL,
    '<sync_slug>',
    'main',
    'external',
    OBJECT_CONSTRUCT('triggered_by', 'cortex_code_plugin_dev'),
    true,
    false,
    current_user()
);
```
Parameters: SYNC_ID (null when using slug), SYNC_SLUG, BRANCH_NAME, RUN_SOURCE_NAME, RUN_SOURCE_METADATA, WAIT_FOR_COMPLETION (true for dev iteration), RAISE_ERRORS (false to get error info in response), CURRENT_USER.

**2. Check the result:**
```sql
SELECT
    SYNC_RUN_ID,
    HEALTH_STATE,
    GLOBAL_ERROR,
    INBOUND_TOTAL_COUNT,
    INBOUND_NEW_COUNT,
    INBOUND_ERRORED_STREAMS,
    INBOUND_SUCCESSFUL_STREAMS,
    INBOUND_ABANDONED_STREAMS,
    INBOUND_CANCELLED_STREAMS,
    INBOUND_GLOBAL_ERROR_BY_STREAM
FROM OMNATA_SYNC_ENGINE.DATA_VIEWS.SYNC_RUN
WHERE SYNC_ID = (
    SELECT SYNC_ID FROM OMNATA_SYNC_ENGINE.DATA_VIEWS.SYNC
    WHERE SYNC_SLUG = '<sync_slug>'
)
ORDER BY RUN_START_DATETIME DESC
LIMIT 1;
```

**3. Evaluate:**

- **HEALTH_STATE = 'HEALTHY'**: All streams succeeded. Report results (record counts per stream). Proceed to step 4 (incremental validation) if this was the first successful run.

- **HEALTH_STATE = 'FAILED' or 'INCOMPLETE'**: Diagnose and fix (step 5).

**4. Validate incremental behavior (after first successful run):**

The first successful run is always a full refresh. After it passes, CoCo must verify that incremental sync works correctly. This catches two common bugs: broken state management (the plugin re-fetches everything each run) and broken change detection (the plugin returns zero records when changes exist).

**4a. Run the sync a second time** (same RUN_SYNC call as step 1).

**4b. Compare run 2 against run 1.** Query both runs:
```sql
SELECT
    SYNC_RUN_ID,
    RUN_START_DATETIME,
    INBOUND_TOTAL_COUNT,
    INBOUND_NEW_COUNT,
    INBOUND_CHANGED_COUNT,
    INBOUND_STREAM_TOTAL_COUNTS
FROM OMNATA_SYNC_ENGINE.DATA_VIEWS.SYNC_RUN
WHERE SYNC_ID = (
    SELECT SYNC_ID FROM OMNATA_SYNC_ENGINE.DATA_VIEWS.SYNC
    WHERE SYNC_SLUG = '<sync_slug>'
)
ORDER BY RUN_START_DATETIME DESC
LIMIT 2;
```

For each stream that supports incremental sync, compare its total count between run 1 and run 2 using the `INBOUND_STREAM_TOTAL_COUNTS` JSON column.

**4c. Evaluate the incremental results:**

| Run 2 result | Diagnosis | Action |
|---|---|---|
| Run 2 total count is roughly the same as run 1 for an incremental stream | The stream is full-refreshing every time. State is not being persisted or used correctly in FETCH_RECORD_PAGE. | Read the FETCH_RECORD_PAGE procedure body. Check that `new_state` is returned correctly (only on the final page) and that `stream_state` is used to resume from the last cursor position on subsequent runs. Fix and redeploy, then re-run. |
| Run 2 total count is zero or very small (much less than run 1) | Incremental is working: the plugin skipped already-seen records. But zero changes detected means we cannot confirm change detection works. | Proceed to step 4d. |
| Run 2 returns some new/changed records | Incremental sync is verified and working. | Mark development state as passed and exit the loop. |

**4d. Verify change detection (when run 2 had zero changes):**

Tell the user:

> The incremental sync ran successfully but detected no changes, which is expected if nothing changed in the source system. To verify that the incremental path picks up changes correctly, please make a small change to a test record in the source system (e.g., update a field on one record) and let me know when you are done.

Wait for the user to confirm they made a change.

**4e. Run the sync a third time** and check the results:

- If `INBOUND_CHANGED_COUNT > 0` or `INBOUND_NEW_COUNT > 0`: Incremental sync is verified. Mark development state as passed and exit.
  ```sql
  CALL OMNATA_SYNC_ENGINE.API.SET_PLUGIN_OBJECT_DEVELOPMENT_STATE(
      '<PLUGIN_FQN>', 'FETCH_RECORD_PAGE', 'ai_test_state', 'passed');
  ```
- If still zero changes: There is likely a bug in the cursor or change-detection logic in FETCH_RECORD_PAGE. Diagnose by reading the procedure body and checking how `stream_state` and `cursor_field_name` are used to filter for changes. Also check `INBOUND_LATEST_STREAMS_STATE` on the SYNC view to see what state was persisted after run 2. Fix and re-run.

**5. Diagnose a failure (when HEALTH_STATE is FAILED or INCOMPLETE):**

- Read `GLOBAL_ERROR` for run-level failures (often connection or platform issues).
- Read `INBOUND_GLOBAL_ERROR_BY_STREAM` for per-stream errors.
- If the `omnata-sync-administration-skill` is available, load its `references/error-knowledge-base.md` to classify the error by origin (Snowflake-side, endpoint-side, platform-level).
- Identify which procedure is likely at fault based on the error (e.g., auth errors point to CONNECTION_TEST, stream errors point to FETCH_RECORD_PAGE).

**6. Fix the code:**

- Read the failing procedure body: `SELECT GET_DDL('PROCEDURE', '...');`
- Identify the bug from the error message and procedure code.
- Write the fix and redeploy via `SAVE_PLUGIN_STORED_PROCEDURE` (Step 4).
- Loop back to step 1 of this cycle.

**7. After 5 failed iterations:**

Stop the loop. Present the full error history to the user:
- Each iteration's error messages
- What was changed at each step
- The current state of the procedure code

Ask the user for guidance. If the `omnata-sync-administration-skill` is installed, suggest loading its `references/event-table-diagnostics.md` for deeper stack trace analysis.

## Stopping Points

Stopping behavior depends on the development mode:

### Step-by-step mode
- After Step 1: Plugin selection confirmed
- After Step 1b: Development mode chosen
- After Step 2: Requirements and design decisions confirmed (at each procedure)
- After Step 3: Procedure body approved (at each procedure)
- After Step 5: Testing complete (at each procedure)

### One-shot mode
- After Step 1: Plugin selection confirmed
- After Step 1b: Development mode and design approach chosen
- During Steps 2-5: Only if design decision stops were requested (option 1)
- After Step 5 (all procedures): All procedures built and tested
- After Step 6: Connection created, user decides whether to iterate
- After Step 7: Sync works end-to-end, or iteration limit reached

## Output

A deployed and tested Omnata plugin, optionally with a working end-to-end test sync.

## Troubleshooting

### Common Issues

1. **"success": false in response** -- Read the error message. Common causes:
   - Missing or incorrect package in the packages JSON
   - Import errors in the procedure body
   - Parameter type mismatches

2. **Procedure not appearing after save** -- Verify:
   - The PLUGIN_FQN is correct
   - You have sufficient privileges
   - Check `SHOW USER PROCEDURES IN SCHEMA <schema>`

3. **Decorator errors** -- Ensure `omnata-plugin-runtime` is included in the packages JSON

4. **Sync creation fails** -- Verify:
   - The connection slug matches an existing connection for this plugin
   - Stream names match what LIST_STREAMS returns
   - The warehouse specified in SYNC_SCHEDULE exists and is accessible

5. **Sync run fails with GLOBAL_ERROR** -- This is typically a connection-level issue (auth, network). Check that the connection was successfully tested in the Omnata UI before iterating on sync code.

## General Principles

- **Document exact signatures:** For each plugin procedure, the reference doc specifies the exact SQL signature the engine calls and the expected return shape. Always match these exactly.
- **Prefer plain `run(session, ...)` functions** returning the documented dict over `omnata_plugin_runtime` decorators, unless the decorator's expected input exactly matches what the engine passes. Decorators that unpack a single OBJECT payload will fail if the engine passes positional arguments instead.
- Procedures are not created directly with CREATE PROCEDURE -- always use `SAVE_PLUGIN_STORED_PROCEDURE` since external access integrations and secrets must be attached.
- The `omnata-plugin-runtime` package is available from PyPi.
- Existing procedures for other plugins can be a useful reference point, but if at any point they clash with this skill's reference docs, the reference docs take precedence. The engine will call the procedure with the documented signature, and the procedure must return the documented shape.
