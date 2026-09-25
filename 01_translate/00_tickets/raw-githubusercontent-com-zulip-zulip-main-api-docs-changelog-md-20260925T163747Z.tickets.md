snapshot: raw-githubusercontent-com-zulip-zulip-main-api-docs-changelog-md-20260925T163747Z.txt
sha256: 47d9577c38a16505a31f59678ba39e2f1b33aba2a64fedfd6072aef70add360e
source_url: https://raw.githubusercontent.com/zulip/zulip/main/api_docs/changelog.md
body_range: 21-129
line_numbers: snapshot

## Ticket 1

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The undocumented `PATCH /users/me/subscriptions` endpoint for | 25 | * The undocumented `PATCH /users/me/subscriptions` endpoint for |
| affected_surface | `PATCH /users/me/subscriptions` | 25 | * The undocumented `PATCH /users/me/subscriptions` endpoint for |
| affected_surface | `POST /users/me/subscriptions` | 28 | ([`POST /users/me/subscriptions`](/api/subscribe)) and |
| affected_surface | `DELETE /users/me/subscriptions` | 29 | bulk-unsubscribe ([`DELETE /users/me/subscriptions`](/api/unsubscribe)) |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | endpoints, which clients should use to subscribe/unsubscribe | 30 | endpoints, which clients should use to subscribe/unsubscribe |
| source | https://raw.githubusercontent.com/zulip/zulip/main/api_docs/changelog.md raw-githubusercontent-com-zulip-zulip-main-api-docs-changelog-md-20260925T163747Z.txt | 25-31 |  |

## Ticket 2

| field | value | line | quote |
| --- | --- | --- | --- |
| change | [`POST /messages/{message_id}/report`](/api/report-message): This endpoint | 35 | * [`POST /messages/{message_id}/report`](/api/report-message): This endpoint |
| affected_surface | `POST /messages/{message_id}/report` | 35 | * [`POST /messages/{message_id}/report`](/api/report-message): This endpoint |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/zulip/zulip/main/api_docs/changelog.md raw-githubusercontent-com-zulip-zulip-main-api-docs-changelog-md-20260925T163747Z.txt | 35-37 |  |

## Ticket 3

| field | value | line | quote |
| --- | --- | --- | --- |
| change | [`GET /events`](/api/get-events), [`GET /messages`](/api/get-messages), | 41 | * [`GET /events`](/api/get-events), [`GET /messages`](/api/get-messages), |
| affected_surface | `GET /events` | 41 | * [`GET /events`](/api/get-events), [`GET /messages`](/api/get-messages), |
| affected_surface | `GET /messages` | 41 | * [`GET /events`](/api/get-events), [`GET /messages`](/api/get-messages), |
| affected_surface | `GET /messages/{message_id}` | 42 | [`GET /messages/{message_id}`](/api/get-message), |
| affected_surface | `POST /messages/flags` | 43 | [`POST /messages/flags`](/api/update-message-flags), |
| affected_surface | `POST /messages/flags/narrow` | 44 | [`POST /messages/flags/narrow`](/api/update-message-flags-for-narrow): |
| affected_surface | `hide_link_previews` | 45 | Added `hide_link_previews` as a supported [message |
| affected_surface | `flags` | 49 | appears in the message's `flags` array and in `update_message_flags` |
| affected_surface | `update_message_flags` | 49 | appears in the message's `flags` array and in `update_message_flags` |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | When set, clients should hide auto-generated | 47 | toggled by the user. When set, clients should hide auto-generated |
| source | https://raw.githubusercontent.com/zulip/zulip/main/api_docs/changelog.md raw-githubusercontent-com-zulip-zulip-main-api-docs-changelog-md-20260925T163747Z.txt | 41-51 |  |

## Ticket 4

| field | value | line | quote |
| --- | --- | --- | --- |
| change | [`PATCH /messages/{message_id}`](/api/update-message): Fixed a bug where | 55 | * [`PATCH /messages/{message_id}`](/api/update-message): Fixed a bug where |
| affected_surface | `PATCH /messages/{message_id}` | 55 | * [`PATCH /messages/{message_id}`](/api/update-message): Fixed a bug where |
| affected_surface | `stream_id` | 56 | passing the `stream_id` that the message is already in was processed as |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/zulip/zulip/main/api_docs/changelog.md raw-githubusercontent-com-zulip-zulip-main-api-docs-changelog-md-20260925T163747Z.txt | 55-57 |  |

## Ticket 5

| field | value | line | quote |
| --- | --- | --- | --- |
| change | [`POST /messages`](/api/send-message): Added `message_url` and | 61 | * [`POST /messages`](/api/send-message): Added `message_url` and |
| affected_surface | `POST /messages` | 61 | * [`POST /messages`](/api/send-message): Added `message_url` and |
| affected_surface | `message_url` | 61 | * [`POST /messages`](/api/send-message): Added `message_url` and |
| affected_surface | `message_link` | 62 | `message_link` fields to the response. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/zulip/zulip/main/api_docs/changelog.md raw-githubusercontent-com-zulip-zulip-main-api-docs-changelog-md-20260925T163747Z.txt | 61-62 |  |

## Ticket 6

| field | value | line | quote |
| --- | --- | --- | --- |
| change | [`POST /users/me/subscriptions`](/api/subscribe), | 66 | * [`POST /users/me/subscriptions`](/api/subscribe), |
| affected_surface | `POST /users/me/subscriptions` | 66 | * [`POST /users/me/subscriptions`](/api/subscribe), |
| affected_surface | `POST /channels/create` | 67 | [`POST /channels/create`](/api/create-channel), |
| affected_surface | `PATCH /streams/{stream_id}` | 68 | [`PATCH /streams/{stream_id}`](/api/update-stream): Added |
| affected_surface | `default_push_notifications` | 69 | `default_push_notifications` boolean parameter that controls whether |
| affected_surface | boolean | 69 | `default_push_notifications` boolean parameter that controls whether |
| affected_surface | this | 75 | modify this parameter. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/zulip/zulip/main/api_docs/changelog.md raw-githubusercontent-com-zulip-zulip-main-api-docs-changelog-md-20260925T163747Z.txt | 66-75 |  |

## Ticket 7

| field | value | line | quote |
| --- | --- | --- | --- |
| change | [`POST /register`](/api/register-queue), [`GET /events`](/api/get-events), | 77 | * [`POST /register`](/api/register-queue), [`GET /events`](/api/get-events), |
| affected_surface | `POST /register` | 77 | * [`POST /register`](/api/register-queue), [`GET /events`](/api/get-events), |
| affected_surface | `GET /events` | 77 | * [`POST /register`](/api/register-queue), [`GET /events`](/api/get-events), |
| affected_surface | `GET /streams` | 78 | [`GET /streams`](/api/get-streams), |
| affected_surface | `GET /streams/{stream_id}` | 79 | [`GET /streams/{stream_id}`](/api/get-stream-by-id): Added |
| affected_surface | `default_push_notifications` | 80 | `default_push_notifications` boolean field to channel objects, which |
| affected_surface | boolean | 80 | `default_push_notifications` boolean field to channel objects, which |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/zulip/zulip/main/api_docs/changelog.md raw-githubusercontent-com-zulip-zulip-main-api-docs-changelog-md-20260925T163747Z.txt | 77-85 |  |

## Ticket 8

| field | value | line | quote |
| --- | --- | --- | --- |
| change | [`GET /export/realm`](/api/get-realm-exports), | 89 | * [`GET /export/realm`](/api/get-realm-exports), |
| affected_surface | `GET /export/realm` | 89 | * [`GET /export/realm`](/api/get-realm-exports), |
| affected_surface | `GET /events` | 90 | [`GET /events`](/api/get-events): Added an `export_from_prior_server` |
| affected_surface | `export_from_prior_server` | 90 | [`GET /events`](/api/get-events): Added an `export_from_prior_server` |
| affected_surface | boolean | 91 | boolean field to the export objects returned. It is `true` |
| affected_surface | `true` | 91 | boolean field to the export objects returned. It is `true` |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | This change was also backported to the Zulip 12.x | 94 | on this server. This change was also backported to the Zulip 12.x |
| effective_date | series, at feature level 499. | 95 | series, at feature level 499. |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/zulip/zulip/main/api_docs/changelog.md raw-githubusercontent-com-zulip-zulip-main-api-docs-changelog-md-20260925T163747Z.txt | 89-95 |  |

## Ticket 9

| field | value | line | quote |
| --- | --- | --- | --- |
| change | [`DELETE /export/realm/{export_id}`](/api/delete-realm-export): Export | 96 | * [`DELETE /export/realm/{export_id}`](/api/delete-realm-export): Export |
| affected_surface | `DELETE /export/realm/{export_id}` | 96 | * [`DELETE /export/realm/{export_id}`](/api/delete-realm-export): Export |
| affected_surface | `export_from_prior_server` | 97 | records with the `export_from_prior_server` field set to `true` cannot |
| affected_surface | `true` | 97 | records with the `export_from_prior_server` field set to `true` cannot |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | change was also backported to the Zulip 12.x series, at feature level 499. | 99 | change was also backported to the Zulip 12.x series, at feature level 499. |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/zulip/zulip/main/api_docs/changelog.md raw-githubusercontent-com-zulip-zulip-main-api-docs-changelog-md-20260925T163747Z.txt | 96-99 |  |

## Ticket 10

| field | value | line | quote |
| --- | --- | --- | --- |
| change | [`PATCH /messages/{message_id}`](/api/update-message): For requests with | 103 | * [`PATCH /messages/{message_id}`](/api/update-message): For requests with |
| affected_surface | `PATCH /messages/{message_id}` | 103 | * [`PATCH /messages/{message_id}`](/api/update-message): For requests with |
| affected_surface | `"propagate_mode": "change_all"` | 104 | `"propagate_mode": "change_all"` from users who are not administrators |
| affected_surface | `"code": "MOVE_MESSAGES_TIME_LIMIT_EXCEEDED"` | 105 | or moderators, the `"code": "MOVE_MESSAGES_TIME_LIMIT_EXCEEDED"` error |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/zulip/zulip/main/api_docs/changelog.md raw-githubusercontent-com-zulip-zulip-main-api-docs-changelog-md-20260925T163747Z.txt | 103-108 |  |

## Ticket 11

| field | value | line | quote |
| --- | --- | --- | --- |
| change | [`POST /register`](/api/register-queue), [`GET /events`](/api/get-events): | 112 | * [`POST /register`](/api/register-queue), [`GET /events`](/api/get-events): |
| affected_surface | `POST /register` | 112 | * [`POST /register`](/api/register-queue), [`GET /events`](/api/get-events): |
| affected_surface | `GET /events` | 112 | * [`POST /register`](/api/register-queue), [`GET /events`](/api/get-events): |
| affected_surface | `require_e2ee_push_notifications` | 113 | The `require_e2ee_push_notifications` realm setting, when enabled, |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | 12.x series, at feature level 500. | 116 | 12.x series, at feature level 500. |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/zulip/zulip/main/api_docs/changelog.md raw-githubusercontent-com-zulip-zulip-main-api-docs-changelog-md-20260925T163747Z.txt | 112-116 |  |

## Ticket 12

| field | value | line | quote |
| --- | --- | --- | --- |
| change | [Message formatting](/api/message-formatting): The global time | 120 | * [Message formatting](/api/message-formatting): The global time |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/zulip/zulip/main/api_docs/changelog.md raw-githubusercontent-com-zulip-zulip-main-api-docs-changelog-md-20260925T163747Z.txt | 120-121 |  |

## Unmapped

- 21: ## Changes in Zulip 13.0
- 23: **Feature level 512**
- 26:   updating channel subscriptions has been deprecated and
- 27:   removed. It was a duplicate of the documented bulk-subscribe
- 31:   users from channels.
- 33: **Feature level 511**
- 36:   now returns an error if the message report fails to be sent to the
- 37:   moderation request channel.
- 39: **Feature level 510**
- 46:   flag](/api/update-message-flags#available-flags) that can be
- 48:   link previews on the message for that user. Like other flags, it
- 50:   events. The flag can be set on any message, whether or not it
- 51:   currently has a link preview.
- 53: **Feature level 509**
- 57:   a channel move.
- 59: **Feature level 508**
- 64: **Feature level 507**
- 70:   mobile push notifications are enabled by default when a user first
- 71:   subscribes to the channel, potentially overriding the user's [default
- 72:   mobile notification
- 73:   setting](/help/channel-notifications#configure-default-notifications-for-all-channels)
- 74:   for channel messages. Only organization administrators can set or
- 81:   indicates whether mobile push notifications will be enabled by default
- 82:   when a user first subscribes to the channel, potentially overriding the
- 83:   user's [default mobile notification
- 84:   setting](/help/channel-notifications#configure-default-notifications-for-all-channels)
- 85:   for channel messages.
- 87: **Feature level 506**
- 92:   for records that were carried across a realm import; the export
- 93:   happened on a previous server, so its tarball is no longer stored
- 98:   be deleted, as the server has no exported data to delete for them. This
- 101: **Feature level 505**
- 106:   response is now also returned when the target message itself is past
- 107:   the time limit, as long as at least one message in the topic is within
- 108:   the limit.
- 110: **Feature level 504**
- 114:   now completely disables legacy push notifications rather than sending
- 115:   them with redacted content. This change was also backported to the Zulip
- 118: **Feature level 503**
- 121:   syntax only recognizes ISO 8601 formatted timestamps.
- 123: **Feature level 502**
- 125: No changes; start of Zulip 13.0 development branch.
- 127: Feature level 501 reserved for future use in 12.x maintenance
- 128: releases.
