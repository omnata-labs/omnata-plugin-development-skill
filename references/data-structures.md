# Pydantic Models and Enums — `omnata_plugin_runtime`

Auto-generated from `omnata_plugin_runtime`. Re-run `export_pydantic_schemas.py` after package updates.

# Enums

## ConnectivityOption
**Import:** `from omnata_plugin_runtime.configuration import ConnectivityOption`  
**Module:** `omnata_plugin_runtime.configuration.ConnectivityOption`

Describes the connectivity options available to a plugin.
These result in slightly different network rules and connection onboarding.

| Member | Value | Description |
|--------|-------|-------------|
| `DIRECT` | `'direct'` |  |
| `NGROK` | `'ngrok'` |  |
| `PRIVATELINK` | `'privatelink'` |  |

---

## InboundStorageBehaviour
**Import:** `from omnata_plugin_runtime.configuration import InboundStorageBehaviour`  
**Module:** `omnata_plugin_runtime.configuration.InboundStorageBehaviour`

str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.

| Member | Value | Description |
|--------|-------|-------------|
| `APPEND` | `'append'` |  |
| `MERGE` | `'merge'` |  |
| `REPLACE` | `'replace'` |  |

---

## InboundStorageBehaviourBulkConfiguration
**Import:** `from omnata_plugin_runtime.configuration import InboundStorageBehaviourBulkConfiguration`  
**Module:** `omnata_plugin_runtime.configuration.InboundStorageBehaviourBulkConfiguration`

Supercedes InboundSyncBulkConfiguration, which was a combination of sync strategy and storage behaviour.

| Member | Value | Description |
|--------|-------|-------------|
| `MERGE` | `'merge'` |  |
| `APPEND` | `'append'` |  |
| `MANUAL` | `'manual'` |  |

---

## InboundSyncBulkConfiguration
**Import:** `from omnata_plugin_runtime.configuration import InboundSyncBulkConfiguration`  
**Module:** `omnata_plugin_runtime.configuration.InboundSyncBulkConfiguration`

Provides a way to apply a combination of sync strategy and storage behaviour to all selected streams.
These options will be reduce to the set of supported strategies. If there is no overlap, only CUSTOMIZE will be supported

| Member | Value | Description |
|--------|-------|-------------|
| `AUTO_MERGE` | `'Auto / Merge changes'` |  |
| `AUTO_APPEND` | `'Auto / Keep history'` |  |
| `CUSTOMIZE` | `'Customize - choose sync behaviours for each object'` |  |
| `ALL_FULL_REPLACE` | `'All Objects - Full refresh / Replace'` |  |
| `ALL_FULL_APPEND` | `'All Objects - Full refresh / Append'` |  |
| `ALL_INCR_MERGE` | `'All Objects - Incremental / Merge'` |  |
| `ALL_INCR_APPEND` | `'All Objects - Incremental / Append'` |  |

---

## InboundSyncStrategy
**Import:** `from omnata_plugin_runtime.configuration import InboundSyncStrategy`  
**Module:** `omnata_plugin_runtime.configuration.InboundSyncStrategy`

str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.

| Member | Value | Description |
|--------|-------|-------------|
| `FULL_REFRESH` | `'Full Refresh'` |  |
| `INCREMENTAL` | `'Incremental'` |  |
| `AUTO` | `'Auto'` |  |

---

## InboundSyncStrategyBulkConfiguration
**Import:** `from omnata_plugin_runtime.configuration import InboundSyncStrategyBulkConfiguration`  
**Module:** `omnata_plugin_runtime.configuration.InboundSyncStrategyBulkConfiguration`

Supercedes InboundSyncBulkConfiguration, which was a combination of sync strategy and storage behaviour.

| Member | Value | Description |
|--------|-------|-------------|
| `AUTO` | `'auto'` |  |
| `MANUAL` | `'manual'` |  |

---

## MapperType
**Import:** `from omnata_plugin_runtime.configuration import MapperType`  
**Module:** `omnata_plugin_runtime.configuration.MapperType`

str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.

| Member | Value | Description |
|--------|-------|-------------|
| `FIELD_MAPPING_SELECTOR` | `'field_mapping_selector'` |  |
| `JINJA_TEMPLATE` | `'jinja_template'` |  |

---

## SyncDirection
**Import:** `from omnata_plugin_runtime.configuration import SyncDirection`  
**Module:** `omnata_plugin_runtime.configuration.SyncDirection`

str(object='') -> str
str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.

| Member | Value | Description |
|--------|-------|-------------|
| `INBOUND` | `'inbound'` |  |
| `OUTBOUND` | `'outbound'` |  |

---

# Models

## InboundConfigurationFormPayload
**Import:** `from omnata_plugin_runtime.api import InboundConfigurationFormPayload`  
**Module:** `omnata_plugin_runtime.api.InboundConfigurationFormPayload`

Encapsulates the payload that is sent to the plugin when it is invoked to provide a configuration form for an inbound sync.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `connectivity_option` | `ConnectivityOption` | no | `direct` |  |  |
| `connection_method` | `str` | yes |  |  |  |
| `connection_parameters` | `dict` | yes |  |  |  |
| `oauth_secret_name` | `str` \| None | no | `None` |  |  |
| `other_secrets_name` | `str` \| None | no | `None` |  |  |
| `sync_direction` | `str` | no | `inbound` |  |  |
| `function_name` | `str` | no | `inbound_configuration_form` |  |  |
| `sync_parameters` | `dict` | yes |  |  |  |
| `current_form_parameters` | `dict` \| None | yes |  |  |  |

---

## InboundSyncRequestPayload
**Import:** `from omnata_plugin_runtime.api import InboundSyncRequestPayload`  
**Module:** `omnata_plugin_runtime.api.InboundSyncRequestPayload`

Encapsulates the payload that is sent to the plugin when it is invoked to perform an inbound sync.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `sync_id` | `int` | yes |  |  |  |
| `sync_branch_name` | `str` | no | `main` |  |  |
| `sync_branch_id` | `int` \| None | no | `None` |  |  |
| `connection_id` | `int` | yes |  |  |  |
| `run_id` | `int` | yes |  |  |  |
| `source_app_name` | `str` | yes |  |  |  |
| `results_schema_name` | `str` | yes |  |  |  |
| `results_table_name` | `str` | yes |  |  |  |
| `logging_level` | `str` | yes |  |  |  |
| `connection_method` | `str` | yes |  |  |  |
| `connectivity_option` | `ConnectivityOption` | no | `direct` |  |  |
| `connection_parameters` | `dict` | yes |  |  |  |
| `oauth_secret_name` | `str` \| None | no | `None` |  |  |
| `other_secrets_name` | `str` \| None | no | `None` |  |  |
| `sync_direction` | `str` | no | `inbound` |  |  |
| `sync_parameters` | `dict` | yes |  |  |  |
| `api_limit_overrides` | list[`ApiLimits`] | yes |  |  |  |
| `rate_limits_state` | `dict` | yes |  |  |  |
| `streams_configuration` | `InboundSyncStreamsConfiguration` | yes |  |  |  |
| `latest_stream_state` | `dict` | yes |  |  |  |
| `time_limit_mins` | `int` | no | `240` |  |  |

---

## OutboundConfigurationFormPayload
**Import:** `from omnata_plugin_runtime.api import OutboundConfigurationFormPayload`  
**Module:** `omnata_plugin_runtime.api.OutboundConfigurationFormPayload`

Encapsulates the payload that is sent to the plugin when it is invoked to provide a configuration form for an outbound sync.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `connectivity_option` | `ConnectivityOption` | no | `direct` |  |  |
| `connection_method` | `str` | yes |  |  |  |
| `connection_parameters` | `dict` | yes |  |  |  |
| `oauth_secret_name` | `str` \| None | no | `None` |  |  |
| `other_secrets_name` | `str` \| None | no | `None` |  |  |
| `sync_direction` | `str` | no | `outbound` |  |  |
| `target_type` | `str` \| None | no | `None` |  |  |
| `sync_strategy` | `OutboundSyncStrategy` | yes |  |  |  |
| `function_name` | `str` | no | `outbound_configuration_form` |  |  |
| `sync_parameters` | `dict` | yes |  |  |  |
| `current_form_parameters` | `dict` \| None | yes |  |  |  |

---

## OutboundSyncRequestPayload
**Import:** `from omnata_plugin_runtime.api import OutboundSyncRequestPayload`  
**Module:** `omnata_plugin_runtime.api.OutboundSyncRequestPayload`

Encapsulates the payload that is sent to the plugin when it is invoked to perform an outbound sync.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `sync_id` | `int` | yes |  |  |  |
| `sync_branch_name` | `str` | no | `main` |  |  |
| `sync_branch_id` | `int` \| None | yes |  |  |  |
| `connection_id` | `int` | yes |  |  |  |
| `run_id` | `int` | yes |  |  |  |
| `source_app_name` | `str` | yes |  |  |  |
| `records_schema_name` | `str` | yes |  |  |  |
| `records_table_name` | `str` | yes |  |  |  |
| `results_schema_name` | `str` | yes |  |  |  |
| `results_table_name` | `str` | yes |  |  |  |
| `logging_level` | `str` | yes |  |  |  |
| `connection_method` | `str` | yes |  |  |  |
| `target_type` | `str` \| None | no | `None` |  |  |
| `connectivity_option` | `ConnectivityOption` | no | `direct` |  |  |
| `connection_parameters` | `dict` | yes |  |  |  |
| `oauth_secret_name` | `str` \| None | no | `None` |  |  |
| `other_secrets_name` | `str` \| None | no | `None` |  |  |
| `sync_direction` | `str` | no | `outbound` |  |  |
| `sync_strategy` | `OutboundSyncStrategy` | yes |  |  |  |
| `sync_parameters` | `dict` | yes |  |  |  |
| `api_limit_overrides` | list[`ApiLimits`] | yes |  |  |  |
| `rate_limits_state` | `dict` | yes |  |  |  |
| `field_mappings` | `StoredJinjaTemplate` \| `StoredFieldMappings` \| None | no | `None` |  |  |
| `time_limit_mins` | `int` | no | `240` |  |  |

---

## PluginMessageAbandonedStreams
**Import:** `from omnata_plugin_runtime.api import PluginMessageAbandonedStreams`  
**Module:** `omnata_plugin_runtime.api.PluginMessageAbandonedStreams`

Updates the list of abandoned streams for a sync run

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `message_type` | `str` | no | `abandoned_streams` |  |  |
| `abandoned_streams` | list[`str`] | yes |  |  |  |

---

## PluginMessageCancelledStreams
**Import:** `from omnata_plugin_runtime.api import PluginMessageCancelledStreams`  
**Module:** `omnata_plugin_runtime.api.PluginMessageCancelledStreams`

Updates the list of cancelled streams for a sync run

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `message_type` | `str` | no | `cancelled_streams` |  |  |
| `cancelled_streams` | list[`str`] | yes |  |  |  |

---

## PluginMessageCurrentActivity
**Import:** `from omnata_plugin_runtime.api import PluginMessageCurrentActivity`  
**Module:** `omnata_plugin_runtime.api.PluginMessageCurrentActivity`

A message that is sent to the plugin to update the current activity status of a sync

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `message_type` | `str` | no | `activity` |  |  |
| `current_activity` | `str` | yes |  |  |  |

---

## PluginMessageRateLimitState
**Import:** `from omnata_plugin_runtime.api import PluginMessageRateLimitState`  
**Module:** `omnata_plugin_runtime.api.PluginMessageRateLimitState`

Updates the state of the rate limiting for a connection during a sync run

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `message_type` | `str` | no | `rate_limit_state` |  |  |
| `rate_limit_state` | `dict` | yes |  |  |  |

---

## PluginMessageStreamProgressUpdate
**Import:** `from omnata_plugin_runtime.api import PluginMessageStreamProgressUpdate`  
**Module:** `omnata_plugin_runtime.api.PluginMessageStreamProgressUpdate`

Updates the record counts and completed streams for a sync run

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `message_type` | `str` | no | `stream_record_counts` |  |  |
| `stream_total_counts` | `dict` | yes |  |  |  |
| `completed_streams` | list[`str`] | yes |  |  |  |
| `stream_errors` | `dict` \| None | no | `None` |  |  |
| `total_records_estimate` | `dict` \| None | no | `None` |  |  |

---

## PluginMessageStreamState
**Import:** `from omnata_plugin_runtime.api import PluginMessageStreamState`  
**Module:** `omnata_plugin_runtime.api.PluginMessageStreamState`

Updates the state of the streams for a sync run

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `message_type` | `str` | no | `stream_state` |  |  |
| `stream_state` | `dict` | yes |  |  |  |

---

## ConnectionConfigurationParameters
**Import:** `from omnata_plugin_runtime.configuration import ConnectionConfigurationParameters`  
**Module:** `omnata_plugin_runtime.configuration.ConnectionConfigurationParameters`

Contains user-provided information completed during connection configuration.
This acts as a base class since connection parameters are the first things collected.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `connection_method` | `str` | yes |  |  |  |
| `connectivity_option` | `ConnectivityOption` | no | `direct` |  |  |
| `connection_parameters` | `dict` \| None | no | `None` |  |  |
| `connection_secrets` | `dict` \| None | no | `None` |  |  |
| `ngrok_tunnel_settings` | `NgrokTunnelSettings` \| None | no | `None` |  |  |
| `access_token_secret_name` | `str` \| None | no | `None` |  |  |

---

## CreateSyncAction
**Import:** `from omnata_plugin_runtime.configuration import CreateSyncAction`  
**Module:** `omnata_plugin_runtime.configuration.CreateSyncAction`

The standard Create sync action.
Indicates that a record/object will be created in the target app.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `action_name` | `str` | yes |  |  |  |
| `description` | `str` | yes |  |  |  |
| `custom_action` | `bool` | no | `True` |  |  |

---

## CreateSyncStrategy
**Import:** `from omnata_plugin_runtime.configuration import CreateSyncStrategy`  
**Module:** `omnata_plugin_runtime.configuration.CreateSyncStrategy`

The standard Create sync strategy.
Record creation -> CreateSyncAction

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `description` | `str` | yes |  |  |  |
| `icon_source` | `str` | no | `<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24"><path fill="currentColor" d="m8 18l-6-6l6-6l1.425 1.425l-4.6 4.6L9.4 16.6Zm8 0l-1.425-1.425l4.6-4.6L14.6 7.4L16 6l6 6Z"/></svg>` |  |  |
| `action_on_record_create` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_update` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_delete` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_unchanged` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `custom_strategy` | `bool` | no | `True` |  |  |

---

## DeleteSyncAction
**Import:** `from omnata_plugin_runtime.configuration import DeleteSyncAction`  
**Module:** `omnata_plugin_runtime.configuration.DeleteSyncAction`

The standard Delete sync action.
Indicates that a record/object will be deleted in the target app.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `action_name` | `str` | yes |  |  |  |
| `description` | `str` | yes |  |  |  |
| `custom_action` | `bool` | no | `True` |  |  |

---

## DeleteSyncStrategy
**Import:** `from omnata_plugin_runtime.configuration import DeleteSyncStrategy`  
**Module:** `omnata_plugin_runtime.configuration.DeleteSyncStrategy`

The standard Delete sync strategy.
Record deletion -> DeleteSyncAction

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `description` | `str` | yes |  |  |  |
| `icon_source` | `str` | no | `<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24"><path fill="currentColor" d="m8 18l-6-6l6-6l1.425 1.425l-4.6 4.6L9.4 16.6Zm8 0l-1.425-1.425l4.6-4.6L14.6 7.4L16 6l6 6Z"/></svg>` |  |  |
| `action_on_record_create` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_update` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_delete` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_unchanged` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `custom_strategy` | `bool` | no | `True` |  |  |

---

## InboundSyncConfigurationParameters
**Import:** `from omnata_plugin_runtime.configuration import InboundSyncConfigurationParameters`  
**Module:** `omnata_plugin_runtime.configuration.InboundSyncConfigurationParameters`

Contains user-provided information completed during inbound connection/sync configuration.
If currently_selected_streams is None, return all streams but only include json schema if it's feasible.
If currently_selected_streams is not None, you should return a list of only those streams  with full json schema included.
If json schema is not returned in either of these cases, then the user will not see the fields in the UI and the 
normalized view will look the same as the raw table.
Note that currently_selected_streams only relates to stream listers. When a sync occurs, the InboundSyncRequest includes
the requested streams.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `connection_method` | `str` | yes |  |  |  |
| `connectivity_option` | `ConnectivityOption` | no | `direct` |  |  |
| `connection_parameters` | `dict` \| None | no | `None` |  |  |
| `connection_secrets` | `dict` \| None | no | `None` |  |  |
| `ngrok_tunnel_settings` | `NgrokTunnelSettings` \| None | no | `None` |  |  |
| `access_token_secret_name` | `str` \| None | no | `None` |  |  |
| `sync_parameters` | `dict` \| None | no | `None` |  |  |
| `current_form_parameters` | `dict` \| None | no | `None` |  |  |
| `currently_selected_streams` | list[`str`] \| None | no | `None` |  |  |

---

## InboundSyncStreamsConfiguration
**Import:** `from omnata_plugin_runtime.configuration import InboundSyncStreamsConfiguration`  
**Module:** `omnata_plugin_runtime.configuration.InboundSyncStreamsConfiguration`

Encapsulates the whole value stored under STREAMS_CONFIGURATION. Includes configuration of streams,
as well as which ones were excluded and how to treat newly discovered objects

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `include_new_streams` | `bool` | yes |  |  |  |
| `new_stream_sync_strategy` | `InboundSyncStrategy` \| None | no | `None` |  |  |
| `new_stream_storage_behaviour` | `InboundStorageBehaviour` \| None | no | `None` |  |  |
| `included_streams` | `dict` | yes |  |  |  |
| `excluded_streams` | list[`str`] | yes |  |  |  |
| `bulk_configuration` | `InboundSyncBulkConfiguration` \| None | no | `None` |  |  |
| `sync_strategy_bulk_configuration` | `InboundSyncStrategyBulkConfiguration` \| None | no | `None` |  |  |
| `storage_behaviour_bulk_configuration` | `InboundStorageBehaviourBulkConfiguration` \| None | no | `None` |  |  |

---

## MirrorSyncStrategy
**Import:** `from omnata_plugin_runtime.configuration import MirrorSyncStrategy`  
**Module:** `omnata_plugin_runtime.configuration.MirrorSyncStrategy`

The standard Mirror sync strategy.
Record creation -> CreateSyncAction
Record update -> UpdateSyncAction
Record delete -> DeleteSyncAction

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `description` | `str` | yes |  |  |  |
| `icon_source` | `str` | no | `<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24"><path fill="currentColor" d="m8 18l-6-6l6-6l1.425 1.425l-4.6 4.6L9.4 16.6Zm8 0l-1.425-1.425l4.6-4.6L14.6 7.4L16 6l6 6Z"/></svg>` |  |  |
| `action_on_record_create` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_update` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_delete` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_unchanged` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `custom_strategy` | `bool` | no | `True` |  |  |

---

## NetworkAddresses
**Import:** `from omnata_plugin_runtime.configuration import NetworkAddresses`  
**Module:** `omnata_plugin_runtime.configuration.NetworkAddresses`

Represents a mix of direct access and privatelink addresses

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `direct` | list[`str`] \| None | no | `None` |  | A list of addresses that can be accessed directly |
| `privatelink` | list[`str`] \| None | no | `None` |  | A list of addresses that require privatelink access |

---

## NgrokTunnelSettings
**Import:** `from omnata_plugin_runtime.configuration import NgrokTunnelSettings`  
**Module:** `omnata_plugin_runtime.configuration.NgrokTunnelSettings`

Stores connection information for ngrok tunnels.
Retrieved from the connection configuration parameters/secrets.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `endpoint_host` | `str` | yes |  |  | The ngrok endpoint (x.ngrok.app) |
| `endpoint_port` | `int` | no | `443` |  | The ngrok endpoint port |
| `client_certificate` | `str` | yes |  |  | The ngrok client certificate, in PEM format |
| `client_key` | `str` | yes |  |  | The ngrok client key, in PEM format |

---

## OutboundRecordTransformationParameters
**Import:** `from omnata_plugin_runtime.configuration import OutboundRecordTransformationParameters`  
**Module:** `omnata_plugin_runtime.configuration.OutboundRecordTransformationParameters`

Allows the plugin author to determine how records are transformed before being sent to the target app.
Since conversion to objects causes a loss of some data types (e.g. timestamps and dates become strings),
and different Snowflake accounts may have different timestamp output formats, specifying the format allows
for a consistent result in the transformed records.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `timestamp_tz_format` | `str` | no | `YYYY-MM-DD HH24:MI:SS.FF3 TZHTZM` |  |  |
| `timestamp_ntz_format` | `str` | no | `YYYY-MM-DD HH24:MI:SS.FF3` |  |  |
| `timestamp_ltz_format` | `str` | no | `YYYY-MM-DD HH24:MI:SS.FF3 TZHTZM` |  |  |
| `date_format` | `str` | no | `YYYY-MM-DD` |  |  |

---

## OutboundSyncAction
**Import:** `from omnata_plugin_runtime.configuration import OutboundSyncAction`  
**Module:** `omnata_plugin_runtime.configuration.OutboundSyncAction`

Base class for Outbound Sync Actions.
Describes what action will be taken by the plugin with a particular record.
These actions are linked to via sync strategies in response to a record create/update/delete.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `action_name` | `str` | yes |  |  |  |
| `description` | `str` | yes |  |  |  |
| `custom_action` | `bool` | no | `True` |  |  |

---

## OutboundSyncConfigurationParameters
**Import:** `from omnata_plugin_runtime.configuration import OutboundSyncConfigurationParameters`  
**Module:** `omnata_plugin_runtime.configuration.OutboundSyncConfigurationParameters`

Contains user-provided information completed during outbound connection/sync configuration.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `connection_method` | `str` | yes |  |  |  |
| `connectivity_option` | `ConnectivityOption` | no | `direct` |  |  |
| `connection_parameters` | `dict` \| None | no | `None` |  |  |
| `connection_secrets` | `dict` \| None | no | `None` |  |  |
| `ngrok_tunnel_settings` | `NgrokTunnelSettings` \| None | no | `None` |  |  |
| `access_token_secret_name` | `str` \| None | no | `None` |  |  |
| `sync_parameters` | `dict` \| None | no | `None` |  |  |
| `current_form_parameters` | `dict` \| None | no | `None` |  |  |
| `target_type` | `str` \| None | no | `None` |  | The label of the OutboundTargetType selected by the user |
| `sync_strategy` | `OutboundSyncStrategy` \| None | no | `None` |  |  |
| `field_mappings` | `StoredJinjaTemplate` \| `StoredFieldMappings` \| None | no | `None` |  |  |

---

## OutboundSyncStrategy
**Import:** `from omnata_plugin_runtime.configuration import OutboundSyncStrategy`  
**Module:** `omnata_plugin_runtime.configuration.OutboundSyncStrategy`

OutboundSyncStrategy is a base class for all outbound sync strategies.
Each implementation decides on what pattern of record changes it needs to observe.
For each type of record change, an OutboundSyncAction describes what it will do in the target app.

Custom OutboundSyncStrategies can be devised, which provide for use cases beyond applying records
and publishing events.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `description` | `str` | yes |  |  |  |
| `icon_source` | `str` | no | `<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24"><path fill="currentColor" d="m8 18l-6-6l6-6l1.425 1.425l-4.6 4.6L9.4 16.6Zm8 0l-1.425-1.425l4.6-4.6L14.6 7.4L16 6l6 6Z"/></svg>` |  |  |
| `action_on_record_create` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_update` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_delete` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_unchanged` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `custom_strategy` | `bool` | no | `True` |  |  |

---

## OutboundTargetParameter
**Import:** `from omnata_plugin_runtime.configuration import OutboundTargetParameter`  
**Module:** `omnata_plugin_runtime.configuration.OutboundTargetParameter`

Accomodates testing outbound syncs in production by nominating a form field who's value stays in the branch.
The reason this information is set statically here instead of as a flag on the FormField, is so that the sync engine 
can have this information readily available without calling the plugin.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `field_name` | `str` | yes |  |  |  |
| `is_branching_toggle` | `bool` | yes |  |  |  |
| `label` | `str` | yes |  |  |  |

---

## OutboundTargetType
**Import:** `from omnata_plugin_runtime.configuration import OutboundTargetType`  
**Module:** `omnata_plugin_runtime.configuration.OutboundTargetType`

Some products have APIs that can be grouped together in ways that support different strategies and may or may not support toggling.
The label should answer the question: "What would you like to sync to?"
Examples:
- A CRM system may have "Standard objects", "Custom objects" or "Events"
- A messaging platform may have "Channels", "Users" or "Messages"
- A marketing platform may have "Customer lists", "Campaigns" or "Automations"
- An Ad platform may have "Campaigns", "Ad groups" or "Ads"
The target type cannot be changed after the sync is created.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `label` | `str` | yes |  |  |  |
| `supported_strategies` | list[`str`] | yes |  |  |  |
| `target_parameter` | `OutboundTargetParameter` \| None | no | `None` |  |  |

---

## RecreateSyncAction
**Import:** `from omnata_plugin_runtime.configuration import RecreateSyncAction`  
**Module:** `omnata_plugin_runtime.configuration.RecreateSyncAction`

The standard Recreate sync action.
Similar to the Create action, but indicates that all existing records in the app will be replaced by these.
If a sync strategy uses this sync action, it doesn't make sense to include any other actions.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `action_name` | `str` | yes |  |  |  |
| `description` | `str` | yes |  |  |  |
| `custom_action` | `bool` | no | `True` |  |  |

---

## ReplaceSyncStrategy
**Import:** `from omnata_plugin_runtime.configuration import ReplaceSyncStrategy`  
**Module:** `omnata_plugin_runtime.configuration.ReplaceSyncStrategy`

The standard Replace sync strategy.
This is a special strategy that means all records that currently exist will be recreated each sync.
Record creation -> RecreateSyncAction
Record update -> RecreateSyncAction
Record unchanged -> RecreateSyncAction

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `description` | `str` | yes |  |  |  |
| `icon_source` | `str` | no | `<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24"><path fill="currentColor" d="m8 18l-6-6l6-6l1.425 1.425l-4.6 4.6L9.4 16.6Zm8 0l-1.425-1.425l4.6-4.6L14.6 7.4L16 6l6 6Z"/></svg>` |  |  |
| `action_on_record_create` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_update` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_delete` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_unchanged` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `custom_strategy` | `bool` | no | `True` |  |  |

---

## SendSyncAction
**Import:** `from omnata_plugin_runtime.configuration import SendSyncAction`  
**Module:** `omnata_plugin_runtime.configuration.SendSyncAction`

The standard Send sync action.
Indicates that a record/object will be sent to the target app. This action is typically
used in event-style applications, to indicate that the action is more of a message than a record operation.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `action_name` | `str` | yes |  |  |  |
| `description` | `str` | yes |  |  |  |
| `custom_action` | `bool` | no | `True` |  |  |

---

## SendSyncStrategy
**Import:** `from omnata_plugin_runtime.configuration import SendSyncStrategy`  
**Module:** `omnata_plugin_runtime.configuration.SendSyncStrategy`

The standard Send sync strategy.
Record creation -> SendSyncAction

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `description` | `str` | yes |  |  |  |
| `icon_source` | `str` | no | `<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24"><path fill="currentColor" d="m8 18l-6-6l6-6l1.425 1.425l-4.6 4.6L9.4 16.6Zm8 0l-1.425-1.425l4.6-4.6L14.6 7.4L16 6l6 6Z"/></svg>` |  |  |
| `action_on_record_create` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_update` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_delete` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_unchanged` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `custom_strategy` | `bool` | no | `True` |  |  |

---

## StoredConfigurationValue
**Import:** `from omnata_plugin_runtime.configuration import StoredConfigurationValue`  
**Module:** `omnata_plugin_runtime.configuration.StoredConfigurationValue`

A configuration value that was provided by a user (to configure a sync or connection).
It contains only a string value and optionally some metadata, all of the display-related properties are discarded

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `value` | `str` | yes |  |  | The stored value |
| `metadata` | `dict` | no |  |  | Metadata associated with the value |

---

## StoredFieldMapping
**Import:** `from omnata_plugin_runtime.configuration import StoredFieldMapping`  
**Module:** `omnata_plugin_runtime.configuration.StoredFieldMapping`

A column->field mapping value that was provided by a user when configuring a sync.
The source can either be a column name (e.g. EMAIL_ADDRESS) or an expression (e.g. CONTACT_DETAILS:email_address::varchar or FIRST_NAME||' '||LAST_NAME))

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `source_type` | `str` | yes |  |  |  |
| `source_value` | `str` | yes |  |  |  |
| `app_field` | `str` | yes |  |  |  |
| `app_metadata` | `dict` | no |  |  |  |

---

## StoredFieldMappings
**Import:** `from omnata_plugin_runtime.configuration import StoredFieldMappings`  
**Module:** `omnata_plugin_runtime.configuration.StoredFieldMappings`

Mapping information that was provided by a user (to configure a sync or connection).
It contains either a list of mappings or a jinja template

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `mapper_type` | `str` | no | `field_mapping_selector` |  |  |
| `field_mappings` | list[`StoredFieldMapping`] | yes |  |  |  |

---

## StoredJinjaTemplate
**Import:** `from omnata_plugin_runtime.configuration import StoredJinjaTemplate`  
**Module:** `omnata_plugin_runtime.configuration.StoredJinjaTemplate`

Mapping information that was provided by a user (to configure a sync or connection).
It contains either a list of mappings or a jinja template

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `mapper_type` | `str` | no | `jinja_template` |  |  |
| `additional_column_expressions` | `dict` | no | `{}` |  |  |
| `jinja_template` | `str` | yes |  |  |  |

---

## StoredStreamConfiguration
**Import:** `from omnata_plugin_runtime.configuration import StoredStreamConfiguration`  
**Module:** `omnata_plugin_runtime.configuration.StoredStreamConfiguration`

Encapsulates all of the configuration necessary to sync an inbound stream.
This information is parsed from the metadata of the streams Sync config object, for convenience.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `stream_name` | `str` | yes |  |  |  |
| `sync_strategy` | `InboundSyncStrategy` | yes |  |  |  |
| `cursor_field` | `str` \| None | no | `None` |  | The field to use as a cursor |
| `primary_key_field` | `str` \| list[`str`] \| None | no | `None` |  | The field(s) that will be used as primary key. |
| `storage_behaviour` | `InboundStorageBehaviour` | yes |  |  |  |
| `stream` | `StreamConfiguration` | yes |  |  |  |
| `latest_state` | `dict` | no |  |  | The latest state of the stream, used for incremental syncs |

---

## StreamConfiguration
**Import:** `from omnata_plugin_runtime.configuration import StreamConfiguration`  
**Module:** `omnata_plugin_runtime.configuration.StreamConfiguration`

Encapsulates all of the configuration necessary to sync an inbound stream.
Derived from the Airbyte protocol, with minor tweaks to suit our differences.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `stream_name` | `str` | yes |  |  |  |
| `supported_sync_strategies` | list[`InboundSyncStrategy`] | yes |  |  |  |
| `source_defined_cursor` | `bool` \| None | no | `None` |  | If true, the plugin controls the cursor field |
| `source_defined_primary_key` | `str` \| list[`str`] \| None | no | `None` |  | If defined, the plugin controls the primary key field |
| `primary_key_can_be_composite` | `bool` \| None | no | `False` |  | If true, the primary key can be composite |
| `default_cursor_field` | `str` \| None | no | `None` |  | The default field to use as a cursor |
| `json_schema` | `dict` \| None | no | `None` |  | JSON Schema for objects provided by stream |
| `metadata` | `dict` | no |  |  | Metadata associated with the stream. Be careful not to include environment-specific information like GUIDs |
| `depends_on_stream` | `str` \| None | no | `None` |  | Marks the stream as requiring another stream to be selected |
| `mandatory` | `bool` | no | `False` |  | Marks the stream as mandatory, meaning it cannot be excluded from the sync configuration |

---

## SubscriptableBaseModel
**Import:** `from omnata_plugin_runtime.configuration import SubscriptableBaseModel`  
**Module:** `omnata_plugin_runtime.configuration.SubscriptableBaseModel`

Extends the Pydantic BaseModel to make it subscriptable

*No fields defined.*

---

## SyncConfigurationParameters
**Import:** `from omnata_plugin_runtime.configuration import SyncConfigurationParameters`  
**Module:** `omnata_plugin_runtime.configuration.SyncConfigurationParameters`

A base class for Sync configuration parameters.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `connection_method` | `str` | yes |  |  |  |
| `connectivity_option` | `ConnectivityOption` | no | `direct` |  |  |
| `connection_parameters` | `dict` \| None | no | `None` |  |  |
| `connection_secrets` | `dict` \| None | no | `None` |  |  |
| `ngrok_tunnel_settings` | `NgrokTunnelSettings` \| None | no | `None` |  |  |
| `access_token_secret_name` | `str` \| None | no | `None` |  |  |
| `sync_parameters` | `dict` \| None | no | `None` |  |  |
| `current_form_parameters` | `dict` \| None | no | `None` |  |  |

---

## SyncScheduleDbt
**Import:** `from omnata_plugin_runtime.configuration import SyncScheduleDbt`  
**Module:** `omnata_plugin_runtime.configuration.SyncScheduleDbt`

A sync schedule which runs when initiated during a dbt run, using the Omnata dbt package.

Args:
    dbt_prod_target_name (str): The name of the dbt target used for production runs
    task_warehouse_dbt_defined (bool): If true, the dbt package will set the schedule settings
    warehouse (str): The Snowflake warehouse which this task uses. If task_warehouse_dbt_defined is True, this is only an initial default before the first run occurs
    time_limit_mins (int): The maximum time the sync can run for before being cancelled
    dbt_dev_target_name (str): The name of the dbt target used by developers outside of CI
    dbt_sync_model_name (str): The name of the dbt model used to run the sync
    dbt_source_model_name (str): The name of the dbt model used as a source for the run, if the sync is Outbound. This will be resolved at runtime and replaces the configured source table
    is_dbt_cloud (bool): If true, dbt cloud is in use

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `mode` | `str` | no | `dbt` |  |  |
| `dbt_prod_target_name` | `str` | no | `prod` |  |  |
| `task_warehouse_dbt_defined` | `bool` | no | `True` |  |  |
| `warehouse` | `str` \| None | no | `None` |  |  |
| `time_limit_mins` | `int` | no | `240` |  |  |
| `dbt_dev_target_name` | `str` | no | `dev` |  |  |
| `dbt_sync_model_name` | `str` | yes |  |  |  |
| `dbt_source_model_name` | `str` \| None | no | `None` |  |  |
| `is_dbt_cloud` | `bool` | no | `True` |  |  |

---

## SyncScheduleDependant
**Import:** `from omnata_plugin_runtime.configuration import SyncScheduleDependant`  
**Module:** `omnata_plugin_runtime.configuration.SyncScheduleDependant`

A sync schedule which runs the sync at the same time or after another sync.

Args:
    run_when (Literal["after_parent_completes","at_same_time_as"]): Determines if this sync runs at the same time as the parent, or after it completes
    warehouse (str): The Snowflake warehouse which this task uses
    time_limit_mins (int): The maximum time the sync can run for before being cancelled
    selected_sync (int): The sync ID of the sync to depend on

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `mode` | `str` | no | `dependent` |  |  |
| `run_when` | `str` | no | `after_parent_completes` |  |  |
| `warehouse` | `str` \| None | no | `None` |  |  |
| `time_limit_mins` | `int` | no | `240` |  |  |
| `selected_sync` | `int` | yes |  |  |  |

---

## SyncScheduleManual
**Import:** `from omnata_plugin_runtime.configuration import SyncScheduleManual`  
**Module:** `omnata_plugin_runtime.configuration.SyncScheduleManual`

A sync schedule which runs only when manually requested.

Args:
    warehouse (str): The Snowflake warehouse which this task uses
    time_limit_mins (int): The maximum time the sync can run for before being cancelled

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `mode` | `str` | no | `manual` |  |  |
| `warehouse` | `str` \| None | no | `None` |  |  |
| `time_limit_mins` | `int` | no | `240` |  |  |

---

## SyncScheduleSnowflakeTask
**Import:** `from omnata_plugin_runtime.configuration import SyncScheduleSnowflakeTask`  
**Module:** `omnata_plugin_runtime.configuration.SyncScheduleSnowflakeTask`

A sync schedule which uses Snowflake tasks to initiate runs.

Args:
    sync_frequency (str): The cron expression for this schedule
    sync_frequency_name (str): The plain english name for this cron schedule
    warehouse (str): The Snowflake warehouse which this task uses
    time_limit_mins (int): The maximum time the sync can run for before being cancelled
    daily_hour (Optional[int]): If the sync frequency is Daily, the hour it runs
    daily_minute (Optional[int]): If the sync frequency is Daily, the minute it runs
    minute_of_hour (Optional[int]): If the sync frequency is Hourly, the minute of the hour it runs

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `mode` | `str` | no | `snowflake_task` |  |  |
| `sync_frequency` | `str` | yes |  |  |  |
| `sync_frequency_name` | `str` | yes |  |  |  |
| `warehouse` | `str` \| None | no | `None` |  |  |
| `time_limit_mins` | `int` | no | `240` |  |  |
| `daily_hour` | `int` \| None | no | `None` |  |  |
| `daily_minute` | `int` \| None | no | `None` |  |  |
| `minute_of_hour` | `int` \| None | no | `None` |  |  |

---

## UpdateSyncAction
**Import:** `from omnata_plugin_runtime.configuration import UpdateSyncAction`  
**Module:** `omnata_plugin_runtime.configuration.UpdateSyncAction`

The standard Update sync action.
Indicates that a record/object will be updated in the target app.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `action_name` | `str` | yes |  |  |  |
| `description` | `str` | yes |  |  |  |
| `custom_action` | `bool` | no | `True` |  |  |

---

## UpdateSyncStrategy
**Import:** `from omnata_plugin_runtime.configuration import UpdateSyncStrategy`  
**Module:** `omnata_plugin_runtime.configuration.UpdateSyncStrategy`

The standard Update sync strategy, designed for applying updates to records which already exist in the remote.
Record create -> UpdateSyncAction
Record update -> UpdateSyncAction

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `description` | `str` | yes |  |  |  |
| `icon_source` | `str` | no | `<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24"><path fill="currentColor" d="m8 18l-6-6l6-6l1.425 1.425l-4.6 4.6L9.4 16.6Zm8 0l-1.425-1.425l4.6-4.6L14.6 7.4L16 6l6 6Z"/></svg>` |  |  |
| `action_on_record_create` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_update` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_delete` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_unchanged` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `custom_strategy` | `bool` | no | `True` |  |  |

---

## UpsertSyncStrategy
**Import:** `from omnata_plugin_runtime.configuration import UpsertSyncStrategy`  
**Module:** `omnata_plugin_runtime.configuration.UpsertSyncStrategy`

The standard Upsert sync strategy.
Record creation -> CreateSyncAction
Record update -> UpdateSyncAction

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `description` | `str` | yes |  |  |  |
| `icon_source` | `str` | no | `<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24"><path fill="currentColor" d="m8 18l-6-6l6-6l1.425 1.425l-4.6 4.6L9.4 16.6Zm8 0l-1.425-1.425l4.6-4.6L14.6 7.4L16 6l6 6Z"/></svg>` |  |  |
| `action_on_record_create` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_update` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_delete` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `action_on_record_unchanged` | `OutboundSyncAction` \| None | no | `None` |  |  |
| `custom_strategy` | `bool` | no | `True` |  |  |

---

## ConfigurationFormBase
**Import:** `from omnata_plugin_runtime.forms import ConfigurationFormBase`  
**Module:** `omnata_plugin_runtime.forms.ConfigurationFormBase`

Defines a form for configuring a sync. Includes zero or more form fields.

:param List[FormFieldBase] fields: A list of fields to display to the user
    :return: nothing

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `fields` | list[`FormInputField` \| `FormTextAreaField` \| `FormSshKeypair` \| `FormX509Certificate` \| `FormGpgKeypair` \| `FormRadioField` \| `FormCheckboxField` \| `FormSliderField` \| `FormDropdownField` \| `InformationField` \| `InformationBoxField` \| `FormSnowflakeStageField`] | yes |  |  |  |

---

## ConnectionMethod
**Import:** `from omnata_plugin_runtime.forms import ConnectionMethod`  
**Module:** `omnata_plugin_runtime.forms.ConnectionMethod`

Defines a method of connecting to an application.
:param str data_source: The name of the connection method, e.g. "OAuth", "API Key", "Credentials"
:param List[FormFieldBase] fields: A list of fields that are used to collect the connection information from the user.
:param Optional[SecurityIntegrationTemplate] oauth_template: If provided, the user will be guided through the process
of creating a security integration, followed by a secret and performing the OAuth flow. Once this secret is completed,
the rest of the values from the form will be captured and then the connection will be tested.
:param str description: A markdown description of the connection method, which will be displayed to the user.
    This should be concise as it will be displayed in a sidebar, but you can include a link to the connection section
    of the plugin's documentation.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `fields` | list[`FormInputField` \| `FormTextAreaField` \| `FormSshKeypair` \| `FormX509Certificate` \| `FormGpgKeypair` \| `FormRadioField` \| `FormCheckboxField` \| `FormSliderField` \| `FormDropdownField` \| `InformationField` \| `InformationBoxField` \| `FormSnowflakeStageField`] | yes |  |  |  |
| `oauth_template` | `SecurityIntegrationTemplateAuthorizationCode` \| `SecurityIntegrationTemplateClientCredentials` \| None | no | `None` |  |  |
| `ngrok_tunnel_configuration` | `NGrokMTLSTunnel` \| None | no | `None` |  |  |
| `description` | `str` | no | `` |  |  |

---

## DynamicFormOptionsDataSource
**Import:** `from omnata_plugin_runtime.forms import DynamicFormOptionsDataSource`  
**Module:** `omnata_plugin_runtime.forms.DynamicFormOptionsDataSource`

A Data Source for providing a set of form options that load dynamically from the server

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `source_function` | `str` | yes |  |  |  |
| `new_option_creator` | `NewOptionCreator` \| None | no | `None` |  |  |
| `type` | `str` | no | `dynamic` |  |  |

---

## FormCheckboxField
**Import:** `from omnata_plugin_runtime.forms import FormCheckboxField`  
**Module:** `omnata_plugin_runtime.forms.FormCheckboxField`

A field which presents a checkbox

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `label` | `str` | yes |  |  |  |
| `default_value` | `bool` | no | `False` |  |  |
| `required` | `bool` | no | `False` |  |  |
| `secret` | `bool` | no | `False` |  |  |
| `depends_on` | `str` \| None | no | `None` |  |  |
| `help_text` | `str` | no | `` |  |  |
| `reload_on_change` | `bool` | no | `False` |  |  |
| `type` | `str` | no | `checkbox` |  |  |

---

## FormDropdownField
**Import:** `from omnata_plugin_runtime.forms import FormDropdownField`  
**Module:** `omnata_plugin_runtime.forms.FormDropdownField`

A field which presents a dropdown list of options

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `data_source` | `StaticFormOptionsDataSource` \| `DynamicFormOptionsDataSource` | yes |  |  |  |
| `name` | `str` | yes |  |  |  |
| `label` | `str` | yes |  |  |  |
| `default_value` | `str` \| None | no | `None` |  |  |
| `required` | `bool` | no | `False` |  |  |
| `secret` | `bool` | no | `False` |  |  |
| `depends_on` | `str` \| None | no | `None` |  |  |
| `help_text` | `str` | no | `` |  |  |
| `reload_on_change` | `bool` | no | `False` |  |  |
| `type` | `str` | no | `dropdown` |  |  |
| `multi_select` | `bool` | no | `False` |  |  |

---

## FormFieldMappingSelector
**Import:** `from omnata_plugin_runtime.forms import FormFieldMappingSelector`  
**Module:** `omnata_plugin_runtime.forms.FormFieldMappingSelector`

Uses a visual column->field mapper, to allow the user to define how source columns map to app fields

:param FormOptionsDataSourceBase data_source: A data source which provides the app field options
:param str depends_on: Provide the name of another field to make it dependant, so that the mapper won't display until a value has been provided
:return: nothing

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `data_source` | `StaticFormOptionsDataSource` \| `DynamicFormOptionsDataSource` | yes |  |  |  |
| `mapper_type` | `str` | no | `field_mapping_selector` |  |  |
| `label` | `str` | no | `Field Mappings` |  |  |
| `depends_on` | `str` \| None | no | `None` |  |  |

---

## FormFieldWithDataSource
**Import:** `from omnata_plugin_runtime.forms import FormFieldWithDataSource`  
**Module:** `omnata_plugin_runtime.forms.FormFieldWithDataSource`

Denotes that the field uses a data source

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `data_source` | `StaticFormOptionsDataSource` \| `DynamicFormOptionsDataSource` | yes |  |  |  |

---

## FormGpgKeypair
**Import:** `from omnata_plugin_runtime.forms import FormGpgKeypair`  
**Module:** `omnata_plugin_runtime.forms.FormGpgKeypair`

An GPG Keypair field, which generates public and private GPG keys for asymmetric cryptography.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `label` | `str` | yes |  |  |  |
| `default_value` | `str` \| None | no | `None` |  |  |
| `required` | `bool` | no | `False` |  |  |
| `depends_on` | `str` \| None | no | `None` |  |  |
| `help_text` | `str` | no | `` |  |  |
| `local_side` | `str` | no | `public` |  |  |
| `allow_user_provided` | `bool` | no | `True` |  |  |
| `type` | `str` | no | `gpg_keypair` |  |  |
| `secret` | `bool` | no | `True` |  |  |

---

## FormInputField
**Import:** `from omnata_plugin_runtime.forms import FormInputField`  
**Module:** `omnata_plugin_runtime.forms.FormInputField`

An input field, which collects a single line of free-form text from the user and no metadata.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `label` | `str` | yes |  |  |  |
| `default_value` | `str` \| `bool` | no | `` |  |  |
| `required` | `bool` | no | `False` |  |  |
| `depends_on` | `str` \| None | no | `None` |  |  |
| `help_text` | `str` | no | `` |  |  |
| `reload_on_change` | `bool` | no | `False` |  |  |
| `secret` | `bool` | no | `False` |  |  |
| `type` | `str` | no | `input` |  |  |

---

## FormJinjaTemplate
**Import:** `from omnata_plugin_runtime.forms import FormJinjaTemplate`  
**Module:** `omnata_plugin_runtime.forms.FormJinjaTemplate`

Uses text area to allow the user to create a template, which can include column values from the source

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `mapper_type` | `str` | no | `jinja_template` |  |  |
| `label` | `str` | no | `Jinja Template` |  |  |
| `depends_on` | `str` \| None | no | `None` |  |  |

---

## FormOption
**Import:** `from omnata_plugin_runtime.forms import FormOption`  
**Module:** `omnata_plugin_runtime.forms.FormOption`

An option used by certain form forms (like Dropdowns).

:param str value: The value to set in the field if this option is selected
:param str label: The label to show in the list. This value is not stored.
:param dict metadata: An arbitrary dictionary to store with the value, which can be retrieved by the plugin
:param bool required: When populating field mapping options, this flag indicates that this field is mandatory
:param bool unique: When populating field mapping options, this flag indicates that this field requires a unique value (i.e. be mapped from a unique column)
:param bool default: Indicates that this option should be the default selected
:param bool disabled: Indicates that the option should appear in the list, but be unselectable
:param str data_type_icon: The data type icon to show next to the option (where applicable)
:return: nothing

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `value` | `str` | yes |  |  |  |
| `label` | `str` | yes |  |  |  |
| `metadata` | `dict` | no |  |  |  |
| `required` | `bool` | no | `False` |  |  |
| `unique` | `bool` | no | `False` |  |  |
| `default` | `bool` | no | `False` |  |  |
| `disabled` | `bool` | no | `False` |  |  |
| `data_type_icon` | `str` | no | `unknown` |  |  |

---

## FormRadioField
**Import:** `from omnata_plugin_runtime.forms import FormRadioField`  
**Module:** `omnata_plugin_runtime.forms.FormRadioField`

A field which presents a set of radio options
:param str name: The name of the form field. This value must be unique, and is used to retrieve the value from within the plugin code.
:param str label: The label for the form field
:param FormOptionsDataSourceBase data_source provides the values for the radio group
:param str default_value: The default value presented initially in the field
:param bool required: If True, means that the form cannot be submitted without a value present
:param str depends_on: The name of another form field. If provided, this form field will not be rendered until there is a value in the field it depends on.
:param str help_text: A longer description of what the field is used for. If provided, a help icon is shown and must be hovered over to display this text.
:param bool reload_on_change: If True, the entire form is reloaded after the value is changed. This is used to conditionally render fields based on values provided in others, but should be used only when strictly necessary.
:return: nothing

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `data_source` | `StaticFormOptionsDataSource` \| `DynamicFormOptionsDataSource` | yes |  |  |  |
| `name` | `str` | yes |  |  |  |
| `label` | `str` | yes |  |  |  |
| `default_value` | `str` \| None | no | `None` |  |  |
| `required` | `bool` | no | `False` |  |  |
| `secret` | `bool` | no | `False` |  |  |
| `depends_on` | `str` \| None | no | `None` |  |  |
| `help_text` | `str` | no | `` |  |  |
| `reload_on_change` | `bool` | no | `False` |  |  |
| `type` | `str` | no | `radio` |  |  |

---

## FormSliderField
**Import:** `from omnata_plugin_runtime.forms import FormSliderField`  
**Module:** `omnata_plugin_runtime.forms.FormSliderField`

A field which presents a slider

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `label` | `str` | yes |  |  |  |
| `default_value` | `str` \| `int` \| None | no | `None` |  |  |
| `secret` | `bool` | no | `False` |  |  |
| `required` | `bool` | no | `False` |  |  |
| `depends_on` | `str` \| None | no | `None` |  |  |
| `help_text` | `str` | no | `` |  |  |
| `reload_on_change` | `bool` | no | `False` |  |  |
| `type` | `str` | no | `slider` |  |  |
| `min_value` | `int` | no | `0` |  |  |
| `max_value` | `int` | no | `100` |  |  |
| `step_size` | `int` | no | `1` |  |  |

---

## FormSnowflakeStageField
**Import:** `from omnata_plugin_runtime.forms import FormSnowflakeStageField`  
**Module:** `omnata_plugin_runtime.forms.FormSnowflakeStageField`

A field which represents a stage which can be selected from a list shared to the plugin.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `label` | `str` | yes |  |  |  |
| `default_value` | `str` \| `bool` | no | `` |  |  |
| `required` | `bool` | no | `False` |  |  |
| `depends_on` | `str` \| None | no | `None` |  |  |
| `help_text` | `str` | no | `` |  |  |
| `reload_on_change` | `bool` | no | `False` |  |  |
| `secret` | `bool` | no | `False` |  |  |
| `type` | `str` | no | `snowflake_stage` |  |  |

---

## FormSshKeypair
**Import:** `from omnata_plugin_runtime.forms import FormSshKeypair`  
**Module:** `omnata_plugin_runtime.forms.FormSshKeypair`

An SSH Keypair field, which generates public and private keys for asymmetric cryptography.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `label` | `str` | yes |  |  |  |
| `default_value` | `str` \| None | no | `None` |  |  |
| `required` | `bool` | no | `False` |  |  |
| `depends_on` | `str` \| None | no | `None` |  |  |
| `help_text` | `str` | no | `` |  |  |
| `local_side` | `str` | no | `public` |  |  |
| `allow_user_provided` | `bool` | no | `True` |  |  |
| `type` | `str` | no | `ssh_keypair` |  |  |
| `secret` | `bool` | no | `True` |  |  |

---

## FormTextAreaField
**Import:** `from omnata_plugin_runtime.forms import FormTextAreaField`  
**Module:** `omnata_plugin_runtime.forms.FormTextAreaField`

A text area field, which collects multi-line free-form text from the user and no metadata.

:param str name: The name of the form field. This value must be unique, and is used to retrieve the value from within the plugin code.
:param str label: The label for the form field
:param str default_value: The default value presented initially in the field
:param bool required: If True, means that the form cannot be submitted without a value present
:param str depends_on: The name of another form field. If provided, this form field will not be rendered until there is a value in the field it depends on.
:param str help_text: A longer description of what the field is used for. If provided, a help icon is shown and must be hovered over to display this text.
:param bool secret: Indicates that the text entered must be masked in the browser, and stored/access securely
:param bool reload_on_change: If True, the entire form is reloaded after the value is changed. This is used to conditionally render fields based on values provided in others, but should be used only when strictly necessary.
:return: nothing

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `label` | `str` | yes |  |  |  |
| `default_value` | `str` | no | `` |  |  |
| `secret` | `bool` | no | `False` |  |  |
| `required` | `bool` | no | `False` |  |  |
| `depends_on` | `str` \| None | no | `None` |  |  |
| `help_text` | `str` | no | `` |  |  |
| `reload_on_change` | `bool` | no | `False` |  |  |
| `type` | `str` | no | `textarea` |  |  |
| `variables` | `bool` | no | `False` |  |  |

---

## FormX509Certificate
**Import:** `from omnata_plugin_runtime.forms import FormX509Certificate`  
**Module:** `omnata_plugin_runtime.forms.FormX509Certificate`

An X509 certificate in PEM format.
Like a textarea field, except it decodes and shows information about the certificate.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `label` | `str` | yes |  |  |  |
| `default_value` | `str` \| None | no | `None` |  |  |
| `required` | `bool` | no | `False` |  |  |
| `depends_on` | `str` \| None | no | `None` |  |  |
| `help_text` | `str` | no | `` |  |  |
| `type` | `str` | no | `x509_certificate` |  |  |
| `secret` | `bool` | no | `True` |  |  |

---

## InboundSyncConfigurationForm
**Import:** `from omnata_plugin_runtime.forms import InboundSyncConfigurationForm`  
**Module:** `omnata_plugin_runtime.forms.InboundSyncConfigurationForm`

Defines a form for configuring an inbound sync, prior to stream selection.
The form values provided via these fields are passed into the inbound_list_streams function.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `fields` | list[`FormInputField` \| `FormTextAreaField` \| `FormSshKeypair` \| `FormX509Certificate` \| `FormGpgKeypair` \| `FormRadioField` \| `FormCheckboxField` \| `FormSliderField` \| `FormDropdownField` \| `InformationField` \| `InformationBoxField` \| `FormSnowflakeStageField`] | no |  |  |  |

---

## InformationBoxField
**Import:** `from omnata_plugin_runtime.forms import InformationBoxField`  
**Module:** `omnata_plugin_runtime.forms.InformationBoxField`

A field which allows information to be displayed to the user, but not edited.
This variant renders it inside a box, with an icon and a different background colour.

:param str name: The name of the form field. This value must be unique.
:param str markdown_content: The markdown to include.
:param str box_type: The type of box to render. One of "info", "warning", "error"
:param str box_icon: The name of the icon to render in the box. If not provided, no icon will be used.
:return: nothing

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `markdown_content` | `str` | yes |  |  |  |
| `depends_on` | `str` \| None | no | `None` |  |  |
| `type` | `str` | no | `information_box` |  |  |
| `reload_on_change` | `bool` | no | `False` |  |  |
| `box_type` | `str` | no | `info` |  |  |
| `box_icon` | `str` \| None | no | `None` |  |  |
| `secret` | `bool` | no | `False` |  |  |

---

## InformationField
**Import:** `from omnata_plugin_runtime.forms import InformationField`  
**Module:** `omnata_plugin_runtime.forms.InformationField`

A field which allows information to be displayed to the user in plain markdown, but not edited.

:param str name: The name of the form field. This value must be unique.
:param str markdown_content: The markdown to include.
:return: nothing

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `markdown_content` | `str` | yes |  |  |  |
| `depends_on` | `str` \| None | no | `None` |  |  |
| `type` | `str` | no | `information` |  |  |
| `reload_on_change` | `bool` | no | `False` |  |  |
| `secret` | `bool` | no | `False` |  |  |

---

## NGrokMTLSTunnel
**Import:** `from omnata_plugin_runtime.forms import NGrokMTLSTunnel`  
**Module:** `omnata_plugin_runtime.forms.NGrokMTLSTunnel`

Designates a ConnectionMethod as connecting via an ngrok tunnel.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `SupportEdgeTermination` | `bool` | no | `True` |  |  |
| `post_tunnel_fields_function` | `str` | yes |  |  |  |

---

## NewOptionCreator
**Import:** `from omnata_plugin_runtime.forms import NewOptionCreator`  
**Module:** `omnata_plugin_runtime.forms.NewOptionCreator`

Allows for options to be added to a datasource by the user.
It does this by presenting the user with a form, then building a StoredConfigurationValue from the provided values.
Since this StoredConfigurationValue won't be present in the data source (at least not initially), there is
also a function (construct_form_option) to convert the StoredConfigurationValue into a FormOption which can be added to the data source.
This means that all the presentation options (e.g. required, unique) must be derivable from the metadata in StoredConfigurationValue.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `creation_form_function` | `str` | yes |  |  |  |
| `creation_complete_function` | `str` | yes |  |  |  |
| `construct_form_option` | `str` | yes |  |  |  |
| `allow_create` | `bool` | no | `True` |  |  |

---

## OutboundSyncConfigurationForm
**Import:** `from omnata_plugin_runtime.forms import OutboundSyncConfigurationForm`  
**Module:** `omnata_plugin_runtime.forms.OutboundSyncConfigurationForm`

Defines a form for configuring an outbound sync.
Includes the zero or more form fields from the base class, and optionally a column->field mapper
to map Snowflake columns to app fields/payloads.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `fields` | list[`FormInputField` \| `FormTextAreaField` \| `FormSshKeypair` \| `FormX509Certificate` \| `FormGpgKeypair` \| `FormRadioField` \| `FormCheckboxField` \| `FormSliderField` \| `FormDropdownField` \| `InformationField` \| `InformationBoxField` \| `FormSnowflakeStageField`] | yes |  |  |  |
| `mapper` | `FormFieldMappingSelector` \| `FormJinjaTemplate` \| None | no | `None` |  |  |

---

## SecurityIntegrationTemplateAuthorizationCode
**Import:** `from omnata_plugin_runtime.forms import SecurityIntegrationTemplateAuthorizationCode`  
**Module:** `omnata_plugin_runtime.forms.SecurityIntegrationTemplateAuthorizationCode`

Provides values used to populate a security integration instructions template, which
in turn allows the customer to create an OAuth based secret object

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `oauth_docs_url` | `str` \| None | no | `None` |  |  |
| `oauth_grant` | `str` | no | `authorization_code` |  |  |
| `oauth_client_id` | `str` | no | `<client id>` |  |  |
| `oauth_client_secret` | `str` | no | `<client secret>` |  |  |
| `oauth_token_endpoint` | `str` | no | `<token endpoint>` |  |  |
| `oauth_authorization_endpoint` | `str` | no | `<authorization endpoint>` |  |  |
| `oauth_allowed_scopes` | list[`str`] | no | `[]` |  |  |

---

## SecurityIntegrationTemplateClientCredentials
**Import:** `from omnata_plugin_runtime.forms import SecurityIntegrationTemplateClientCredentials`  
**Module:** `omnata_plugin_runtime.forms.SecurityIntegrationTemplateClientCredentials`

Provides values used to populate a security integration instructions template, which
in turn allows the customer to create an OAuth based secret object

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `oauth_docs_url` | `str` \| None | no | `None` |  |  |
| `oauth_grant` | `str` | no | `client_credentials` |  |  |
| `oauth_client_id` | `str` | no | `<client id>` |  |  |
| `oauth_client_secret` | `str` | no | `<client secret>` |  |  |
| `oauth_token_endpoint` | `str` | no | `<token endpoint>` |  |  |
| `oauth_allowed_scopes` | list[`str`] | no | `[]` |  |  |

---

## StaticFormOptionsDataSource
**Import:** `from omnata_plugin_runtime.forms import StaticFormOptionsDataSource`  
**Module:** `omnata_plugin_runtime.forms.StaticFormOptionsDataSource`

A Data Source for providing a static set of form options

:param List[FormOption] values: The list of values to return
:param NewOptionCreator new_option_creator: If provided, it means that values can be added to the datasource via the provided mechanism
:return: nothing

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `values` | list[`FormOption`] | no |  |  |  |
| `new_option_creator` | `NewOptionCreator` \| None | no | `None` |  |  |
| `type` | `str` | no | `static` |  |  |

---

## FullyQualifiedTable
**Import:** `from omnata_plugin_runtime.json_schema import FullyQualifiedTable`  
**Module:** `omnata_plugin_runtime.json_schema.FullyQualifiedTable`

Represents a fully qualified table name in Snowflake, including database, schema, and table name.
This is not a template, it's a fully specified object.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `database_name` | `str` \| None | no | `None` |  | The database name |
| `schema_name` | `str` | yes |  |  | The schema name |
| `table_name` | `str` | yes |  |  | The table name |

---

## JsonSchemaProperty
**Import:** `from omnata_plugin_runtime.json_schema import JsonSchemaProperty`  
**Module:** `omnata_plugin_runtime.json_schema.JsonSchemaProperty`

The most basic common properties for a JSON schema property, plus the extra ones we use for providing Snowflake-specific information.
Used mainly to do partial parsing as we extract fields from within the schema

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `type` | `str` \| list[`str`] \| None | yes |  |  | The type of the property |
| `$ref` | `str` \| None | no | `None` |  | The reference to another schema |
| `nullable` | `bool` | no | `True` |  | Whether the property is nullable |
| `description` | `str` \| None | no | `None` |  | The description of the property |
| `format` | `str` \| None | no | `None` |  | The format of the property, e.g. date-time |
| `properties` | `dict` \| None | no | `None` |  | The sub-properties of the property, if the property is an object type |
| `snowflakeTimestampType` | `str` \| None | no | `None` |  | The Snowflake timestamp type to use when interpreting a date-time string. |
| `snowflakeTimestampFormat` | `str` \| None | no | `None` |  | The Snowflake timestamp format to use when interpreting a date-time string. |
| `snowflakePrecision` | `int` \| None | no | `None` |  | The Snowflake precision to assign to the column. |
| `snowflakeScale` | `int` \| None | no | `None` |  | The Snowflake scale to assign to the column. |
| `snowflakeColumnExpression` | `str` \| None | no | `None` |  | When advanced processing is needed, you can provide a value here. Use {{variant_path}} to interpolate the path to the JSON field. |
| `isJoinColumn` | `bool` \| None | no | `False` |  | Whether this column is sourced from a joined stream |
| `requiredStreamNames` | list[`str`] \| None | no | `None` |  | The names of the streams that are depended upon by this column, via joins. If these streams are not selected, the column will be omitted. |
| `referencedFields` | `dict` \| None | no | `None` |  | The names of fields that are referenced by this field, keyed on the stream name (or None if it's the current stream). This is used to order the fields, and also to cascade the removal of unsupported fields (e.g. in formulas). |

---

## JsonSchemaTopLevel
**Import:** `from omnata_plugin_runtime.json_schema import JsonSchemaTopLevel`  
**Module:** `omnata_plugin_runtime.json_schema.JsonSchemaTopLevel`

This model is used as a starting point for parsing a JSON schema.
It does not validate the whole thing up-front, as there is some complex recursion as well as external configuration.
Instead, it takes the basic properties and then allows for further parsing on demand.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `description` | `str` \| None | no | `None` |  | The description of the schema |
| `joins` | list[`SnowflakeViewJoin`] \| None | no | `None` |  | The joins to include in the view |
| `properties` | `dict` \| None | no | `None` |  | The properties of the schema. This is left as a dictionary, and parsed on demand. |

---

## SnowflakeViewColumn
**Import:** `from omnata_plugin_runtime.json_schema import SnowflakeViewColumn`  
**Module:** `omnata_plugin_runtime.json_schema.SnowflakeViewColumn`

Represents everything needed to express a column in a Snowflake normalized view.
The name is the column name, the expression is the SQL expression to use in the view.
In other words, the column definition is "expression as name".

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `original_name` | `str` | yes |  |  | The name of the column before the column naming transformation is applied |
| `expression` | `str` | yes |  |  |  |
| `comment` | `str` \| None | no | `None` |  |  |
| `is_join_column` | `bool` \| None | no | `False` |  | Whether this column is sourced from a joined stream |
| `required_stream_names` | list[`str`] \| None | no | `None` |  | The names of the streams that are depended upon by this column, via joins. If these streams are not selected, the column will be omitted |
| `referenced_columns` | `dict` \| None | no | `None` |  | The names of columns that are referenced by this column, keyed on the stream name (or None if it's the current stream). This is used to order the columns, and also to cascade the removal of unsupported columns (e.g. in formulas). |

---

## SnowflakeViewJoin
**Import:** `from omnata_plugin_runtime.json_schema import SnowflakeViewJoin`  
**Module:** `omnata_plugin_runtime.json_schema.SnowflakeViewJoin`

Represents a join in a Snowflake normalized view.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `left_alias` | `str` | yes |  |  | The alias to use on the left side of the join |
| `left_column` | `str` | yes |  |  | The column to join on from the left side |
| `join_stream_name` | `str` | yes |  |  | The name of the stream to join (right side) |
| `join_stream_alias` | `str` | yes |  |  | The alias to use for the joined stream, this is used in the column definitions instead of the stream name, and accomodates the possibility of multiple joins to the same stream |
| `join_stream_column` | `str` | yes |  |  | The column to join on from the right side |

---

## SnowflakeViewPart
**Import:** `from omnata_plugin_runtime.json_schema import SnowflakeViewPart`  
**Module:** `omnata_plugin_runtime.json_schema.SnowflakeViewPart`

Represents a stream within a normalized view.
Because a normalized view can be built from multiple streams, this is potentially only part of the view.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `stream_name` | `str` | yes |  |  | The name of the stream |
| `raw_table_location` | `FullyQualifiedTable` | yes |  |  | The location of the raw table that the stream is sourced from |
| `comment` | `str` \| None | no | `None` |  | The comment to assign to the view |
| `columns` | list[`SnowflakeViewColumn`] | yes |  |  | The columns to include in the view |
| `joins` | list[`SnowflakeViewJoin`] | yes |  |  | The joins to include in the view |

---

## SnowflakeViewParts
**Import:** `from omnata_plugin_runtime.json_schema import SnowflakeViewParts`  
**Module:** `omnata_plugin_runtime.json_schema.SnowflakeViewParts`

Represents a set of streams within a normalized view.
This is the top level object that represents the whole view.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `main_part` | `SnowflakeViewPart` | yes |  |  | The main part of the view, which is the stream that the view is named after |
| `joined_parts` | list[`SnowflakeViewPart`] | yes |  |  | The other streams that are joined to the main stream |

---

## ConnectResponse
**Import:** `from omnata_plugin_runtime.omnata_plugin import ConnectResponse`  
**Module:** `omnata_plugin_runtime.omnata_plugin.ConnectResponse`

Encapsulates the response to a connection request. This is used to pass back any additional
information that may be discovered during connection that's relevant to the plugin (e.g. Account Identifiers).
You can also specifies any additional network addresses that are needed to connect to the app, that might not
have been known until the connection was made.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `connection_parameters` | `dict` | no | `{}` |  |  |
| `connection_secrets` | `dict` | no | `{}` |  |  |
| `network_addresses` | list[`str`] \| `NetworkAddresses` | no | `[]` |  |  |

---

## DailyBillingEventRequest
**Import:** `from omnata_plugin_runtime.omnata_plugin import DailyBillingEventRequest`  
**Module:** `omnata_plugin_runtime.omnata_plugin.DailyBillingEventRequest`

Represents a request to provide billing events for that day.
These will occur at midnight, and cover the previous 24 hours.
Provides enough information for the plugin to create billing events for the day.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `billing_schedule` | `str` | no | `DAILY` |  |  |
| `billable_connections_inbound` | `int` | no | `0` |  |  |
| `billable_connections_outbound` | `int` | no | `0` |  |  |
| `ngrok_connections_inbound` | `int` | no | `0` |  |  |
| `ngrok_connections_outbound` | `int` | no | `0` |  |  |
| `has_active_inbound` | `bool` | no | `False` |  |  |
| `has_active_outbound` | `bool` | no | `False` |  |  |

---

## MonthlyBillingEventRequest
**Import:** `from omnata_plugin_runtime.omnata_plugin import MonthlyBillingEventRequest`  
**Module:** `omnata_plugin_runtime.omnata_plugin.MonthlyBillingEventRequest`

Represents a request to provide billing events for that month.
These will occur at midnight on the first of each month, and cover the whole previous month.
Currently, these exist to provide a way to bill for the number of active ngrok connections
and associated data overages.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `billing_schedule` | `str` | no | `MONTHLY` |  |  |
| `distinct_active_ngrok_connections` | `int` | no | `0` |  |  |
| `ngrok_data_usage_bytes` | `int` | no | `0` |  |  |
| `has_active_inbound` | `bool` | no | `False` |  |  |
| `has_active_outbound` | `bool` | no | `False` |  |  |
| `billable_connections_inbound` | `int` | no | `0` |  |  |
| `billable_connections_outbound` | `int` | no | `0` |  |  |

---

## PluginInfo
**Import:** `from omnata_plugin_runtime.omnata_plugin import PluginInfo`  
**Module:** `omnata_plugin_runtime.omnata_plugin.PluginInfo`

Manifest plus other derived information about a plugin which is determined during upload.
:param str manifest: The manifest from the plugin's code
:param List[str] anaconda_packages: A list of anaconda packages required by the plugin
:param List[str] bundled_packages: A list of bundled packages required by the plugin
:param str icon_source: The base64 encoded icon for the plugin
:param str plugin_class_name: The name of the plugin class
:param bool has_custom_validator: Whether or not the plugin has a custom validator
:param str plugin_runtime_version: The version of the Omnata plugin runtime that the current version of the plugin was built against
:param str tier: The tier of the plugin. 
    Setting this to 'byo' means that the plugin is internally developed or a free community plugin. The sync engine does not bill for the first plugin of this type, nor are billing events created for it.
    Setting this to 'partner' means that the plugin was developed and distributed by a partner. 
    All other values only carry meaning for Omnata plugins, to indicate which iconography to apply within the application.
:param str package_source: Whether the plugin is packaged as a function or a stage
:param List[UDFDefinition] consumer_udfs: A list of UDFs that the plugin exposes to consumers
:param List[UDTFDefinition] consumer_udtfs: A list of UDTFs that the plugin exposes to consumers

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `manifest` | `PluginManifest` | yes |  |  |  |
| `anaconda_packages` | list[`str`] | yes |  |  |  |
| `bundled_packages` | list[`str`] | yes |  |  |  |
| `icon_source` | `str` \| None | no | `None` |  |  |
| `plugin_class_name` | `str` | yes |  |  |  |
| `has_custom_validator` | `bool` | yes |  |  |  |
| `plugin_runtime_version` | `str` | yes |  |  |  |
| `plugin_devkit_version` | `str` | no | `unknown` |  |  |
| `tier` | `str` | yes |  |  |  |
| `package_source` | `str` | yes |  |  |  |
| `consumer_udfs` | list[`UDFDefinition`] | no |  |  |  |
| `consumer_udtfs` | list[`UDTFDefinition`] | no |  |  |  |

---

## PluginManifest
**Import:** `from omnata_plugin_runtime.omnata_plugin import PluginManifest`  
**Module:** `omnata_plugin_runtime.omnata_plugin.PluginManifest`

Constructs a Plugin Manifest, which identifies the application, describes how it can work, and defines any runtime code dependancies.
    :param str plugin_id: A short, string identifier for the application, a combination of lowercase alphanumeric and underscores, e.g. "google_sheets"
    :param str plugin_name: A descriptive name for the application, e.g. "Google Sheets"
    :param str developer_id: A short, string identifier for the developer, a combination of lowercase alphanumeric and underscores, e.g. "acme_corp"
    :param str developer_name: A descriptive name for the developer, e.g. "Acme Corp"
    :param str docs_url: The URL where plugin documentation can be found, e.g. "https://docs.omnata.com"
    :param bool supports_inbound: A flag to indicate whether or not the plugin supports inbound sync. Support for inbound sync behaviours (full/incremental) is defined per inbound stream.
    :param List[OutboundSyncStrategy] supported_outbound_strategies: A list of sync strategies that the plugin can support, e.g. create,upsert.
    :param List[ConnectivityOption] supported_connectivity_options: A list of connectivity options that the plugin can support, e.g. direct,ngrok,privatelink
    :param str timestamp_tz_format: The format to use when converting TIMESTAMP_TZ values to strings in the transformed record.
    :param str timestamp_ntz_format: The format to use when converting TIMESTAMP_NTZ values to strings in the transformed record.
    :param str timestamp_ltz_format: The format to use when converting TIMESTAMP_LTZ values to strings in the transformed record.
    For each of the above three formats, you can include "{{precision}}" to substitute the precision of the timestamp, if that matters.
    For example, "YYYY-MM-DDTHH24:MI:SS.FF{{precision}}TZHTZM" would be a valid format string.
    :param str date_format: The format to use when converting DATE values to strings in the transformed record.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `plugin_id` | `str` | yes |  |  |  |
| `plugin_name` | `str` | yes |  |  |  |
| `developer_id` | `str` | yes |  |  |  |
| `developer_name` | `str` | yes |  |  |  |
| `docs_url` | `str` | yes |  |  |  |
| `supports_inbound` | `bool` | yes |  |  |  |
| `supported_outbound_strategies` | list[`OutboundSyncStrategy`] | yes |  |  |  |
| `supported_connectivity_options` | list[`ConnectivityOption`] | no |  |  |  |
| `outbound_target_types` | list[`OutboundTargetType`] \| None | no | `None` |  |  |
| `outbound_target_transformation_parameters` | `OutboundRecordTransformationParameters` | no |  |  |  |

---

## SnowflakeBillingEvent
**Import:** `from omnata_plugin_runtime.omnata_plugin import SnowflakeBillingEvent`  
**Module:** `omnata_plugin_runtime.omnata_plugin.SnowflakeBillingEvent`

The inputs to Snowflake's SYSTEM$CREATE_BILLING_EVENT function.
See https://docs.snowflake.com/en/sql-reference/functions/system_create_billing_event

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `billing_class` | `str` | yes |  |  |  |
| `base_charge` | `float` \| `str` | yes |  |  |  |
| `timestamp` | `str` | no | `2026-04-22T06:57:32.102612Z` |  |  |
| `sub_class` | `str` \| None | no | `None` |  |  |
| `start_timestamp` | `str` \| None | no | `None` |  |  |
| `objects` | list[`str`] | no | `[]` |  |  |
| `additional_info` | `dict` | no | `{}` |  |  |

---

## SnowflakeFunctionParameter
**Import:** `from omnata_plugin_runtime.omnata_plugin import SnowflakeFunctionParameter`  
**Module:** `omnata_plugin_runtime.omnata_plugin.SnowflakeFunctionParameter`

Represents a parameter for a Snowflake UDF or UDTF

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `description` | `str` | yes |  |  |  |
| `data_type` | `str` | yes |  |  |  |
| `default_value_clause` | `str` \| None | no | `None` |  |  |

---

## SnowflakeUDTFResultColumn
**Import:** `from omnata_plugin_runtime.omnata_plugin import SnowflakeUDTFResultColumn`  
**Module:** `omnata_plugin_runtime.omnata_plugin.SnowflakeUDTFResultColumn`

Represents a result column for a Snowflake UDTF

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `data_type` | `str` | yes |  |  |  |

---

## UDFDefinition
**Import:** `from omnata_plugin_runtime.omnata_plugin import UDFDefinition`  
**Module:** `omnata_plugin_runtime.omnata_plugin.UDFDefinition`

The information needed by the plugin uploader to put a Python UDF definition into the setup script.
Do not use this class directly in plugins, instead use the omnata_udf decorator.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `language` | `str` | yes |  |  |  |
| `runtime_version` | `str` | yes |  |  |  |
| `description` | `str` | yes |  |  |  |
| `params` | list[`SnowflakeFunctionParameter`] | yes |  |  |  |
| `result_data_type` | `str` | yes |  |  |  |
| `handler` | `str` | yes |  |  |  |
| `expose_to_consumer` | `bool` | yes |  |  |  |
| `imports` | list[`str`] \| None | no | `None` |  |  |
| `packages` | list[`str`] \| None | no | `None` |  |  |

---

## UDTFDefinition
**Import:** `from omnata_plugin_runtime.omnata_plugin import UDTFDefinition`  
**Module:** `omnata_plugin_runtime.omnata_plugin.UDTFDefinition`

The information needed by the plugin uploader to put a Python UDTF definition into the setup script.
Do not use this class directly in plugins, instead use the omnata_udtf decorator.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | `str` | yes |  |  |  |
| `language` | `str` | yes |  |  |  |
| `runtime_version` | `str` | yes |  |  |  |
| `description` | `str` | yes |  |  |  |
| `params` | list[`SnowflakeFunctionParameter`] | yes |  |  |  |
| `result_columns` | list[`SnowflakeUDTFResultColumn`] | yes |  |  |  |
| `handler` | `str` | yes |  |  |  |
| `expose_to_consumer` | `bool` | yes |  |  |  |
| `imports` | list[`str`] \| None | no | `None` |  |  |
| `packages` | list[`str`] \| None | no | `None` |  |  |

---

## ApiLimits
**Import:** `from omnata_plugin_runtime.rate_limiting import ApiLimits`  
**Module:** `omnata_plugin_runtime.rate_limiting.ApiLimits`

Encapsulates the constraints imposed by an app's APIs

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `endpoint_category` | `str` | no | `All endpoints` |  | the name of the API category (e.g. "Data loading endpoints") |
| `request_matchers` | list[`HttpRequestMatcher`] | no | `[{'http_methods': ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'], 'url_regex': '.*'}]` |  | a list of request matchers. If None is provided, all requests will be matched |
| `request_rates` | list[`RequestRateLimit`] | no | `None` |  | imposes time delays between requests to stay under a defined rate limit |

---

## HttpRequestMatcher
**Import:** `from omnata_plugin_runtime.rate_limiting import HttpRequestMatcher`  
**Module:** `omnata_plugin_runtime.rate_limiting.HttpRequestMatcher`

A class used to match an HTTP request

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `http_methods` | list[`str`] | yes |  |  |  |
| `url_regex` | `str` | yes |  |  |  |

---

## RateLimitState
**Import:** `from omnata_plugin_runtime.rate_limiting import RateLimitState`  
**Module:** `omnata_plugin_runtime.rate_limiting.RateLimitState`

Encapsulates the rate limiting state of an endpoint category for a particular connection (as opposed to configuration)
Importantly, we are very strict on all timestamps being timezone aware and UTC.
Accuracy is critical for these calculations, so we raise errors early to ensure that we're not making mistakes.

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `wait_until` | `str` \| None | no | `None` |  | Providing a value here means that no requests should occur until a specific moment in the future |
| `previous_request_timestamps` | list[`str`] \| None | no | `[]` |  | A list of timestamps where previous requests have been made, used to calculate the next request time |

---

## RequestRateLimit
**Import:** `from omnata_plugin_runtime.rate_limiting import RequestRateLimit`  
**Module:** `omnata_plugin_runtime.rate_limiting.RequestRateLimit`

Request rate limits
    Defined as a request count, time unit and number of units e.g. (1,"second",5) = 1 request per 5 seconds, or (100, "minute", 15) = 100 requests per 15 minutes

| Field | Type | Required | Default | Constraints | Description |
|-------|------|----------|---------|-------------|-------------|
| `request_count` | `int` | yes |  |  |  |
| `time_unit` | `str` | yes |  |  |  |
| `unit_count` | `int` | yes |  |  |  |

---
