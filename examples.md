# Examples

This file is written whole by `03_examples/build_examples.py` from the pairs named in
`03_examples/examples-manifest.md` and is never edited by hand: a change to the script or to the
manifest means running the script again. Each pair is one snapshot and the tickets file written for
it, input then output, every block a byte copy of the committed file, its header included. The suite
`02_validate/run_fixtures.py` regenerates this file and requires it to equal the committed one byte
for byte, so a hand edit of one character fails the suite.

## Pair 1

Input: raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt
```
source_url: https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md
final_url: https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md
http_status: 200
content_type: text/plain; charset=utf-8
retrieved: 20260922T032148Z
routine: as-served
routine_version: 1
sha256: 9f1b853d1198ba0c250d19552cb88b4834abf3ed4587155c271695fd8167ba65
--- body ---
      1: # Changelog
      2: 
      3: PagerDuty aims to have no breaking changes to our API, we do fix bugs and add new functionality continously. This document serves as a reference for any bug fixes or additions to our API.
      4: 
      5: Currently we do not deprecate or remove any API functionality.
      6: 
      7: ----
      8: 
      9: ### 2020-09-02
     10: - Added Audit Record description in API CONCEPTS document.
     11: - Clarified in the descriptions of audit record endpoints that records are returned in lists.
     12: 
     13: ### 2020-08-28
     14: - Added Early-Access endpoint for audit trail records
     15:    - `GET /services/{id}/audit/records`
     16: 
     17: ### 2020-08-27
     18: - Added Early-Access endpoint for audit trail records
     19:    - `GET /escalation_policies/{id}/audit/records`
     20: 
     21: ### 2020-08-27
     22: - Documented [Events V2 integration](https://developer.pagerduty.com/docs/events-api-v2/overview/) type on `/services/{id}/integrations` endpoints.
     23:     - Note: This existed previously and was missing from this documentation.
     24: 
     25: ### 2020-08-24
     26: - Clarified `contact_method` on various User Contact Method management endpoints.
     27: - Clarified Notification Subscription endpoints current under the Early Access.
     28: 
     29: ### 2020-08-18
     30: - Added Early-Access endpoints for audit trail records
     31:    - `GET /schedules/{id}/audit/records`
     32: 
     33: ### 2020-08-10
     34: - Added documentation on `config` and `headers` options for webhooks v2.
     35: - Added Request Examples with custom headers.
     36: 
     37: ### 2020-08-07
     38: - Updated models to include standard fields such as `id`, `type`, `summary`, `html_url`, and `self`.
     39: - Fixed inconsistencies with the `Reference` model.
     40: 
     41: ### 2020-08-06
     42: - Added Early-Access endpoints for audit trail records
     43:    - `GET /audit/records`
     44:    - `GET /teams/{id}/audit/records`
     45:    - `GET /users/{id}/audit/records`
     46: 
     47: ### 2020-08-04
     48: - Added 6 new Early-Access endpoints around incident subscription management.
     49:     - `GET /users/{id}/notification_subscriptions`
     50:     - `POST /users/{id}/notification_subscriptions`
     51:     - `POST /users/{id}/notification_subscriptions/unsubscribe`
     52:     - `GET /incidents/{id}/status_updates/subscribers`
     53:     - `POST /incidents/{id}/status_updates/subscribers`
     54:     - `POST /incidents/{id}/status_updates/unsubscribe`
     55: 
     56: ### 2020-07-24
     57: - Updated the request sample for `POST /extensions` and `PUT /extensions/{id}`.
     58: - Clarified Content-Type header for all endpoints.
     59: 
     60: ### 2020-07-10
     61: - Updated filters for all 5 `/analytics/metrics` and `/analytics/raw` endpoints. The `business_service_ids` filter is added as a possible optional filter choice. This filter accepts an array, to allow filtering by multiple business service IDs.
     62: 
     63: ### 2020-07-08
     64: - Add limit to the number of incidents or alerts that can be updated in a single API call to multi-update (i.e. `PUT /incidents`) above which the client receives status 413.
     65: 
     66: ### 2020-07-08
     67: - Updated filters for all 5 `/analytics/metrics` and `/analytics/raw` endpoints. The `priority` filter is replaced by `priority_ids` and `priority_names` filters. Both of these new filters accept an array, to allow filtering by multiple priority IDs or names.
     68: 
     69: ### 2020-07-01
     70: - Added documentation for configuring JIRA integration via API
     71: 
     72: ### 2020-06-29
     73: - Updated required headers, and filters for `POST analytics/raw/incidents`, `POST analytics/metrics/incidents/all`, `POST analytics/metrics/incidents/services` and `POST analytics/metrics/incidents/teams`.
     74: - Added `GET`, `DELETE`, and `PUT /users/{user_id}/status_update_notification_rules/{status_update_notitication_rule_id}`
     75: - Added `GET`, `POST /users/{user_id}/status_update_notification_rules`
     76: 
     77: ### 2020-06-22
     78: - Document `POST extensions/{id}/enable` for extensions that are temporarily disabled.
     79: 
     80: ### 2020-06-18
     81: - Added `POST analytics/metrics/incidents/all`, `POST analytics/metrics/incidents/services` and `POST analytics/metrics/incidents/teams` endpoints for Early Access.
     82: 
     83: ### 2020-06-17
     84: - Moved `POST analytics/incidents` and `GET analytics/incidents/{id}` to `POST analytics/raw/incidents` and `GET analytics/raw/incidents/{id}`
     85: 
     86: ### 2020-06-15
     87: - Added `POST analytics/incidents` and `GET analytics/incidents/{id}` endpoints for Early Access.
     88: 
     89: ### 2020-06-05
     90: - Modified `optional_total` query param to `total` on the business service list endpoint.
     91: - `optional_total` field will continue to be supported.
     92: 
     93: ### 2020-06-01
     94: - Added `suspend` event rule action to the API.
     95: 
     96: ### 2020-05-29
     97: - Added `GET /response_plays`, `POST /response_plays`, `GET /response_plays/{id}`, `PUT /response_plays/{id}`, and `DELETE /response_plays/{id}` endpoints.
     98: - Updated Response Plays description in API CONCEPTS document.
     99: 
    100: ### 2020-05-27
    101:  - Documented `total` query parameter on paginated endpoints.
    102: 
    103: ### 2020-05-19
    104:  - Added a `PUT log_entries/{id}/channel` endpoint to enable updates to log entry channel details.
    105: 
    106: ### 2020-05-12
    107:  - Fix Schema of `/teams/{id}/members` endpoint to match reality of behaviour.
    108: 
    109: ### 2020-04-30
    110:  - Add `teams` field to `Schedule` model, which is supported for updates and included in responses.
    111:  - Clarified Reference Model, `id` field is required.
    112: 
    113: ### 2020-04-27
    114:  - Document `include[]=temporarily_disabled` for extensions.
    115: 
    116: ### 2020-04-24
    117:  - Add `type` fields to `Log Entry` models.
    118:  - Fixed issue with Postman build. New version available, and new ones will continue to be published with each new update here.
    119: 
    120: ### 2020-04-21
    121:  - Fixed model `type` fields in schema definitions.
    122:  - Fix issues with Request Examples
    123: 
    124: ### 2020-04-15
    125:  - Updated all reference schemas to better match reality of API.
    126:  - Added examples to all Request and Response body's that were missing them.
    127: 
    128: ### 2020-04-15
    129:  - Added Events V1 and Events V2 APIs.
    130: 
    131: ### 2020-04-13
    132:  - Modified response and request examples to match OpenAPI 3.0.1 schema
    133: 
    134: ### 2020-04-09
    135:  - Added a `GET /service_dependencies/technical_services/{id}` endpoint.
    136:  - *BREAKING* `POST /service_dependencies/associate` was changed from 204 to 200 for successful changes.
    137:  - *BREAKING* `POST /service_dependencies/disassociate` was changed from 204 to 200 for successful changes.
    138:  - *Documentation Change* Fixed a mistake in the documentation. The `relationships` property in the request for `POST /service_dependencies/associate` and `POST /service_dependencies/disassociate` is an array and not an object.
    139:  - *Documentation Change* The `service_dependencies` endpoints can now be found at the top level instead of under the `Business Services` section.
    140: 
    141: ### 2020-04-06
    142:  - Added new Rulesets endpoints
    143: 
    144: ### 2020-04-01
    145:  - Added `since` and `until` parameters to `GET /incidents/{id}/log_entries`.
    146: 
    147: ### 2020-03-24
    148:  - Added `teams` to all `/business_services` endpoints.
    149: 
    150: ### 2020-03-23
    151:  - Clarified language on `GET /tags` query parameter to better explain how matching happens.
    152: 
    153: ### 2020-03-02
    154:  - Add new Business Services endpoints
    155: 
    156: ### 2020-01-27
    157:  - Clarified `POST /escalation_policies` description.
    158: 
    159: ### 2020-02-26
    160:  - `GET /oncalls OnCalls[].end` will now correctly respond `null` only when the user does not go off call.
    161: 
    162: ### 2020-01-10
    163:  - Added `on_call_handoff_notifications` to `EscalationPolicy` model.
    164:    - The field allow users to set whether they would like on-call handoff notifications for escalation policies that have no attached services.
    165:    - The field has been added to all `/escalation_policies` endpoints' request and response schema.
    166:    - The field has two options `always` and `if_has_services`, and defaults to `if_has_services` on `PUT` and `POST`

```

Output: raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.tickets.md
```
snapshot: raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt
sha256: 9f1b853d1198ba0c250d19552cb88b4834abf3ed4587155c271695fd8167ba65
source_url: https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md
body_range: 1-166
line_numbers: snapshot

## Ticket 1

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added Audit Record description in API CONCEPTS document. | 10 | - Added Audit Record description in API CONCEPTS document. |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-02 | 9 | ### 2020-09-02 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 10 |  |

## Ticket 2

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Clarified in the descriptions of audit record endpoints that records are returned in lists. | 11 | - Clarified in the descriptions of audit record endpoints that records are returned in lists. |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-02 | 9 | ### 2020-09-02 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 11 |  |

## Ticket 3

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /services/{id}/audit/records` | 15 | - `GET /services/{id}/audit/records` |
| affected_surface | `GET /services/{id}/audit/records` | 15 | - `GET /services/{id}/audit/records` |
| breaking | not in source |  |  |
| entry_date | 2020-08-28 | 13 | ### 2020-08-28 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 15 |  |

## Ticket 4

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /escalation_policies/{id}/audit/records` | 19 | - `GET /escalation_policies/{id}/audit/records` |
| affected_surface | `GET /escalation_policies/{id}/audit/records` | 19 | - `GET /escalation_policies/{id}/audit/records` |
| breaking | not in source |  |  |
| entry_date | 2020-08-27 | 17 | ### 2020-08-27 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 19 |  |

## Ticket 5

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Clarified `contact_method` on various User Contact Method management endpoints. | 26 | - Clarified `contact_method` on various User Contact Method management endpoints. |
| affected_surface | `contact_method` | 26 | - Clarified `contact_method` on various User Contact Method management endpoints. |
| affected_surface | Contact | 26 | - Clarified `contact_method` on various User Contact Method management endpoints. |
| breaking | not in source |  |  |
| entry_date | 2020-08-24 | 25 | ### 2020-08-24 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 26 |  |

## Ticket 6

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Clarified Notification Subscription endpoints current under the Early Access. | 27 | - Clarified Notification Subscription endpoints current under the Early Access. |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-08-24 | 25 | ### 2020-08-24 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 27 |  |

## Ticket 7

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /schedules/{id}/audit/records` | 31 | - `GET /schedules/{id}/audit/records` |
| affected_surface | `GET /schedules/{id}/audit/records` | 31 | - `GET /schedules/{id}/audit/records` |
| breaking | not in source |  |  |
| entry_date | 2020-08-18 | 29 | ### 2020-08-18 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 31 |  |

## Ticket 8

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added documentation on `config` and `headers` options for webhooks v2. | 34 | - Added documentation on `config` and `headers` options for webhooks v2. |
| affected_surface | `config` | 34 | - Added documentation on `config` and `headers` options for webhooks v2. |
| affected_surface | `headers` | 34 | - Added documentation on `config` and `headers` options for webhooks v2. |
| breaking | not in source |  |  |
| entry_date | 2020-08-10 | 33 | ### 2020-08-10 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 34 |  |

## Ticket 9

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added Request Examples with custom headers. | 35 | - Added Request Examples with custom headers. |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-08-10 | 33 | ### 2020-08-10 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 35 |  |

## Ticket 10

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Updated models to include standard fields such as `id`, `type`, `summary`, `html_url`, and `self`. | 38 | - Updated models to include standard fields such as `id`, `type`, `summary`, `html_url`, and `self`. |
| affected_surface | `id` | 38 | - Updated models to include standard fields such as `id`, `type`, `summary`, `html_url`, and `self`. |
| affected_surface | `type` | 38 | - Updated models to include standard fields such as `id`, `type`, `summary`, `html_url`, and `self`. |
| affected_surface | `summary` | 38 | - Updated models to include standard fields such as `id`, `type`, `summary`, `html_url`, and `self`. |
| affected_surface | `html_url` | 38 | - Updated models to include standard fields such as `id`, `type`, `summary`, `html_url`, and `self`. |
| affected_surface | `self` | 38 | - Updated models to include standard fields such as `id`, `type`, `summary`, `html_url`, and `self`. |
| breaking | not in source |  |  |
| entry_date | 2020-08-07 | 37 | ### 2020-08-07 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 38 |  |

## Ticket 11

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fixed inconsistencies with the `Reference` model. | 39 | - Fixed inconsistencies with the `Reference` model. |
| affected_surface | `Reference` | 39 | - Fixed inconsistencies with the `Reference` model. |
| breaking | not in source |  |  |
| entry_date | 2020-08-07 | 37 | ### 2020-08-07 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 39 |  |

## Ticket 12

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /audit/records` | 43 | - `GET /audit/records` |
| affected_surface | `GET /audit/records` | 43 | - `GET /audit/records` |
| breaking | not in source |  |  |
| entry_date | 2020-08-06 | 41 | ### 2020-08-06 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 43 |  |

## Ticket 13

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /teams/{id}/audit/records` | 44 | - `GET /teams/{id}/audit/records` |
| affected_surface | `GET /teams/{id}/audit/records` | 44 | - `GET /teams/{id}/audit/records` |
| breaking | not in source |  |  |
| entry_date | 2020-08-06 | 41 | ### 2020-08-06 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 44 |  |

## Ticket 14

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /users/{id}/audit/records` | 45 | - `GET /users/{id}/audit/records` |
| affected_surface | `GET /users/{id}/audit/records` | 45 | - `GET /users/{id}/audit/records` |
| breaking | not in source |  |  |
| entry_date | 2020-08-06 | 41 | ### 2020-08-06 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 45 |  |

## Ticket 15

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /users/{id}/notification_subscriptions` | 49 | - `GET /users/{id}/notification_subscriptions` |
| affected_surface | `GET /users/{id}/notification_subscriptions` | 49 | - `GET /users/{id}/notification_subscriptions` |
| breaking | not in source |  |  |
| entry_date | 2020-08-04 | 47 | ### 2020-08-04 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 49 |  |

## Ticket 16

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /users/{id}/notification_subscriptions` | 50 | - `POST /users/{id}/notification_subscriptions` |
| affected_surface | `POST /users/{id}/notification_subscriptions` | 50 | - `POST /users/{id}/notification_subscriptions` |
| breaking | not in source |  |  |
| entry_date | 2020-08-04 | 47 | ### 2020-08-04 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 50 |  |

## Ticket 17

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /users/{id}/notification_subscriptions/unsubscribe` | 51 | - `POST /users/{id}/notification_subscriptions/unsubscribe` |
| affected_surface | `POST /users/{id}/notification_subscriptions/unsubscribe` | 51 | - `POST /users/{id}/notification_subscriptions/unsubscribe` |
| breaking | not in source |  |  |
| entry_date | 2020-08-04 | 47 | ### 2020-08-04 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 51 |  |

## Ticket 18

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /incidents/{id}/status_updates/subscribers` | 52 | - `GET /incidents/{id}/status_updates/subscribers` |
| affected_surface | `GET /incidents/{id}/status_updates/subscribers` | 52 | - `GET /incidents/{id}/status_updates/subscribers` |
| breaking | not in source |  |  |
| entry_date | 2020-08-04 | 47 | ### 2020-08-04 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 52 |  |

## Ticket 19

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /incidents/{id}/status_updates/subscribers` | 53 | - `POST /incidents/{id}/status_updates/subscribers` |
| affected_surface | `POST /incidents/{id}/status_updates/subscribers` | 53 | - `POST /incidents/{id}/status_updates/subscribers` |
| breaking | not in source |  |  |
| entry_date | 2020-08-04 | 47 | ### 2020-08-04 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 53 |  |

## Ticket 20

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /incidents/{id}/status_updates/unsubscribe` | 54 | - `POST /incidents/{id}/status_updates/unsubscribe` |
| affected_surface | `POST /incidents/{id}/status_updates/unsubscribe` | 54 | - `POST /incidents/{id}/status_updates/unsubscribe` |
| breaking | not in source |  |  |
| entry_date | 2020-08-04 | 47 | ### 2020-08-04 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 54 |  |

## Ticket 21

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Updated the request sample for `POST /extensions` and `PUT /extensions/{id}`. | 57 | - Updated the request sample for `POST /extensions` and `PUT /extensions/{id}`. |
| affected_surface | `POST /extensions` | 57 | - Updated the request sample for `POST /extensions` and `PUT /extensions/{id}`. |
| affected_surface | `PUT /extensions/{id}` | 57 | - Updated the request sample for `POST /extensions` and `PUT /extensions/{id}`. |
| breaking | not in source |  |  |
| entry_date | 2020-07-24 | 56 | ### 2020-07-24 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 57 |  |

## Ticket 22

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Clarified Content-Type header for all endpoints. | 58 | - Clarified Content-Type header for all endpoints. |
| affected_surface | Content-Type | 58 | - Clarified Content-Type header for all endpoints. |
| breaking | not in source |  |  |
| entry_date | 2020-07-24 | 56 | ### 2020-07-24 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 58 |  |

## Ticket 23

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Updated filters for all 5 `/analytics/metrics` and `/analytics/raw` endpoints. The `business_service_ids` filter is added as a possible optional filter choice. This filter accepts an array, to allow filtering by multiple business service IDs. | 61 | - Updated filters for all 5 `/analytics/metrics` and `/analytics/raw` endpoints. The `business_service_ids` filter is added as a possible optional filter choice. This filter accepts an array, to allow filtering by multiple business service IDs. |
| affected_surface | `/analytics/metrics` | 61 | - Updated filters for all 5 `/analytics/metrics` and `/analytics/raw` endpoints. The `business_service_ids` filter is added as a possible optional filter choice. This filter accepts an array, to allow filtering by multiple business service IDs. |
| affected_surface | `/analytics/raw` | 61 | - Updated filters for all 5 `/analytics/metrics` and `/analytics/raw` endpoints. The `business_service_ids` filter is added as a possible optional filter choice. This filter accepts an array, to allow filtering by multiple business service IDs. |
| affected_surface | `business_service_ids` | 61 | - Updated filters for all 5 `/analytics/metrics` and `/analytics/raw` endpoints. The `business_service_ids` filter is added as a possible optional filter choice. This filter accepts an array, to allow filtering by multiple business service IDs. |
| breaking | not in source |  |  |
| entry_date | 2020-07-10 | 60 | ### 2020-07-10 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 61 |  |

## Ticket 24

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Add limit to the number of incidents or alerts that can be updated in a single API call to multi-update (i.e. `PUT /incidents`) above which the client receives status 413. | 64 | - Add limit to the number of incidents or alerts that can be updated in a single API call to multi-update (i.e. `PUT /incidents`) above which the client receives status 413. |
| affected_surface | `PUT /incidents` | 64 | - Add limit to the number of incidents or alerts that can be updated in a single API call to multi-update (i.e. `PUT /incidents`) above which the client receives status 413. |
| breaking | not in source |  |  |
| entry_date | 2020-07-08 | 63 | ### 2020-07-08 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 64 |  |

## Ticket 25

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Updated filters for all 5 `/analytics/metrics` and `/analytics/raw` endpoints. The `priority` filter is replaced by `priority_ids` and `priority_names` filters. Both of these new filters accept an array, to allow filtering by multiple priority IDs or names. | 67 | - Updated filters for all 5 `/analytics/metrics` and `/analytics/raw` endpoints. The `priority` filter is replaced by `priority_ids` and `priority_names` filters. Both of these new filters accept an array, to allow filtering by multiple priority IDs or names. |
| affected_surface | `/analytics/metrics` | 67 | - Updated filters for all 5 `/analytics/metrics` and `/analytics/raw` endpoints. The `priority` filter is replaced by `priority_ids` and `priority_names` filters. Both of these new filters accept an array, to allow filtering by multiple priority IDs or names. |
| affected_surface | `/analytics/raw` | 67 | - Updated filters for all 5 `/analytics/metrics` and `/analytics/raw` endpoints. The `priority` filter is replaced by `priority_ids` and `priority_names` filters. Both of these new filters accept an array, to allow filtering by multiple priority IDs or names. |
| affected_surface | `priority` | 67 | - Updated filters for all 5 `/analytics/metrics` and `/analytics/raw` endpoints. The `priority` filter is replaced by `priority_ids` and `priority_names` filters. Both of these new filters accept an array, to allow filtering by multiple priority IDs or names. |
| affected_surface | `priority_ids` | 67 | - Updated filters for all 5 `/analytics/metrics` and `/analytics/raw` endpoints. The `priority` filter is replaced by `priority_ids` and `priority_names` filters. Both of these new filters accept an array, to allow filtering by multiple priority IDs or names. |
| affected_surface | `priority_names` | 67 | - Updated filters for all 5 `/analytics/metrics` and `/analytics/raw` endpoints. The `priority` filter is replaced by `priority_ids` and `priority_names` filters. Both of these new filters accept an array, to allow filtering by multiple priority IDs or names. |
| breaking | not in source |  |  |
| entry_date | 2020-07-08 | 66 | ### 2020-07-08 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 67 |  |

## Ticket 26

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added documentation for configuring JIRA integration via API | 70 | - Added documentation for configuring JIRA integration via API |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-07-01 | 69 | ### 2020-07-01 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 70 |  |

## Ticket 27

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Updated required headers, and filters for `POST analytics/raw/incidents`, `POST analytics/metrics/incidents/all`, `POST analytics/metrics/incidents/services` and `POST analytics/metrics/incidents/teams`. | 73 | - Updated required headers, and filters for `POST analytics/raw/incidents`, `POST analytics/metrics/incidents/all`, `POST analytics/metrics/incidents/services` and `POST analytics/metrics/incidents/teams`. |
| affected_surface | `POST analytics/raw/incidents` | 73 | - Updated required headers, and filters for `POST analytics/raw/incidents`, `POST analytics/metrics/incidents/all`, `POST analytics/metrics/incidents/services` and `POST analytics/metrics/incidents/teams`. |
| affected_surface | `POST analytics/metrics/incidents/all` | 73 | - Updated required headers, and filters for `POST analytics/raw/incidents`, `POST analytics/metrics/incidents/all`, `POST analytics/metrics/incidents/services` and `POST analytics/metrics/incidents/teams`. |
| affected_surface | `POST analytics/metrics/incidents/services` | 73 | - Updated required headers, and filters for `POST analytics/raw/incidents`, `POST analytics/metrics/incidents/all`, `POST analytics/metrics/incidents/services` and `POST analytics/metrics/incidents/teams`. |
| affected_surface | `POST analytics/metrics/incidents/teams` | 73 | - Updated required headers, and filters for `POST analytics/raw/incidents`, `POST analytics/metrics/incidents/all`, `POST analytics/metrics/incidents/services` and `POST analytics/metrics/incidents/teams`. |
| breaking | not in source |  |  |
| entry_date | 2020-06-29 | 72 | ### 2020-06-29 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 73 |  |

## Ticket 28

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `GET`, `DELETE`, and `PUT /users/{user_id}/status_update_notification_rules/{status_update_notitication_rule_id}` | 74 | - Added `GET`, `DELETE`, and `PUT /users/{user_id}/status_update_notification_rules/{status_update_notitication_rule_id}` |
| affected_surface | `GET` | 74 | - Added `GET`, `DELETE`, and `PUT /users/{user_id}/status_update_notification_rules/{status_update_notitication_rule_id}` |
| affected_surface | `DELETE` | 74 | - Added `GET`, `DELETE`, and `PUT /users/{user_id}/status_update_notification_rules/{status_update_notitication_rule_id}` |
| affected_surface | `PUT /users/{user_id}/status_update_notification_rules/{status_update_notitication_rule_id}` | 74 | - Added `GET`, `DELETE`, and `PUT /users/{user_id}/status_update_notification_rules/{status_update_notitication_rule_id}` |
| breaking | not in source |  |  |
| entry_date | 2020-06-29 | 72 | ### 2020-06-29 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 74 |  |

## Ticket 29

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `GET`, `POST /users/{user_id}/status_update_notification_rules` | 75 | - Added `GET`, `POST /users/{user_id}/status_update_notification_rules` |
| affected_surface | `GET` | 75 | - Added `GET`, `POST /users/{user_id}/status_update_notification_rules` |
| affected_surface | `POST /users/{user_id}/status_update_notification_rules` | 75 | - Added `GET`, `POST /users/{user_id}/status_update_notification_rules` |
| breaking | not in source |  |  |
| entry_date | 2020-06-29 | 72 | ### 2020-06-29 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 75 |  |

## Ticket 30

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Document `POST extensions/{id}/enable` for extensions that are temporarily disabled. | 78 | - Document `POST extensions/{id}/enable` for extensions that are temporarily disabled. |
| affected_surface | `POST extensions/{id}/enable` | 78 | - Document `POST extensions/{id}/enable` for extensions that are temporarily disabled. |
| breaking | not in source |  |  |
| entry_date | 2020-06-22 | 77 | ### 2020-06-22 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 78 |  |

## Ticket 31

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `POST analytics/metrics/incidents/all`, `POST analytics/metrics/incidents/services` and `POST analytics/metrics/incidents/teams` endpoints for Early Access. | 81 | - Added `POST analytics/metrics/incidents/all`, `POST analytics/metrics/incidents/services` and `POST analytics/metrics/incidents/teams` endpoints for Early Access. |
| affected_surface | `POST analytics/metrics/incidents/all` | 81 | - Added `POST analytics/metrics/incidents/all`, `POST analytics/metrics/incidents/services` and `POST analytics/metrics/incidents/teams` endpoints for Early Access. |
| affected_surface | `POST analytics/metrics/incidents/services` | 81 | - Added `POST analytics/metrics/incidents/all`, `POST analytics/metrics/incidents/services` and `POST analytics/metrics/incidents/teams` endpoints for Early Access. |
| affected_surface | `POST analytics/metrics/incidents/teams` | 81 | - Added `POST analytics/metrics/incidents/all`, `POST analytics/metrics/incidents/services` and `POST analytics/metrics/incidents/teams` endpoints for Early Access. |
| breaking | not in source |  |  |
| entry_date | 2020-06-18 | 80 | ### 2020-06-18 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 81 |  |

## Ticket 32

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Moved `POST analytics/incidents` and `GET analytics/incidents/{id}` to `POST analytics/raw/incidents` and `GET analytics/raw/incidents/{id}` | 84 | - Moved `POST analytics/incidents` and `GET analytics/incidents/{id}` to `POST analytics/raw/incidents` and `GET analytics/raw/incidents/{id}` |
| affected_surface | `POST analytics/incidents` | 84 | - Moved `POST analytics/incidents` and `GET analytics/incidents/{id}` to `POST analytics/raw/incidents` and `GET analytics/raw/incidents/{id}` |
| affected_surface | `GET analytics/incidents/{id}` | 84 | - Moved `POST analytics/incidents` and `GET analytics/incidents/{id}` to `POST analytics/raw/incidents` and `GET analytics/raw/incidents/{id}` |
| affected_surface | `POST analytics/raw/incidents` | 84 | - Moved `POST analytics/incidents` and `GET analytics/incidents/{id}` to `POST analytics/raw/incidents` and `GET analytics/raw/incidents/{id}` |
| affected_surface | `GET analytics/raw/incidents/{id}` | 84 | - Moved `POST analytics/incidents` and `GET analytics/incidents/{id}` to `POST analytics/raw/incidents` and `GET analytics/raw/incidents/{id}` |
| breaking | not in source |  |  |
| entry_date | 2020-06-17 | 83 | ### 2020-06-17 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 84 |  |

## Ticket 33

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `POST analytics/incidents` and `GET analytics/incidents/{id}` endpoints for Early Access. | 87 | - Added `POST analytics/incidents` and `GET analytics/incidents/{id}` endpoints for Early Access. |
| affected_surface | `POST analytics/incidents` | 87 | - Added `POST analytics/incidents` and `GET analytics/incidents/{id}` endpoints for Early Access. |
| affected_surface | `GET analytics/incidents/{id}` | 87 | - Added `POST analytics/incidents` and `GET analytics/incidents/{id}` endpoints for Early Access. |
| breaking | not in source |  |  |
| entry_date | 2020-06-15 | 86 | ### 2020-06-15 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 87 |  |

## Ticket 34

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Modified `optional_total` query param to `total` on the business service list endpoint. | 90 | - Modified `optional_total` query param to `total` on the business service list endpoint. |
| affected_surface | `optional_total` | 90 | - Modified `optional_total` query param to `total` on the business service list endpoint. |
| affected_surface | `total` | 90 | - Modified `optional_total` query param to `total` on the business service list endpoint. |
| breaking | not in source |  |  |
| entry_date | 2020-06-05 | 89 | ### 2020-06-05 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 90 |  |

## Ticket 35

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `suspend` event rule action to the API. | 94 | - Added `suspend` event rule action to the API. |
| affected_surface | `suspend` | 94 | - Added `suspend` event rule action to the API. |
| breaking | not in source |  |  |
| entry_date | 2020-06-01 | 93 | ### 2020-06-01 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 94 |  |

## Ticket 36

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `GET /response_plays`, `POST /response_plays`, `GET /response_plays/{id}`, `PUT /response_plays/{id}`, and `DELETE /response_plays/{id}` endpoints. | 97 | - Added `GET /response_plays`, `POST /response_plays`, `GET /response_plays/{id}`, `PUT /response_plays/{id}`, and `DELETE /response_plays/{id}` endpoints. |
| affected_surface | `GET /response_plays` | 97 | - Added `GET /response_plays`, `POST /response_plays`, `GET /response_plays/{id}`, `PUT /response_plays/{id}`, and `DELETE /response_plays/{id}` endpoints. |
| affected_surface | `POST /response_plays` | 97 | - Added `GET /response_plays`, `POST /response_plays`, `GET /response_plays/{id}`, `PUT /response_plays/{id}`, and `DELETE /response_plays/{id}` endpoints. |
| affected_surface | `GET /response_plays/{id}` | 97 | - Added `GET /response_plays`, `POST /response_plays`, `GET /response_plays/{id}`, `PUT /response_plays/{id}`, and `DELETE /response_plays/{id}` endpoints. |
| affected_surface | `PUT /response_plays/{id}` | 97 | - Added `GET /response_plays`, `POST /response_plays`, `GET /response_plays/{id}`, `PUT /response_plays/{id}`, and `DELETE /response_plays/{id}` endpoints. |
| affected_surface | `DELETE /response_plays/{id}` | 97 | - Added `GET /response_plays`, `POST /response_plays`, `GET /response_plays/{id}`, `PUT /response_plays/{id}`, and `DELETE /response_plays/{id}` endpoints. |
| breaking | not in source |  |  |
| entry_date | 2020-05-29 | 96 | ### 2020-05-29 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 97 |  |

## Ticket 37

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Updated Response Plays description in API CONCEPTS document. | 98 | - Updated Response Plays description in API CONCEPTS document. |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-05-29 | 96 | ### 2020-05-29 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 98 |  |

## Ticket 38

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Documented `total` query parameter on paginated endpoints. | 101 | - Documented `total` query parameter on paginated endpoints. |
| affected_surface | `total` | 101 | - Documented `total` query parameter on paginated endpoints. |
| affected_surface | query | 101 | - Documented `total` query parameter on paginated endpoints. |
| breaking | not in source |  |  |
| entry_date | 2020-05-27 | 100 | ### 2020-05-27 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 101 |  |

## Ticket 39

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added a `PUT log_entries/{id}/channel` endpoint to enable updates to log entry channel details. | 104 | - Added a `PUT log_entries/{id}/channel` endpoint to enable updates to log entry channel details. |
| affected_surface | `PUT log_entries/{id}/channel` | 104 | - Added a `PUT log_entries/{id}/channel` endpoint to enable updates to log entry channel details. |
| breaking | not in source |  |  |
| entry_date | 2020-05-19 | 103 | ### 2020-05-19 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 104 |  |

## Ticket 40

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fix Schema of `/teams/{id}/members` endpoint to match reality of behaviour. | 107 | - Fix Schema of `/teams/{id}/members` endpoint to match reality of behaviour. |
| affected_surface | `/teams/{id}/members` | 107 | - Fix Schema of `/teams/{id}/members` endpoint to match reality of behaviour. |
| breaking | not in source |  |  |
| entry_date | 2020-05-12 | 106 | ### 2020-05-12 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 107 |  |

## Ticket 41

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Add `teams` field to `Schedule` model, which is supported for updates and included in responses. | 110 | - Add `teams` field to `Schedule` model, which is supported for updates and included in responses. |
| affected_surface | `teams` | 110 | - Add `teams` field to `Schedule` model, which is supported for updates and included in responses. |
| affected_surface | `Schedule` | 110 | - Add `teams` field to `Schedule` model, which is supported for updates and included in responses. |
| breaking | not in source |  |  |
| entry_date | 2020-04-30 | 109 | ### 2020-04-30 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 110 |  |

## Ticket 42

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Clarified Reference Model, `id` field is required. | 111 | - Clarified Reference Model, `id` field is required. |
| affected_surface | `id` | 111 | - Clarified Reference Model, `id` field is required. |
| breaking | not in source |  |  |
| entry_date | 2020-04-30 | 109 | ### 2020-04-30 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 111 |  |

## Ticket 43

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Document `include[]=temporarily_disabled` for extensions. | 114 | - Document `include[]=temporarily_disabled` for extensions. |
| affected_surface | `include[]=temporarily_disabled` | 114 | - Document `include[]=temporarily_disabled` for extensions. |
| breaking | not in source |  |  |
| entry_date | 2020-04-27 | 113 | ### 2020-04-27 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 114 |  |

## Ticket 44

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Add `type` fields to `Log Entry` models. | 117 | - Add `type` fields to `Log Entry` models. |
| affected_surface | `type` | 117 | - Add `type` fields to `Log Entry` models. |
| affected_surface | `Log Entry` | 117 | - Add `type` fields to `Log Entry` models. |
| breaking | not in source |  |  |
| entry_date | 2020-04-24 | 116 | ### 2020-04-24 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 117 |  |

## Ticket 45

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fixed issue with Postman build. New version available, and new ones will continue to be published with each new update here. | 118 | - Fixed issue with Postman build. New version available, and new ones will continue to be published with each new update here. |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-04-24 | 116 | ### 2020-04-24 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 118 |  |

## Ticket 46

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fixed model `type` fields in schema definitions. | 121 | - Fixed model `type` fields in schema definitions. |
| affected_surface | `type` | 121 | - Fixed model `type` fields in schema definitions. |
| breaking | not in source |  |  |
| entry_date | 2020-04-21 | 120 | ### 2020-04-21 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 121 |  |

## Ticket 47

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fix issues with Request Examples | 122 | - Fix issues with Request Examples |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-04-21 | 120 | ### 2020-04-21 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 122 |  |

## Ticket 48

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Updated all reference schemas to better match reality of API. | 125 | - Updated all reference schemas to better match reality of API. |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-04-15 | 124 | ### 2020-04-15 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 125 |  |

## Ticket 49

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added examples to all Request and Response body's that were missing them. | 126 | - Added examples to all Request and Response body's that were missing them. |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-04-15 | 124 | ### 2020-04-15 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 126 |  |

## Ticket 50

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added Events V1 and Events V2 APIs. | 129 | - Added Events V1 and Events V2 APIs. |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-04-15 | 128 | ### 2020-04-15 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 129 |  |

## Ticket 51

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Modified response and request examples to match OpenAPI 3.0.1 schema | 132 | - Modified response and request examples to match OpenAPI 3.0.1 schema |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-04-13 | 131 | ### 2020-04-13 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 132 |  |

## Ticket 52

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added a `GET /service_dependencies/technical_services/{id}` endpoint. | 135 | - Added a `GET /service_dependencies/technical_services/{id}` endpoint. |
| affected_surface | `GET /service_dependencies/technical_services/{id}` | 135 | - Added a `GET /service_dependencies/technical_services/{id}` endpoint. |
| breaking | not in source |  |  |
| entry_date | 2020-04-09 | 134 | ### 2020-04-09 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 135 |  |

## Ticket 53

| field | value | line | quote |
| --- | --- | --- | --- |
| change | *BREAKING* `POST /service_dependencies/associate` was changed from 204 to 200 for successful changes. | 136 | - *BREAKING* `POST /service_dependencies/associate` was changed from 204 to 200 for successful changes. |
| affected_surface | `POST /service_dependencies/associate` | 136 | - *BREAKING* `POST /service_dependencies/associate` was changed from 204 to 200 for successful changes. |
| breaking | not in source |  |  |
| entry_date | 2020-04-09 | 134 | ### 2020-04-09 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 136 |  |

## Ticket 54

| field | value | line | quote |
| --- | --- | --- | --- |
| change | *BREAKING* `POST /service_dependencies/disassociate` was changed from 204 to 200 for successful changes. | 137 | - *BREAKING* `POST /service_dependencies/disassociate` was changed from 204 to 200 for successful changes. |
| affected_surface | `POST /service_dependencies/disassociate` | 137 | - *BREAKING* `POST /service_dependencies/disassociate` was changed from 204 to 200 for successful changes. |
| breaking | not in source |  |  |
| entry_date | 2020-04-09 | 134 | ### 2020-04-09 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 137 |  |

## Ticket 55

| field | value | line | quote |
| --- | --- | --- | --- |
| change | *Documentation Change* Fixed a mistake in the documentation. The `relationships` property in the request for `POST /service_dependencies/associate` and `POST /service_dependencies/disassociate` is an array and not an object. | 138 | - *Documentation Change* Fixed a mistake in the documentation. The `relationships` property in the request for `POST /service_dependencies/associate` and `POST /service_dependencies/disassociate` is an array and not an object. |
| affected_surface | `relationships` | 138 | - *Documentation Change* Fixed a mistake in the documentation. The `relationships` property in the request for `POST /service_dependencies/associate` and `POST /service_dependencies/disassociate` is an array and not an object. |
| affected_surface | `POST /service_dependencies/associate` | 138 | - *Documentation Change* Fixed a mistake in the documentation. The `relationships` property in the request for `POST /service_dependencies/associate` and `POST /service_dependencies/disassociate` is an array and not an object. |
| affected_surface | `POST /service_dependencies/disassociate` | 138 | - *Documentation Change* Fixed a mistake in the documentation. The `relationships` property in the request for `POST /service_dependencies/associate` and `POST /service_dependencies/disassociate` is an array and not an object. |
| breaking | not in source |  |  |
| entry_date | 2020-04-09 | 134 | ### 2020-04-09 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 138 |  |

## Ticket 56

| field | value | line | quote |
| --- | --- | --- | --- |
| change | *Documentation Change* The `service_dependencies` endpoints can now be found at the top level instead of under the `Business Services` section. | 139 | - *Documentation Change* The `service_dependencies` endpoints can now be found at the top level instead of under the `Business Services` section. |
| affected_surface | `service_dependencies` | 139 | - *Documentation Change* The `service_dependencies` endpoints can now be found at the top level instead of under the `Business Services` section. |
| affected_surface | `Business Services` | 139 | - *Documentation Change* The `service_dependencies` endpoints can now be found at the top level instead of under the `Business Services` section. |
| breaking | not in source |  |  |
| entry_date | 2020-04-09 | 134 | ### 2020-04-09 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 139 |  |

## Ticket 57

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added new Rulesets endpoints | 142 | - Added new Rulesets endpoints |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-04-06 | 141 | ### 2020-04-06 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 142 |  |

## Ticket 58

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `since` and `until` parameters to `GET /incidents/{id}/log_entries`. | 145 | - Added `since` and `until` parameters to `GET /incidents/{id}/log_entries`. |
| affected_surface | `since` | 145 | - Added `since` and `until` parameters to `GET /incidents/{id}/log_entries`. |
| affected_surface | `until` | 145 | - Added `since` and `until` parameters to `GET /incidents/{id}/log_entries`. |
| affected_surface | `GET /incidents/{id}/log_entries` | 145 | - Added `since` and `until` parameters to `GET /incidents/{id}/log_entries`. |
| breaking | not in source |  |  |
| entry_date | 2020-04-01 | 144 | ### 2020-04-01 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 145 |  |

## Ticket 59

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `teams` to all `/business_services` endpoints. | 148 | - Added `teams` to all `/business_services` endpoints. |
| affected_surface | `teams` | 148 | - Added `teams` to all `/business_services` endpoints. |
| affected_surface | `/business_services` | 148 | - Added `teams` to all `/business_services` endpoints. |
| breaking | not in source |  |  |
| entry_date | 2020-03-24 | 147 | ### 2020-03-24 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 148 |  |

## Ticket 60

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Clarified language on `GET /tags` query parameter to better explain how matching happens. | 151 | - Clarified language on `GET /tags` query parameter to better explain how matching happens. |
| affected_surface | `GET /tags` | 151 | - Clarified language on `GET /tags` query parameter to better explain how matching happens. |
| affected_surface | query | 151 | - Clarified language on `GET /tags` query parameter to better explain how matching happens. |
| breaking | not in source |  |  |
| entry_date | 2020-03-23 | 150 | ### 2020-03-23 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 151 |  |

## Ticket 61

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Add new Business Services endpoints | 154 | - Add new Business Services endpoints |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-03-02 | 153 | ### 2020-03-02 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 154 |  |

## Ticket 62

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Clarified `POST /escalation_policies` description. | 157 | - Clarified `POST /escalation_policies` description. |
| affected_surface | `POST /escalation_policies` | 157 | - Clarified `POST /escalation_policies` description. |
| breaking | not in source |  |  |
| entry_date | 2020-01-27 | 156 | ### 2020-01-27 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 157 |  |

## Ticket 63

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /oncalls OnCalls[].end` will now correctly respond `null` only when the user does not go off call. | 160 | - `GET /oncalls OnCalls[].end` will now correctly respond `null` only when the user does not go off call. |
| affected_surface | `GET /oncalls OnCalls[].end` | 160 | - `GET /oncalls OnCalls[].end` will now correctly respond `null` only when the user does not go off call. |
| affected_surface | `null` | 160 | - `GET /oncalls OnCalls[].end` will now correctly respond `null` only when the user does not go off call. |
| breaking | not in source |  |  |
| entry_date | 2020-02-26 | 159 | ### 2020-02-26 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 160 |  |

## Ticket 64

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The field has been added to all `/escalation_policies` endpoints' request and response schema. | 165 | - The field has been added to all `/escalation_policies` endpoints' request and response schema. |
| affected_surface | `on_call_handoff_notifications` | 163 | - Added `on_call_handoff_notifications` to `EscalationPolicy` model. |
| affected_surface | `EscalationPolicy` | 163 | - Added `on_call_handoff_notifications` to `EscalationPolicy` model. |
| affected_surface | The | 165 | - The field has been added to all `/escalation_policies` endpoints' request and response schema. |
| affected_surface | `/escalation_policies` | 165 | - The field has been added to all `/escalation_policies` endpoints' request and response schema. |
| breaking | not in source |  |  |
| entry_date | 2020-01-10 | 162 | ### 2020-01-10 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/PagerDuty/api-schema/f2c09c0df6b3c4bd9d5df8a9940014785a8fb87f/docs/CHANGELOG.md raw-githubusercontent-com-pagerduty-api-schema-f2c09c0df6b3c4bd9d5df8a9940014785-20260922T032148Z.txt | 165 |  |

## Unmapped

- 1: # Changelog
- 3: PagerDuty aims to have no breaking changes to our API, we do fix bugs and add new functionality continously. This document serves as a reference for any bug fixes or additions to our API.
- 5: Currently we do not deprecate or remove any API functionality.
- 7: ----
- 14: - Added Early-Access endpoint for audit trail records
- 18: - Added Early-Access endpoint for audit trail records
- 21: ### 2020-08-27
- 22: - Documented [Events V2 integration](https://developer.pagerduty.com/docs/events-api-v2/overview/) type on `/services/{id}/integrations` endpoints.
- 23:     - Note: This existed previously and was missing from this documentation.
- 30: - Added Early-Access endpoints for audit trail records
- 42: - Added Early-Access endpoints for audit trail records
- 48: - Added 6 new Early-Access endpoints around incident subscription management.
- 91: - `optional_total` field will continue to be supported.
- 164:    - The field allow users to set whether they would like on-call handoff notifications for escalation policies that have no attached services.
- 166:    - The field has two options `always` and `if_has_services`, and defaults to `if_has_services` on `PUT` and `POST`

```

## Pair 2

Input: raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt
```
source_url: https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md
final_url: https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md
http_status: 200
content_type: text/plain; charset=utf-8
retrieved: 20260921T212216Z
routine: as-served
routine_version: 1
sha256: d5cfeba8e2effb279f33fac41e317078f4460f921d9ef7379927d2ab5dd792b6
--- body ---
      1: ---
      2: title: "Engine API version history"
      3: description: "Documentation of changes that have been made to Engine API."
      4: keywords: "API, Docker, rcli, REST, documentation"
      5: ---
      6: 
      7: <!-- This file is maintained within the docker/docker Github
      8:      repository at https://github.com/docker/docker/. Make all
      9:      pull requests against that repo. If you see this file in
     10:      another repository, consider it read-only there, as it will
     11:      periodically be overwritten by the definitive file. Pull
     12:      requests which include edits to this file in other repositories
     13:      will be rejected.
     14: -->
     15: 
     16: ## v1.26 API changes
     17: 
     18: [Docker Engine API v1.26](https://docs.docker.com/engine/api/v1.26/) documentation
     19: 
     20: * `POST /plugins/(plugin name)/upgrade` upgrade a plugin.
     21: 
     22: ## v1.25 API changes
     23: 
     24: [Docker Engine API v1.25](https://docs.docker.com/engine/api/v1.25/) documentation
     25: 
     26: * The API version is now required in all API calls. Instead of just requesting, for example, the URL `/containers/json`, you must now request `/v1.25/containers/json`.
     27: * `GET /version` now returns `MinAPIVersion`.
     28: * `POST /build` accepts `networkmode` parameter to specify network used during build.
     29: * `GET /images/(name)/json` now returns `OsVersion` if populated
     30: * `GET /info` now returns `Isolation`.
     31: * `POST /containers/create` now takes `AutoRemove` in HostConfig, to enable auto-removal of the container on daemon side when the container's process exits.
     32: * `GET /containers/json` and `GET /containers/(id or name)/json` now return `"removing"` as a value for the `State.Status` field if the container is being removed. Previously, "exited" was returned as status.
     33: * `GET /containers/json` now accepts `removing` as a valid value for the `status` filter.
     34: * `GET /containers/json` now supports filtering containers by `health` status.
     35: * `DELETE /volumes/(name)` now accepts a `force` query parameter to force removal of volumes that were already removed out of band by the volume driver plugin.
     36: * `POST /containers/create/` and `POST /containers/(name)/update` now validates restart policies.
     37: * `POST /containers/create` now validates IPAMConfig in NetworkingConfig, and returns error for invalid IPv4 and IPv6 addresses (`--ip` and `--ip6` in `docker create/run`).
     38: * `POST /containers/create` now takes a `Mounts` field in `HostConfig` which replaces `Binds`, `Volumes`, and `Tmpfs`. *note*: `Binds`, `Volumes`, and `Tmpfs` are still available and can be combined with `Mounts`.
     39: * `POST /build` now performs a preliminary validation of the `Dockerfile` before starting the build, and returns an error if the syntax is incorrect. Note that this change is _unversioned_ and applied to all API versions.
     40: * `POST /build` accepts `cachefrom` parameter to specify images used for build cache.
     41: * `GET /networks/` endpoint now correctly returns a list of *all* networks,
     42:   instead of the default network if a trailing slash is provided, but no `name`
     43:   or `id`.
     44: * `DELETE /containers/(name)` endpoint now returns an error of `removal of container name is already in progress` with status code of 400, when container name is in a state of removal in progress.
     45: * `GET /containers/json` now supports a `is-task` filter to filter
     46:   containers that are tasks (part of a service in swarm mode).
     47: * `POST /containers/create` now takes `StopTimeout` field.
     48: * `POST /services/create` and `POST /services/(id or name)/update` now accept `Monitor` and `MaxFailureRatio` parameters, which control the response to failures during service updates.
     49: * `POST /services/(id or name)/update` now accepts a `ForceUpdate` parameter inside the `TaskTemplate`, which causes the service to be updated even if there are no changes which would ordinarily trigger an update.
     50: * `POST /services/create` and `POST /services/(id or name)/update` now return a `Warnings` array.
     51: * `GET /networks/(name)` now returns field `Created` in response to show network created time.
     52: * `POST /containers/(id or name)/exec` now accepts an `Env` field, which holds a list of environment variables to be set in the context of the command execution.
     53: * `GET /volumes`, `GET /volumes/(name)`, and `POST /volumes/create` now return the `Options` field which holds the driver specific options to use for when creating the volume.
     54: * `GET /exec/(id)/json` now returns `Pid`, which is the system pid for the exec'd process.
     55: * `POST /containers/prune` prunes stopped containers.
     56: * `POST /images/prune` prunes unused images.
     57: * `POST /volumes/prune` prunes unused volumes.
     58: * `POST /networks/prune` prunes unused networks.
     59: * Every API response now includes a `Docker-Experimental` header specifying if experimental features are enabled (value can be `true` or `false`).
     60: * Every API response now includes a `API-Version` header specifying the default API version of the server.
     61: * The `hostConfig` option now accepts the fields `CpuRealtimePeriod` and `CpuRtRuntime` to allocate cpu runtime to rt tasks when `CONFIG_RT_GROUP_SCHED` is enabled in the kernel.
     62: * The `SecurityOptions` field within the `GET /info` response now includes `userns` if user namespaces are enabled in the daemon.
     63: * `GET /nodes` and `GET /node/(id or name)` now return `Addr` as part of a node's `Status`, which is the address that that node connects to the manager from.
     64: * The `HostConfig` field now includes `NanoCPUs` that represents CPU quota in units of 10<sup>-9</sup> CPUs.
     65: * `GET /info` now returns more structured information about security options.
     66: * The `HostConfig` field now includes `CpuCount` that represents the number of CPUs available for execution by the container. Windows daemon only.
     67: * `POST /services/create` and `POST /services/(id or name)/update` now accept the `TTY` parameter, which allocate a pseudo-TTY in container.
     68: * `POST /services/create` and `POST /services/(id or name)/update` now accept the `DNSConfig` parameter, which specifies DNS related configurations in resolver configuration file (resolv.conf) through `Nameservers`, `Search`, and `Options`.
     69: * `GET /networks/(id or name)` now includes IP and name of all peers nodes for swarm mode overlay networks.
     70: * `GET /plugins` list plugins.
     71: * `POST /plugins/pull?name=<plugin name>` pulls a plugin.
     72: * `GET /plugins/(plugin name)` inspect a plugin.
     73: * `POST /plugins/(plugin name)/set` configure a plugin.
     74: * `POST /plugins/(plugin name)/enable` enable a plugin.
     75: * `POST /plugins/(plugin name)/disable` disable a plugin.
     76: * `POST /plugins/(plugin name)/push` push a plugin.
     77: * `POST /plugins/create?name=(plugin name)` create a plugin.
     78: * `DELETE /plugins/(plugin name)` delete a plugin.
     79: * `POST /node/(id or name)/update` now accepts both `id` or `name` to identify the node to update.
     80: * `GET /images/json` now support a `reference` filter.
     81: * `GET /secrets` returns information on the secrets.
     82: * `POST /secrets/create` creates a secret.
     83: * `DELETE /secrets/{id}` removes the secret `id`.
     84: * `GET /secrets/{id}` returns information on the secret `id`.
     85: * `POST /secrets/{id}/update` updates the secret `id`.
     86: * `POST /services/(id or name)/update` now accepts service name or prefix of service id as a parameter.
     87: 
     88: ## v1.24 API changes
     89: 
     90: [Docker Engine API v1.24](v1.24.md) documentation
     91: 
     92: * `POST /containers/create` now takes `StorageOpt` field.
     93: * `GET /info` now returns `SecurityOptions` field, showing if `apparmor`, `seccomp`, or `selinux` is supported.
     94: * `GET /info` no longer returns the `ExecutionDriver` property. This property was no longer used after integration
     95:   with ContainerD in Docker 1.11.
     96: * `GET /networks` now supports filtering by `label` and `driver`.
     97: * `GET /containers/json` now supports filtering containers by `network` name or id.
     98: * `POST /containers/create` now takes `IOMaximumBandwidth` and `IOMaximumIOps` fields. Windows daemon only.
     99: * `POST /containers/create` now returns an HTTP 400 "bad parameter" message
    100:   if no command is specified (instead of an HTTP 500 "server error")
    101: * `GET /images/search` now takes a `filters` query parameter.
    102: * `GET /events` now supports a `reload` event that is emitted when the daemon configuration is reloaded.
    103: * `GET /events` now supports filtering by daemon name or ID.
    104: * `GET /events` now supports a `detach` event that is emitted on detaching from container process.
    105: * `GET /events` now supports an `exec_detach ` event that is emitted on detaching from exec process.
    106: * `GET /images/json` now supports filters `since` and `before`.
    107: * `POST /containers/(id or name)/start` no longer accepts a `HostConfig`.
    108: * `POST /images/(name)/tag` no longer has a `force` query parameter.
    109: * `GET /images/search` now supports maximum returned search results `limit`.
    110: * `POST /containers/{name:.*}/copy` is now removed and errors out starting from this API version.
    111: * API errors are now returned as JSON instead of plain text.
    112: * `POST /containers/create` and `POST /containers/(id)/start` allow you to configure kernel parameters (sysctls) for use in the container.
    113: * `POST /containers/<container ID>/exec` and `POST /exec/<exec ID>/start`
    114:   no longer expects a "Container" field to be present. This property was not used
    115:   and is no longer sent by the docker client.
    116: * `POST /containers/create/` now validates the hostname (should be a valid RFC 1123 hostname).
    117: * `POST /containers/create/` `HostConfig.PidMode` field now accepts `container:<name|id>`,
    118:   to have the container join the PID namespace of an existing container.
    119: 
    120: ## v1.23 API changes
    121: 
    122: [Docker Engine API v1.23](v1.23.md) documentation
    123: 
    124: * `GET /containers/json` returns the state of the container, one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`.
    125: * `GET /containers/json` returns the mount points for the container.
    126: * `GET /networks/(name)` now returns an `Internal` field showing whether the network is internal or not.
    127: * `GET /networks/(name)` now returns an `EnableIPv6` field showing whether the network has ipv6 enabled or not.
    128: * `POST /containers/(name)/update` now supports updating container's restart policy.
    129: * `POST /networks/create` now supports enabling ipv6 on the network by setting the `EnableIPv6` field (doing this with a label will no longer work).
    130: * `GET /info` now returns `CgroupDriver` field showing what cgroup driver the daemon is using; `cgroupfs` or `systemd`.
    131: * `GET /info` now returns `KernelMemory` field, showing if "kernel memory limit" is supported.
    132: * `POST /containers/create` now takes `PidsLimit` field, if the kernel is >= 4.3 and the pids cgroup is supported.
    133: * `GET /containers/(id or name)/stats` now returns `pids_stats`, if the kernel is >= 4.3 and the pids cgroup is supported.
    134: * `POST /containers/create` now allows you to override usernamespaces remapping and use privileged options for the container.
    135: * `POST /containers/create` now allows specifying `nocopy` for named volumes, which disables automatic copying from the container path to the volume.
    136: * `POST /auth` now returns an `IdentityToken` when supported by a registry.
    137: * `POST /containers/create` with both `Hostname` and `Domainname` fields specified will result in the container's hostname being set to `Hostname`, rather than `Hostname.Domainname`.
    138: * `GET /volumes` now supports more filters, new added filters are `name` and `driver`.
    139: * `GET /containers/(id or name)/logs` now accepts a `details` query parameter to stream the extra attributes that were provided to the containers `LogOpts`, such as environment variables and labels, with the logs.
    140: * `POST /images/load` now returns progress information as a JSON stream, and has a `quiet` query parameter to suppress progress details.
    141: 
    142: ## v1.22 API changes
    143: 
    144: [Docker Engine API v1.22](v1.22.md) documentation
    145: 
    146: * `POST /container/(name)/update` updates the resources of a container.
    147: * `GET /containers/json` supports filter `isolation` on Windows.
    148: * `GET /containers/json` now returns the list of networks of containers.
    149: * `GET /info` Now returns `Architecture` and `OSType` fields, providing information
    150:   about the host architecture and operating system type that the daemon runs on.
    151: * `GET /networks/(name)` now returns a `Name` field for each container attached to the network.
    152: * `GET /version` now returns the `BuildTime` field in RFC3339Nano format to make it
    153:   consistent with other date/time values returned by the API.
    154: * `AuthConfig` now supports a `registrytoken` for token based authentication
    155: * `POST /containers/create` now has a 4M minimum value limit for `HostConfig.KernelMemory`
    156: * Pushes initiated with `POST /images/(name)/push` and pulls initiated with `POST /images/create`
    157:   will be cancelled if the HTTP connection making the API request is closed before
    158:   the push or pull completes.
    159: * `POST /containers/create` now allows you to set a read/write rate limit for a
    160:   device (in bytes per second or IO per second).
    161: * `GET /networks` now supports filtering by `name`, `id` and `type`.
    162: * `POST /containers/create` now allows you to set the static IPv4 and/or IPv6 address for the container.
    163: * `POST /networks/(id)/connect` now allows you to set the static IPv4 and/or IPv6 address for the container.
    164: * `GET /info` now includes the number of containers running, stopped, and paused.
    165: * `POST /networks/create` now supports restricting external access to the network by setting the `Internal` field.
    166: * `POST /networks/(id)/disconnect` now includes a `Force` option to forcefully disconnect a container from network
    167: * `GET /containers/(id)/json` now returns the `NetworkID` of containers.
    168: * `POST /networks/create` Now supports an options field in the IPAM config that provides options
    169:   for custom IPAM plugins.
    170: * `GET /networks/{network-id}` Now returns IPAM config options for custom IPAM plugins if any
    171:   are available.
    172: * `GET /networks/<network-id>` now returns subnets info for user-defined networks.
    173: * `GET /info` can now return a `SystemStatus` field useful for returning additional information about applications
    174:   that are built on top of engine.
    175: 
    176: ## v1.21 API changes
    177: 
    178: [Docker Engine API v1.21](v1.21.md) documentation
    179: 
    180: * `GET /volumes` lists volumes from all volume drivers.
    181: * `POST /volumes/create` to create a volume.
    182: * `GET /volumes/(name)` get low-level information about a volume.
    183: * `DELETE /volumes/(name)` remove a volume with the specified name.
    184: * `VolumeDriver` was moved from `config` to `HostConfig` to make the configuration portable.
    185: * `GET /images/(name)/json` now returns information about an image's `RepoTags` and `RepoDigests`.
    186: * The `config` option now accepts the field `StopSignal`, which specifies the signal to use to kill a container.
    187: * `GET /containers/(id)/stats` will return networking information respectively for each interface.
    188: * The `HostConfig` option now includes the `DnsOptions` field to configure the container's DNS options.
    189: * `POST /build` now optionally takes a serialized map of build-time variables.
    190: * `GET /events` now includes a `timenano` field, in addition to the existing `time` field.
    191: * `GET /events` now supports filtering by image and container labels.
    192: * `GET /info` now lists engine version information and return the information of `CPUShares` and `Cpuset`.
    193: * `GET /containers/json` will return `ImageID` of the image used by container.
    194: * `POST /exec/(name)/start` will now return an HTTP 409 when the container is either stopped or paused.
    195: * `POST /containers/create` now takes `KernelMemory` in HostConfig to specify kernel memory limit.
    196: * `GET /containers/(name)/json` now accepts a `size` parameter. Setting this parameter to '1' returns container size information in the `SizeRw` and `SizeRootFs` fields.
    197: * `GET /containers/(name)/json` now returns a `NetworkSettings.Networks` field,
    198:   detailing network settings per network. This field deprecates the
    199:   `NetworkSettings.Gateway`, `NetworkSettings.IPAddress`,
    200:   `NetworkSettings.IPPrefixLen`, and `NetworkSettings.MacAddress` fields, which
    201:   are still returned for backward-compatibility, but will be removed in a future version.
    202: * `GET /exec/(id)/json` now returns a `NetworkSettings.Networks` field,
    203:   detailing networksettings per network. This field deprecates the
    204:   `NetworkSettings.Gateway`, `NetworkSettings.IPAddress`,
    205:   `NetworkSettings.IPPrefixLen`, and `NetworkSettings.MacAddress` fields, which
    206:   are still returned for backward-compatibility, but will be removed in a future version.
    207: * The `HostConfig` option now includes the `OomScoreAdj` field for adjusting the
    208:   badness heuristic. This heuristic selects which processes the OOM killer kills
    209:   under out-of-memory conditions.
    210: 
    211: ## v1.20 API changes
    212: 
    213: [Docker Engine API v1.20](v1.20.md) documentation
    214: 
    215: * `GET /containers/(id)/archive` get an archive of filesystem content from a container.
    216: * `PUT /containers/(id)/archive` upload an archive of content to be extracted to
    217: an existing directory inside a container's filesystem.
    218: * `POST /containers/(id)/copy` is deprecated in favor of the above `archive`
    219: endpoint which can be used to download files and directories from a container.
    220: * The `hostConfig` option now accepts the field `GroupAdd`, which specifies a
    221: list of additional groups that the container process will run as.
    222: 
    223: ## v1.19 API changes
    224: 
    225: [Docker Engine API v1.19](v1.19.md) documentation
    226: 
    227: * When the daemon detects a version mismatch with the client, usually when
    228: the client is newer than the daemon, an HTTP 400 is now returned instead
    229: of a 404.
    230: * `GET /containers/(id)/stats` now accepts `stream` bool to get only one set of stats and disconnect.
    231: * `GET /containers/(id)/logs` now accepts a `since` timestamp parameter.
    232: * `GET /info` The fields `Debug`, `IPv4Forwarding`, `MemoryLimit`, and
    233: `SwapLimit` are now returned as boolean instead of as an int. In addition, the
    234: end point now returns the new boolean fields `CpuCfsPeriod`, `CpuCfsQuota`, and
    235: `OomKillDisable`.
    236: * The `hostConfig` option now accepts the fields `CpuPeriod` and `CpuQuota`
    237: * `POST /build` accepts `cpuperiod` and `cpuquota` options
    238: 
    239: ## v1.18 API changes
    240: 
    241: [Docker Engine API v1.18](v1.18.md) documentation
    242: 
    243: * `GET /version` now returns `Os`, `Arch` and `KernelVersion`.
    244: * `POST /containers/create` and `POST /containers/(id)/start`allow you to  set ulimit settings for use in the container.
    245: * `GET /info` now returns `SystemTime`, `HttpProxy`,`HttpsProxy` and `NoProxy`.
    246: * `GET /images/json` added a `RepoDigests` field to include image digest information.
    247: * `POST /build` can now set resource constraints for all containers created for the build.
    248: * `CgroupParent` can be passed in the host config to setup container cgroups under a specific cgroup.
    249: * `POST /build` closing the HTTP request cancels the build
    250: * `POST /containers/(id)/exec` includes `Warnings` field to response.

```

Output: raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.tickets.md
```
snapshot: raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt
sha256: d5cfeba8e2effb279f33fac41e317078f4460f921d9ef7379927d2ab5dd792b6
source_url: https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md
body_range: 1-250
line_numbers: snapshot

## Ticket 1

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /plugins/(plugin name)/upgrade` upgrade a plugin. | 20 | * `POST /plugins/(plugin name)/upgrade` upgrade a plugin. |
| affected_surface | `POST /plugins/(plugin name)/upgrade` | 20 | * `POST /plugins/(plugin name)/upgrade` upgrade a plugin. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 20 |  |

## Ticket 2

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The API version is now required in all API calls. Instead of just requesting, for example, the URL `/containers/json`, you must now request `/v1.25/containers/json`. | 26 | * The API version is now required in all API calls. Instead of just requesting, for example, the URL `/containers/json`, you must now request `/v1.25/containers/json`. |
| affected_surface | `/containers/json` | 26 | * The API version is now required in all API calls. Instead of just requesting, for example, the URL `/containers/json`, you must now request `/v1.25/containers/json`. |
| affected_surface | `/v1.25/containers/json` | 26 | * The API version is now required in all API calls. Instead of just requesting, for example, the URL `/containers/json`, you must now request `/v1.25/containers/json`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | Instead of just requesting, for example, the URL `/containers/json`, you must now request `/v1.25/containers/json`. | 26 | * The API version is now required in all API calls. Instead of just requesting, for example, the URL `/containers/json`, you must now request `/v1.25/containers/json`. |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 26 |  |

## Ticket 3

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /version` now returns `MinAPIVersion`. | 27 | * `GET /version` now returns `MinAPIVersion`. |
| affected_surface | `GET /version` | 27 | * `GET /version` now returns `MinAPIVersion`. |
| affected_surface | `MinAPIVersion` | 27 | * `GET /version` now returns `MinAPIVersion`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 27 |  |

## Ticket 4

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /build` accepts `networkmode` parameter to specify network used during build. | 28 | * `POST /build` accepts `networkmode` parameter to specify network used during build. |
| affected_surface | `POST /build` | 28 | * `POST /build` accepts `networkmode` parameter to specify network used during build. |
| affected_surface | `networkmode` | 28 | * `POST /build` accepts `networkmode` parameter to specify network used during build. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 28 |  |

## Ticket 5

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /images/(name)/json` now returns `OsVersion` if populated | 29 | * `GET /images/(name)/json` now returns `OsVersion` if populated |
| affected_surface | `GET /images/(name)/json` | 29 | * `GET /images/(name)/json` now returns `OsVersion` if populated |
| affected_surface | `OsVersion` | 29 | * `GET /images/(name)/json` now returns `OsVersion` if populated |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 29 |  |

## Ticket 6

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` now returns `Isolation`. | 30 | * `GET /info` now returns `Isolation`. |
| affected_surface | `GET /info` | 30 | * `GET /info` now returns `Isolation`. |
| affected_surface | `Isolation` | 30 | * `GET /info` now returns `Isolation`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 30 |  |

## Ticket 7

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now takes `AutoRemove` in HostConfig, to enable auto-removal of the container on daemon side when the container's process exits. | 31 | * `POST /containers/create` now takes `AutoRemove` in HostConfig, to enable auto-removal of the container on daemon side when the container's process exits. |
| affected_surface | `POST /containers/create` | 31 | * `POST /containers/create` now takes `AutoRemove` in HostConfig, to enable auto-removal of the container on daemon side when the container's process exits. |
| affected_surface | `AutoRemove` | 31 | * `POST /containers/create` now takes `AutoRemove` in HostConfig, to enable auto-removal of the container on daemon side when the container's process exits. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 31 |  |

## Ticket 8

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/json` and `GET /containers/(id or name)/json` now return `"removing"` as a value for the `State.Status` field if the container is being removed. Previously, "exited" was returned as status. | 32 | * `GET /containers/json` and `GET /containers/(id or name)/json` now return `"removing"` as a value for the `State.Status` field if the container is being removed. Previously, "exited" was returned as status. |
| affected_surface | `GET /containers/json` | 32 | * `GET /containers/json` and `GET /containers/(id or name)/json` now return `"removing"` as a value for the `State.Status` field if the container is being removed. Previously, "exited" was returned as status. |
| affected_surface | `GET /containers/(id or name)/json` | 32 | * `GET /containers/json` and `GET /containers/(id or name)/json` now return `"removing"` as a value for the `State.Status` field if the container is being removed. Previously, "exited" was returned as status. |
| affected_surface | `"removing"` | 32 | * `GET /containers/json` and `GET /containers/(id or name)/json` now return `"removing"` as a value for the `State.Status` field if the container is being removed. Previously, "exited" was returned as status. |
| affected_surface | `State.Status` | 32 | * `GET /containers/json` and `GET /containers/(id or name)/json` now return `"removing"` as a value for the `State.Status` field if the container is being removed. Previously, "exited" was returned as status. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 32 |  |

## Ticket 9

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/json` now accepts `removing` as a valid value for the `status` filter. | 33 | * `GET /containers/json` now accepts `removing` as a valid value for the `status` filter. |
| affected_surface | `GET /containers/json` | 33 | * `GET /containers/json` now accepts `removing` as a valid value for the `status` filter. |
| affected_surface | `removing` | 33 | * `GET /containers/json` now accepts `removing` as a valid value for the `status` filter. |
| affected_surface | `status` | 33 | * `GET /containers/json` now accepts `removing` as a valid value for the `status` filter. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 33 |  |

## Ticket 10

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/json` now supports filtering containers by `health` status. | 34 | * `GET /containers/json` now supports filtering containers by `health` status. |
| affected_surface | `GET /containers/json` | 34 | * `GET /containers/json` now supports filtering containers by `health` status. |
| affected_surface | `health` | 34 | * `GET /containers/json` now supports filtering containers by `health` status. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 34 |  |

## Ticket 11

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `DELETE /volumes/(name)` now accepts a `force` query parameter to force removal of volumes that were already removed out of band by the volume driver plugin. | 35 | * `DELETE /volumes/(name)` now accepts a `force` query parameter to force removal of volumes that were already removed out of band by the volume driver plugin. |
| affected_surface | `DELETE /volumes/(name)` | 35 | * `DELETE /volumes/(name)` now accepts a `force` query parameter to force removal of volumes that were already removed out of band by the volume driver plugin. |
| affected_surface | `force` | 35 | * `DELETE /volumes/(name)` now accepts a `force` query parameter to force removal of volumes that were already removed out of band by the volume driver plugin. |
| affected_surface | query | 35 | * `DELETE /volumes/(name)` now accepts a `force` query parameter to force removal of volumes that were already removed out of band by the volume driver plugin. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 35 |  |

## Ticket 12

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create/` and `POST /containers/(name)/update` now validates restart policies. | 36 | * `POST /containers/create/` and `POST /containers/(name)/update` now validates restart policies. |
| affected_surface | `POST /containers/create/` | 36 | * `POST /containers/create/` and `POST /containers/(name)/update` now validates restart policies. |
| affected_surface | `POST /containers/(name)/update` | 36 | * `POST /containers/create/` and `POST /containers/(name)/update` now validates restart policies. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 36 |  |

## Ticket 13

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now validates IPAMConfig in NetworkingConfig, and returns error for invalid IPv4 and IPv6 addresses (`--ip` and `--ip6` in `docker create/run`). | 37 | * `POST /containers/create` now validates IPAMConfig in NetworkingConfig, and returns error for invalid IPv4 and IPv6 addresses (`--ip` and `--ip6` in `docker create/run`). |
| affected_surface | `POST /containers/create` | 37 | * `POST /containers/create` now validates IPAMConfig in NetworkingConfig, and returns error for invalid IPv4 and IPv6 addresses (`--ip` and `--ip6` in `docker create/run`). |
| affected_surface | `--ip` | 37 | * `POST /containers/create` now validates IPAMConfig in NetworkingConfig, and returns error for invalid IPv4 and IPv6 addresses (`--ip` and `--ip6` in `docker create/run`). |
| affected_surface | `--ip6` | 37 | * `POST /containers/create` now validates IPAMConfig in NetworkingConfig, and returns error for invalid IPv4 and IPv6 addresses (`--ip` and `--ip6` in `docker create/run`). |
| affected_surface | `docker create/run` | 37 | * `POST /containers/create` now validates IPAMConfig in NetworkingConfig, and returns error for invalid IPv4 and IPv6 addresses (`--ip` and `--ip6` in `docker create/run`). |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 37 |  |

## Ticket 14

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now takes a `Mounts` field in `HostConfig` which replaces `Binds`, `Volumes`, and `Tmpfs`. *note*: `Binds`, `Volumes`, and `Tmpfs` are still available and can be combined with `Mounts`. | 38 | * `POST /containers/create` now takes a `Mounts` field in `HostConfig` which replaces `Binds`, `Volumes`, and `Tmpfs`. *note*: `Binds`, `Volumes`, and `Tmpfs` are still available and can be combined with `Mounts`. |
| affected_surface | `POST /containers/create` | 38 | * `POST /containers/create` now takes a `Mounts` field in `HostConfig` which replaces `Binds`, `Volumes`, and `Tmpfs`. *note*: `Binds`, `Volumes`, and `Tmpfs` are still available and can be combined with `Mounts`. |
| affected_surface | `Mounts` | 38 | * `POST /containers/create` now takes a `Mounts` field in `HostConfig` which replaces `Binds`, `Volumes`, and `Tmpfs`. *note*: `Binds`, `Volumes`, and `Tmpfs` are still available and can be combined with `Mounts`. |
| affected_surface | `HostConfig` | 38 | * `POST /containers/create` now takes a `Mounts` field in `HostConfig` which replaces `Binds`, `Volumes`, and `Tmpfs`. *note*: `Binds`, `Volumes`, and `Tmpfs` are still available and can be combined with `Mounts`. |
| affected_surface | `Binds` | 38 | * `POST /containers/create` now takes a `Mounts` field in `HostConfig` which replaces `Binds`, `Volumes`, and `Tmpfs`. *note*: `Binds`, `Volumes`, and `Tmpfs` are still available and can be combined with `Mounts`. |
| affected_surface | `Volumes` | 38 | * `POST /containers/create` now takes a `Mounts` field in `HostConfig` which replaces `Binds`, `Volumes`, and `Tmpfs`. *note*: `Binds`, `Volumes`, and `Tmpfs` are still available and can be combined with `Mounts`. |
| affected_surface | `Tmpfs` | 38 | * `POST /containers/create` now takes a `Mounts` field in `HostConfig` which replaces `Binds`, `Volumes`, and `Tmpfs`. *note*: `Binds`, `Volumes`, and `Tmpfs` are still available and can be combined with `Mounts`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 38 |  |

## Ticket 15

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /build` now performs a preliminary validation of the `Dockerfile` before starting the build, and returns an error if the syntax is incorrect. Note that this change is _unversioned_ and applied to all API versions. | 39 | * `POST /build` now performs a preliminary validation of the `Dockerfile` before starting the build, and returns an error if the syntax is incorrect. Note that this change is _unversioned_ and applied to all API versions. |
| affected_surface | `POST /build` | 39 | * `POST /build` now performs a preliminary validation of the `Dockerfile` before starting the build, and returns an error if the syntax is incorrect. Note that this change is _unversioned_ and applied to all API versions. |
| affected_surface | `Dockerfile` | 39 | * `POST /build` now performs a preliminary validation of the `Dockerfile` before starting the build, and returns an error if the syntax is incorrect. Note that this change is _unversioned_ and applied to all API versions. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 39 |  |

## Ticket 16

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /build` accepts `cachefrom` parameter to specify images used for build cache. | 40 | * `POST /build` accepts `cachefrom` parameter to specify images used for build cache. |
| affected_surface | `POST /build` | 40 | * `POST /build` accepts `cachefrom` parameter to specify images used for build cache. |
| affected_surface | `cachefrom` | 40 | * `POST /build` accepts `cachefrom` parameter to specify images used for build cache. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 40 |  |

## Ticket 17

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /networks/` endpoint now correctly returns a list of *all* networks, | 41 | * `GET /networks/` endpoint now correctly returns a list of *all* networks, |
| affected_surface | `GET /networks/` | 41 | * `GET /networks/` endpoint now correctly returns a list of *all* networks, |
| affected_surface | `name` | 42 | instead of the default network if a trailing slash is provided, but no `name` |
| affected_surface | `id` | 43 | or `id`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 41-43 |  |

## Ticket 18

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `DELETE /containers/(name)` endpoint now returns an error of `removal of container name is already in progress` with status code of 400, when container name is in a state of removal in progress. | 44 | * `DELETE /containers/(name)` endpoint now returns an error of `removal of container name is already in progress` with status code of 400, when container name is in a state of removal in progress. |
| affected_surface | `DELETE /containers/(name)` | 44 | * `DELETE /containers/(name)` endpoint now returns an error of `removal of container name is already in progress` with status code of 400, when container name is in a state of removal in progress. |
| affected_surface | `removal of container name is already in progress` | 44 | * `DELETE /containers/(name)` endpoint now returns an error of `removal of container name is already in progress` with status code of 400, when container name is in a state of removal in progress. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 44 |  |

## Ticket 19

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/json` now supports a `is-task` filter to filter | 45 | * `GET /containers/json` now supports a `is-task` filter to filter |
| affected_surface | `GET /containers/json` | 45 | * `GET /containers/json` now supports a `is-task` filter to filter |
| affected_surface | `is-task` | 45 | * `GET /containers/json` now supports a `is-task` filter to filter |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 45-46 |  |

## Ticket 20

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now takes `StopTimeout` field. | 47 | * `POST /containers/create` now takes `StopTimeout` field. |
| affected_surface | `POST /containers/create` | 47 | * `POST /containers/create` now takes `StopTimeout` field. |
| affected_surface | `StopTimeout` | 47 | * `POST /containers/create` now takes `StopTimeout` field. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 47 |  |

## Ticket 21

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /services/create` and `POST /services/(id or name)/update` now accept `Monitor` and `MaxFailureRatio` parameters, which control the response to failures during service updates. | 48 | * `POST /services/create` and `POST /services/(id or name)/update` now accept `Monitor` and `MaxFailureRatio` parameters, which control the response to failures during service updates. |
| affected_surface | `POST /services/create` | 48 | * `POST /services/create` and `POST /services/(id or name)/update` now accept `Monitor` and `MaxFailureRatio` parameters, which control the response to failures during service updates. |
| affected_surface | `POST /services/(id or name)/update` | 48 | * `POST /services/create` and `POST /services/(id or name)/update` now accept `Monitor` and `MaxFailureRatio` parameters, which control the response to failures during service updates. |
| affected_surface | `Monitor` | 48 | * `POST /services/create` and `POST /services/(id or name)/update` now accept `Monitor` and `MaxFailureRatio` parameters, which control the response to failures during service updates. |
| affected_surface | `MaxFailureRatio` | 48 | * `POST /services/create` and `POST /services/(id or name)/update` now accept `Monitor` and `MaxFailureRatio` parameters, which control the response to failures during service updates. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 48 |  |

## Ticket 22

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /services/(id or name)/update` now accepts a `ForceUpdate` parameter inside the `TaskTemplate`, which causes the service to be updated even if there are no changes which would ordinarily trigger an update. | 49 | * `POST /services/(id or name)/update` now accepts a `ForceUpdate` parameter inside the `TaskTemplate`, which causes the service to be updated even if there are no changes which would ordinarily trigger an update. |
| affected_surface | `POST /services/(id or name)/update` | 49 | * `POST /services/(id or name)/update` now accepts a `ForceUpdate` parameter inside the `TaskTemplate`, which causes the service to be updated even if there are no changes which would ordinarily trigger an update. |
| affected_surface | `ForceUpdate` | 49 | * `POST /services/(id or name)/update` now accepts a `ForceUpdate` parameter inside the `TaskTemplate`, which causes the service to be updated even if there are no changes which would ordinarily trigger an update. |
| affected_surface | `TaskTemplate` | 49 | * `POST /services/(id or name)/update` now accepts a `ForceUpdate` parameter inside the `TaskTemplate`, which causes the service to be updated even if there are no changes which would ordinarily trigger an update. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 49 |  |

## Ticket 23

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /services/create` and `POST /services/(id or name)/update` now return a `Warnings` array. | 50 | * `POST /services/create` and `POST /services/(id or name)/update` now return a `Warnings` array. |
| affected_surface | `POST /services/create` | 50 | * `POST /services/create` and `POST /services/(id or name)/update` now return a `Warnings` array. |
| affected_surface | `POST /services/(id or name)/update` | 50 | * `POST /services/create` and `POST /services/(id or name)/update` now return a `Warnings` array. |
| affected_surface | `Warnings` | 50 | * `POST /services/create` and `POST /services/(id or name)/update` now return a `Warnings` array. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 50 |  |

## Ticket 24

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /networks/(name)` now returns field `Created` in response to show network created time. | 51 | * `GET /networks/(name)` now returns field `Created` in response to show network created time. |
| affected_surface | `GET /networks/(name)` | 51 | * `GET /networks/(name)` now returns field `Created` in response to show network created time. |
| affected_surface | returns | 51 | * `GET /networks/(name)` now returns field `Created` in response to show network created time. |
| affected_surface | `Created` | 51 | * `GET /networks/(name)` now returns field `Created` in response to show network created time. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 51 |  |

## Ticket 25

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/(id or name)/exec` now accepts an `Env` field, which holds a list of environment variables to be set in the context of the command execution. | 52 | * `POST /containers/(id or name)/exec` now accepts an `Env` field, which holds a list of environment variables to be set in the context of the command execution. |
| affected_surface | `POST /containers/(id or name)/exec` | 52 | * `POST /containers/(id or name)/exec` now accepts an `Env` field, which holds a list of environment variables to be set in the context of the command execution. |
| affected_surface | `Env` | 52 | * `POST /containers/(id or name)/exec` now accepts an `Env` field, which holds a list of environment variables to be set in the context of the command execution. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 52 |  |

## Ticket 26

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /volumes`, `GET /volumes/(name)`, and `POST /volumes/create` now return the `Options` field which holds the driver specific options to use for when creating the volume. | 53 | * `GET /volumes`, `GET /volumes/(name)`, and `POST /volumes/create` now return the `Options` field which holds the driver specific options to use for when creating the volume. |
| affected_surface | `GET /volumes` | 53 | * `GET /volumes`, `GET /volumes/(name)`, and `POST /volumes/create` now return the `Options` field which holds the driver specific options to use for when creating the volume. |
| affected_surface | `GET /volumes/(name)` | 53 | * `GET /volumes`, `GET /volumes/(name)`, and `POST /volumes/create` now return the `Options` field which holds the driver specific options to use for when creating the volume. |
| affected_surface | `POST /volumes/create` | 53 | * `GET /volumes`, `GET /volumes/(name)`, and `POST /volumes/create` now return the `Options` field which holds the driver specific options to use for when creating the volume. |
| affected_surface | `Options` | 53 | * `GET /volumes`, `GET /volumes/(name)`, and `POST /volumes/create` now return the `Options` field which holds the driver specific options to use for when creating the volume. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 53 |  |

## Ticket 27

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /exec/(id)/json` now returns `Pid`, which is the system pid for the exec'd process. | 54 | * `GET /exec/(id)/json` now returns `Pid`, which is the system pid for the exec'd process. |
| affected_surface | `GET /exec/(id)/json` | 54 | * `GET /exec/(id)/json` now returns `Pid`, which is the system pid for the exec'd process. |
| affected_surface | `Pid` | 54 | * `GET /exec/(id)/json` now returns `Pid`, which is the system pid for the exec'd process. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 54 |  |

## Ticket 28

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/prune` prunes stopped containers. | 55 | * `POST /containers/prune` prunes stopped containers. |
| affected_surface | `POST /containers/prune` | 55 | * `POST /containers/prune` prunes stopped containers. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 55 |  |

## Ticket 29

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /images/prune` prunes unused images. | 56 | * `POST /images/prune` prunes unused images. |
| affected_surface | `POST /images/prune` | 56 | * `POST /images/prune` prunes unused images. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 56 |  |

## Ticket 30

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /volumes/prune` prunes unused volumes. | 57 | * `POST /volumes/prune` prunes unused volumes. |
| affected_surface | `POST /volumes/prune` | 57 | * `POST /volumes/prune` prunes unused volumes. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 57 |  |

## Ticket 31

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /networks/prune` prunes unused networks. | 58 | * `POST /networks/prune` prunes unused networks. |
| affected_surface | `POST /networks/prune` | 58 | * `POST /networks/prune` prunes unused networks. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 58 |  |

## Ticket 32

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Every API response now includes a `Docker-Experimental` header specifying if experimental features are enabled (value can be `true` or `false`). | 59 | * Every API response now includes a `Docker-Experimental` header specifying if experimental features are enabled (value can be `true` or `false`). |
| affected_surface | `Docker-Experimental` | 59 | * Every API response now includes a `Docker-Experimental` header specifying if experimental features are enabled (value can be `true` or `false`). |
| affected_surface | `true` | 59 | * Every API response now includes a `Docker-Experimental` header specifying if experimental features are enabled (value can be `true` or `false`). |
| affected_surface | `false` | 59 | * Every API response now includes a `Docker-Experimental` header specifying if experimental features are enabled (value can be `true` or `false`). |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 59 |  |

## Ticket 33

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Every API response now includes a `API-Version` header specifying the default API version of the server. | 60 | * Every API response now includes a `API-Version` header specifying the default API version of the server. |
| affected_surface | `API-Version` | 60 | * Every API response now includes a `API-Version` header specifying the default API version of the server. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 60 |  |

## Ticket 34

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The `hostConfig` option now accepts the fields `CpuRealtimePeriod` and `CpuRtRuntime` to allocate cpu runtime to rt tasks when `CONFIG_RT_GROUP_SCHED` is enabled in the kernel. | 61 | * The `hostConfig` option now accepts the fields `CpuRealtimePeriod` and `CpuRtRuntime` to allocate cpu runtime to rt tasks when `CONFIG_RT_GROUP_SCHED` is enabled in the kernel. |
| affected_surface | `hostConfig` | 61 | * The `hostConfig` option now accepts the fields `CpuRealtimePeriod` and `CpuRtRuntime` to allocate cpu runtime to rt tasks when `CONFIG_RT_GROUP_SCHED` is enabled in the kernel. |
| affected_surface | `CpuRealtimePeriod` | 61 | * The `hostConfig` option now accepts the fields `CpuRealtimePeriod` and `CpuRtRuntime` to allocate cpu runtime to rt tasks when `CONFIG_RT_GROUP_SCHED` is enabled in the kernel. |
| affected_surface | `CpuRtRuntime` | 61 | * The `hostConfig` option now accepts the fields `CpuRealtimePeriod` and `CpuRtRuntime` to allocate cpu runtime to rt tasks when `CONFIG_RT_GROUP_SCHED` is enabled in the kernel. |
| affected_surface | `CONFIG_RT_GROUP_SCHED` | 61 | * The `hostConfig` option now accepts the fields `CpuRealtimePeriod` and `CpuRtRuntime` to allocate cpu runtime to rt tasks when `CONFIG_RT_GROUP_SCHED` is enabled in the kernel. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 61 |  |

## Ticket 35

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The `SecurityOptions` field within the `GET /info` response now includes `userns` if user namespaces are enabled in the daemon. | 62 | * The `SecurityOptions` field within the `GET /info` response now includes `userns` if user namespaces are enabled in the daemon. |
| affected_surface | `SecurityOptions` | 62 | * The `SecurityOptions` field within the `GET /info` response now includes `userns` if user namespaces are enabled in the daemon. |
| affected_surface | `GET /info` | 62 | * The `SecurityOptions` field within the `GET /info` response now includes `userns` if user namespaces are enabled in the daemon. |
| affected_surface | `userns` | 62 | * The `SecurityOptions` field within the `GET /info` response now includes `userns` if user namespaces are enabled in the daemon. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 62 |  |

## Ticket 36

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /nodes` and `GET /node/(id or name)` now return `Addr` as part of a node's `Status`, which is the address that that node connects to the manager from. | 63 | * `GET /nodes` and `GET /node/(id or name)` now return `Addr` as part of a node's `Status`, which is the address that that node connects to the manager from. |
| affected_surface | `GET /nodes` | 63 | * `GET /nodes` and `GET /node/(id or name)` now return `Addr` as part of a node's `Status`, which is the address that that node connects to the manager from. |
| affected_surface | `GET /node/(id or name)` | 63 | * `GET /nodes` and `GET /node/(id or name)` now return `Addr` as part of a node's `Status`, which is the address that that node connects to the manager from. |
| affected_surface | `Addr` | 63 | * `GET /nodes` and `GET /node/(id or name)` now return `Addr` as part of a node's `Status`, which is the address that that node connects to the manager from. |
| affected_surface | `Status` | 63 | * `GET /nodes` and `GET /node/(id or name)` now return `Addr` as part of a node's `Status`, which is the address that that node connects to the manager from. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 63 |  |

## Ticket 37

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The `HostConfig` field now includes `NanoCPUs` that represents CPU quota in units of 10<sup>-9</sup> CPUs. | 64 | * The `HostConfig` field now includes `NanoCPUs` that represents CPU quota in units of 10<sup>-9</sup> CPUs. |
| affected_surface | `HostConfig` | 64 | * The `HostConfig` field now includes `NanoCPUs` that represents CPU quota in units of 10<sup>-9</sup> CPUs. |
| affected_surface | `NanoCPUs` | 64 | * The `HostConfig` field now includes `NanoCPUs` that represents CPU quota in units of 10<sup>-9</sup> CPUs. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 64 |  |

## Ticket 38

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` now returns more structured information about security options. | 65 | * `GET /info` now returns more structured information about security options. |
| affected_surface | `GET /info` | 65 | * `GET /info` now returns more structured information about security options. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 65 |  |

## Ticket 39

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The `HostConfig` field now includes `CpuCount` that represents the number of CPUs available for execution by the container. Windows daemon only. | 66 | * The `HostConfig` field now includes `CpuCount` that represents the number of CPUs available for execution by the container. Windows daemon only. |
| affected_surface | `HostConfig` | 66 | * The `HostConfig` field now includes `CpuCount` that represents the number of CPUs available for execution by the container. Windows daemon only. |
| affected_surface | `CpuCount` | 66 | * The `HostConfig` field now includes `CpuCount` that represents the number of CPUs available for execution by the container. Windows daemon only. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 66 |  |

## Ticket 40

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /services/create` and `POST /services/(id or name)/update` now accept the `TTY` parameter, which allocate a pseudo-TTY in container. | 67 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `TTY` parameter, which allocate a pseudo-TTY in container. |
| affected_surface | `POST /services/create` | 67 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `TTY` parameter, which allocate a pseudo-TTY in container. |
| affected_surface | `POST /services/(id or name)/update` | 67 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `TTY` parameter, which allocate a pseudo-TTY in container. |
| affected_surface | `TTY` | 67 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `TTY` parameter, which allocate a pseudo-TTY in container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 67 |  |

## Ticket 41

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /services/create` and `POST /services/(id or name)/update` now accept the `DNSConfig` parameter, which specifies DNS related configurations in resolver configuration file (resolv.conf) through `Nameservers`, `Search`, and `Options`. | 68 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `DNSConfig` parameter, which specifies DNS related configurations in resolver configuration file (resolv.conf) through `Nameservers`, `Search`, and `Options`. |
| affected_surface | `POST /services/create` | 68 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `DNSConfig` parameter, which specifies DNS related configurations in resolver configuration file (resolv.conf) through `Nameservers`, `Search`, and `Options`. |
| affected_surface | `POST /services/(id or name)/update` | 68 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `DNSConfig` parameter, which specifies DNS related configurations in resolver configuration file (resolv.conf) through `Nameservers`, `Search`, and `Options`. |
| affected_surface | `DNSConfig` | 68 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `DNSConfig` parameter, which specifies DNS related configurations in resolver configuration file (resolv.conf) through `Nameservers`, `Search`, and `Options`. |
| affected_surface | `Nameservers` | 68 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `DNSConfig` parameter, which specifies DNS related configurations in resolver configuration file (resolv.conf) through `Nameservers`, `Search`, and `Options`. |
| affected_surface | `Search` | 68 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `DNSConfig` parameter, which specifies DNS related configurations in resolver configuration file (resolv.conf) through `Nameservers`, `Search`, and `Options`. |
| affected_surface | `Options` | 68 | * `POST /services/create` and `POST /services/(id or name)/update` now accept the `DNSConfig` parameter, which specifies DNS related configurations in resolver configuration file (resolv.conf) through `Nameservers`, `Search`, and `Options`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 68 |  |

## Ticket 42

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /networks/(id or name)` now includes IP and name of all peers nodes for swarm mode overlay networks. | 69 | * `GET /networks/(id or name)` now includes IP and name of all peers nodes for swarm mode overlay networks. |
| affected_surface | `GET /networks/(id or name)` | 69 | * `GET /networks/(id or name)` now includes IP and name of all peers nodes for swarm mode overlay networks. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 69 |  |

## Ticket 43

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /plugins` list plugins. | 70 | * `GET /plugins` list plugins. |
| affected_surface | `GET /plugins` | 70 | * `GET /plugins` list plugins. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 70 |  |

## Ticket 44

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /plugins/pull?name=<plugin name>` pulls a plugin. | 71 | * `POST /plugins/pull?name=<plugin name>` pulls a plugin. |
| affected_surface | `POST /plugins/pull?name=<plugin name>` | 71 | * `POST /plugins/pull?name=<plugin name>` pulls a plugin. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 71 |  |

## Ticket 45

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /plugins/(plugin name)` inspect a plugin. | 72 | * `GET /plugins/(plugin name)` inspect a plugin. |
| affected_surface | `GET /plugins/(plugin name)` | 72 | * `GET /plugins/(plugin name)` inspect a plugin. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 72 |  |

## Ticket 46

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /plugins/(plugin name)/set` configure a plugin. | 73 | * `POST /plugins/(plugin name)/set` configure a plugin. |
| affected_surface | `POST /plugins/(plugin name)/set` | 73 | * `POST /plugins/(plugin name)/set` configure a plugin. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 73 |  |

## Ticket 47

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /plugins/(plugin name)/enable` enable a plugin. | 74 | * `POST /plugins/(plugin name)/enable` enable a plugin. |
| affected_surface | `POST /plugins/(plugin name)/enable` | 74 | * `POST /plugins/(plugin name)/enable` enable a plugin. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 74 |  |

## Ticket 48

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /plugins/(plugin name)/disable` disable a plugin. | 75 | * `POST /plugins/(plugin name)/disable` disable a plugin. |
| affected_surface | `POST /plugins/(plugin name)/disable` | 75 | * `POST /plugins/(plugin name)/disable` disable a plugin. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 75 |  |

## Ticket 49

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /plugins/(plugin name)/push` push a plugin. | 76 | * `POST /plugins/(plugin name)/push` push a plugin. |
| affected_surface | `POST /plugins/(plugin name)/push` | 76 | * `POST /plugins/(plugin name)/push` push a plugin. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 76 |  |

## Ticket 50

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /plugins/create?name=(plugin name)` create a plugin. | 77 | * `POST /plugins/create?name=(plugin name)` create a plugin. |
| affected_surface | `POST /plugins/create?name=(plugin name)` | 77 | * `POST /plugins/create?name=(plugin name)` create a plugin. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 77 |  |

## Ticket 51

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `DELETE /plugins/(plugin name)` delete a plugin. | 78 | * `DELETE /plugins/(plugin name)` delete a plugin. |
| affected_surface | `DELETE /plugins/(plugin name)` | 78 | * `DELETE /plugins/(plugin name)` delete a plugin. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 78 |  |

## Ticket 52

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /node/(id or name)/update` now accepts both `id` or `name` to identify the node to update. | 79 | * `POST /node/(id or name)/update` now accepts both `id` or `name` to identify the node to update. |
| affected_surface | `POST /node/(id or name)/update` | 79 | * `POST /node/(id or name)/update` now accepts both `id` or `name` to identify the node to update. |
| affected_surface | `id` | 79 | * `POST /node/(id or name)/update` now accepts both `id` or `name` to identify the node to update. |
| affected_surface | `name` | 79 | * `POST /node/(id or name)/update` now accepts both `id` or `name` to identify the node to update. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 79 |  |

## Ticket 53

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /images/json` now support a `reference` filter. | 80 | * `GET /images/json` now support a `reference` filter. |
| affected_surface | `GET /images/json` | 80 | * `GET /images/json` now support a `reference` filter. |
| affected_surface | `reference` | 80 | * `GET /images/json` now support a `reference` filter. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 80 |  |

## Ticket 54

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /secrets` returns information on the secrets. | 81 | * `GET /secrets` returns information on the secrets. |
| affected_surface | `GET /secrets` | 81 | * `GET /secrets` returns information on the secrets. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 81 |  |

## Ticket 55

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /secrets/create` creates a secret. | 82 | * `POST /secrets/create` creates a secret. |
| affected_surface | `POST /secrets/create` | 82 | * `POST /secrets/create` creates a secret. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 82 |  |

## Ticket 56

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `DELETE /secrets/{id}` removes the secret `id`. | 83 | * `DELETE /secrets/{id}` removes the secret `id`. |
| affected_surface | `DELETE /secrets/{id}` | 83 | * `DELETE /secrets/{id}` removes the secret `id`. |
| affected_surface | `id` | 83 | * `DELETE /secrets/{id}` removes the secret `id`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 83 |  |

## Ticket 57

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /secrets/{id}` returns information on the secret `id`. | 84 | * `GET /secrets/{id}` returns information on the secret `id`. |
| affected_surface | `GET /secrets/{id}` | 84 | * `GET /secrets/{id}` returns information on the secret `id`. |
| affected_surface | `id` | 84 | * `GET /secrets/{id}` returns information on the secret `id`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 84 |  |

## Ticket 58

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /secrets/{id}/update` updates the secret `id`. | 85 | * `POST /secrets/{id}/update` updates the secret `id`. |
| affected_surface | `POST /secrets/{id}/update` | 85 | * `POST /secrets/{id}/update` updates the secret `id`. |
| affected_surface | `id` | 85 | * `POST /secrets/{id}/update` updates the secret `id`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 85 |  |

## Ticket 59

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /services/(id or name)/update` now accepts service name or prefix of service id as a parameter. | 86 | * `POST /services/(id or name)/update` now accepts service name or prefix of service id as a parameter. |
| affected_surface | `POST /services/(id or name)/update` | 86 | * `POST /services/(id or name)/update` now accepts service name or prefix of service id as a parameter. |
| affected_surface | a | 86 | * `POST /services/(id or name)/update` now accepts service name or prefix of service id as a parameter. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 86 |  |

## Ticket 60

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now takes `StorageOpt` field. | 92 | * `POST /containers/create` now takes `StorageOpt` field. |
| affected_surface | `POST /containers/create` | 92 | * `POST /containers/create` now takes `StorageOpt` field. |
| affected_surface | `StorageOpt` | 92 | * `POST /containers/create` now takes `StorageOpt` field. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 92 |  |

## Ticket 61

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` now returns `SecurityOptions` field, showing if `apparmor`, `seccomp`, or `selinux` is supported. | 93 | * `GET /info` now returns `SecurityOptions` field, showing if `apparmor`, `seccomp`, or `selinux` is supported. |
| affected_surface | `GET /info` | 93 | * `GET /info` now returns `SecurityOptions` field, showing if `apparmor`, `seccomp`, or `selinux` is supported. |
| affected_surface | `SecurityOptions` | 93 | * `GET /info` now returns `SecurityOptions` field, showing if `apparmor`, `seccomp`, or `selinux` is supported. |
| affected_surface | `apparmor` | 93 | * `GET /info` now returns `SecurityOptions` field, showing if `apparmor`, `seccomp`, or `selinux` is supported. |
| affected_surface | `seccomp` | 93 | * `GET /info` now returns `SecurityOptions` field, showing if `apparmor`, `seccomp`, or `selinux` is supported. |
| affected_surface | `selinux` | 93 | * `GET /info` now returns `SecurityOptions` field, showing if `apparmor`, `seccomp`, or `selinux` is supported. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 93 |  |

## Ticket 62

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` no longer returns the `ExecutionDriver` property. This property was no longer used after integration | 94 | * `GET /info` no longer returns the `ExecutionDriver` property. This property was no longer used after integration |
| affected_surface | `GET /info` | 94 | * `GET /info` no longer returns the `ExecutionDriver` property. This property was no longer used after integration |
| affected_surface | `ExecutionDriver` | 94 | * `GET /info` no longer returns the `ExecutionDriver` property. This property was no longer used after integration |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 94-95 |  |

## Ticket 63

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /networks` now supports filtering by `label` and `driver`. | 96 | * `GET /networks` now supports filtering by `label` and `driver`. |
| affected_surface | `GET /networks` | 96 | * `GET /networks` now supports filtering by `label` and `driver`. |
| affected_surface | `label` | 96 | * `GET /networks` now supports filtering by `label` and `driver`. |
| affected_surface | `driver` | 96 | * `GET /networks` now supports filtering by `label` and `driver`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 96 |  |

## Ticket 64

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/json` now supports filtering containers by `network` name or id. | 97 | * `GET /containers/json` now supports filtering containers by `network` name or id. |
| affected_surface | `GET /containers/json` | 97 | * `GET /containers/json` now supports filtering containers by `network` name or id. |
| affected_surface | `network` | 97 | * `GET /containers/json` now supports filtering containers by `network` name or id. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 97 |  |

## Ticket 65

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now takes `IOMaximumBandwidth` and `IOMaximumIOps` fields. Windows daemon only. | 98 | * `POST /containers/create` now takes `IOMaximumBandwidth` and `IOMaximumIOps` fields. Windows daemon only. |
| affected_surface | `POST /containers/create` | 98 | * `POST /containers/create` now takes `IOMaximumBandwidth` and `IOMaximumIOps` fields. Windows daemon only. |
| affected_surface | `IOMaximumBandwidth` | 98 | * `POST /containers/create` now takes `IOMaximumBandwidth` and `IOMaximumIOps` fields. Windows daemon only. |
| affected_surface | `IOMaximumIOps` | 98 | * `POST /containers/create` now takes `IOMaximumBandwidth` and `IOMaximumIOps` fields. Windows daemon only. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 98 |  |

## Ticket 66

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now returns an HTTP 400 "bad parameter" message | 99 | * `POST /containers/create` now returns an HTTP 400 "bad parameter" message |
| affected_surface | `POST /containers/create` | 99 | * `POST /containers/create` now returns an HTTP 400 "bad parameter" message |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 99-100 |  |

## Ticket 67

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /images/search` now takes a `filters` query parameter. | 101 | * `GET /images/search` now takes a `filters` query parameter. |
| affected_surface | `GET /images/search` | 101 | * `GET /images/search` now takes a `filters` query parameter. |
| affected_surface | `filters` | 101 | * `GET /images/search` now takes a `filters` query parameter. |
| affected_surface | query | 101 | * `GET /images/search` now takes a `filters` query parameter. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 101 |  |

## Ticket 68

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /events` now supports a `reload` event that is emitted when the daemon configuration is reloaded. | 102 | * `GET /events` now supports a `reload` event that is emitted when the daemon configuration is reloaded. |
| affected_surface | `GET /events` | 102 | * `GET /events` now supports a `reload` event that is emitted when the daemon configuration is reloaded. |
| affected_surface | `reload` | 102 | * `GET /events` now supports a `reload` event that is emitted when the daemon configuration is reloaded. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 102 |  |

## Ticket 69

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /events` now supports filtering by daemon name or ID. | 103 | * `GET /events` now supports filtering by daemon name or ID. |
| affected_surface | `GET /events` | 103 | * `GET /events` now supports filtering by daemon name or ID. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 103 |  |

## Ticket 70

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /events` now supports a `detach` event that is emitted on detaching from container process. | 104 | * `GET /events` now supports a `detach` event that is emitted on detaching from container process. |
| affected_surface | `GET /events` | 104 | * `GET /events` now supports a `detach` event that is emitted on detaching from container process. |
| affected_surface | `detach` | 104 | * `GET /events` now supports a `detach` event that is emitted on detaching from container process. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 104 |  |

## Ticket 71

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /events` now supports an `exec_detach ` event that is emitted on detaching from exec process. | 105 | * `GET /events` now supports an `exec_detach ` event that is emitted on detaching from exec process. |
| affected_surface | `GET /events` | 105 | * `GET /events` now supports an `exec_detach ` event that is emitted on detaching from exec process. |
| affected_surface | `exec_detach ` | 105 | * `GET /events` now supports an `exec_detach ` event that is emitted on detaching from exec process. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 105 |  |

## Ticket 72

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /images/json` now supports filters `since` and `before`. | 106 | * `GET /images/json` now supports filters `since` and `before`. |
| affected_surface | `GET /images/json` | 106 | * `GET /images/json` now supports filters `since` and `before`. |
| affected_surface | `since` | 106 | * `GET /images/json` now supports filters `since` and `before`. |
| affected_surface | `before` | 106 | * `GET /images/json` now supports filters `since` and `before`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 106 |  |

## Ticket 73

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/(id or name)/start` no longer accepts a `HostConfig`. | 107 | * `POST /containers/(id or name)/start` no longer accepts a `HostConfig`. |
| affected_surface | `POST /containers/(id or name)/start` | 107 | * `POST /containers/(id or name)/start` no longer accepts a `HostConfig`. |
| affected_surface | `HostConfig` | 107 | * `POST /containers/(id or name)/start` no longer accepts a `HostConfig`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 107 |  |

## Ticket 74

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /images/(name)/tag` no longer has a `force` query parameter. | 108 | * `POST /images/(name)/tag` no longer has a `force` query parameter. |
| affected_surface | `POST /images/(name)/tag` | 108 | * `POST /images/(name)/tag` no longer has a `force` query parameter. |
| affected_surface | `force` | 108 | * `POST /images/(name)/tag` no longer has a `force` query parameter. |
| affected_surface | query | 108 | * `POST /images/(name)/tag` no longer has a `force` query parameter. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 108 |  |

## Ticket 75

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /images/search` now supports maximum returned search results `limit`. | 109 | * `GET /images/search` now supports maximum returned search results `limit`. |
| affected_surface | `GET /images/search` | 109 | * `GET /images/search` now supports maximum returned search results `limit`. |
| affected_surface | `limit` | 109 | * `GET /images/search` now supports maximum returned search results `limit`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 109 |  |

## Ticket 76

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/{name:.*}/copy` is now removed and errors out starting from this API version. | 110 | * `POST /containers/{name:.*}/copy` is now removed and errors out starting from this API version. |
| affected_surface | `POST /containers/{name:.*}/copy` | 110 | * `POST /containers/{name:.*}/copy` is now removed and errors out starting from this API version. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | `POST /containers/{name:.*}/copy` is now removed and errors out starting from this API version. | 110 | * `POST /containers/{name:.*}/copy` is now removed and errors out starting from this API version. |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 110 |  |

## Ticket 77

| field | value | line | quote |
| --- | --- | --- | --- |
| change | API errors are now returned as JSON instead of plain text. | 111 | * API errors are now returned as JSON instead of plain text. |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 111 |  |

## Ticket 78

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` and `POST /containers/(id)/start` allow you to configure kernel parameters (sysctls) for use in the container. | 112 | * `POST /containers/create` and `POST /containers/(id)/start` allow you to configure kernel parameters (sysctls) for use in the container. |
| affected_surface | `POST /containers/create` | 112 | * `POST /containers/create` and `POST /containers/(id)/start` allow you to configure kernel parameters (sysctls) for use in the container. |
| affected_surface | `POST /containers/(id)/start` | 112 | * `POST /containers/create` and `POST /containers/(id)/start` allow you to configure kernel parameters (sysctls) for use in the container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 112 |  |

## Ticket 79

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/<container ID>/exec` and `POST /exec/<exec ID>/start` | 113 | * `POST /containers/<container ID>/exec` and `POST /exec/<exec ID>/start` |
| affected_surface | `POST /containers/<container ID>/exec` | 113 | * `POST /containers/<container ID>/exec` and `POST /exec/<exec ID>/start` |
| affected_surface | `POST /exec/<exec ID>/start` | 113 | * `POST /containers/<container ID>/exec` and `POST /exec/<exec ID>/start` |
| affected_surface | "Container" | 114 | no longer expects a "Container" field to be present. This property was not used |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 113-115 |  |

## Ticket 80

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create/` now validates the hostname (should be a valid RFC 1123 hostname). | 116 | * `POST /containers/create/` now validates the hostname (should be a valid RFC 1123 hostname). |
| affected_surface | `POST /containers/create/` | 116 | * `POST /containers/create/` now validates the hostname (should be a valid RFC 1123 hostname). |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 116 |  |

## Ticket 81

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create/` `HostConfig.PidMode` field now accepts `container:<name\|id>`, | 117 | * `POST /containers/create/` `HostConfig.PidMode` field now accepts `container:<name\|id>`, |
| affected_surface | `POST /containers/create/` | 117 | * `POST /containers/create/` `HostConfig.PidMode` field now accepts `container:<name\|id>`, |
| affected_surface | `HostConfig.PidMode` | 117 | * `POST /containers/create/` `HostConfig.PidMode` field now accepts `container:<name\|id>`, |
| affected_surface | `container:<name\|id>` | 117 | * `POST /containers/create/` `HostConfig.PidMode` field now accepts `container:<name\|id>`, |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 117-118 |  |

## Ticket 82

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/json` returns the state of the container, one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`. | 124 | * `GET /containers/json` returns the state of the container, one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`. |
| affected_surface | `GET /containers/json` | 124 | * `GET /containers/json` returns the state of the container, one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`. |
| affected_surface | `created` | 124 | * `GET /containers/json` returns the state of the container, one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`. |
| affected_surface | `restarting` | 124 | * `GET /containers/json` returns the state of the container, one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`. |
| affected_surface | `running` | 124 | * `GET /containers/json` returns the state of the container, one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`. |
| affected_surface | `paused` | 124 | * `GET /containers/json` returns the state of the container, one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`. |
| affected_surface | `exited` | 124 | * `GET /containers/json` returns the state of the container, one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`. |
| affected_surface | `dead` | 124 | * `GET /containers/json` returns the state of the container, one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 124 |  |

## Ticket 83

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/json` returns the mount points for the container. | 125 | * `GET /containers/json` returns the mount points for the container. |
| affected_surface | `GET /containers/json` | 125 | * `GET /containers/json` returns the mount points for the container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 125 |  |

## Ticket 84

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /networks/(name)` now returns an `Internal` field showing whether the network is internal or not. | 126 | * `GET /networks/(name)` now returns an `Internal` field showing whether the network is internal or not. |
| affected_surface | `GET /networks/(name)` | 126 | * `GET /networks/(name)` now returns an `Internal` field showing whether the network is internal or not. |
| affected_surface | `Internal` | 126 | * `GET /networks/(name)` now returns an `Internal` field showing whether the network is internal or not. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 126 |  |

## Ticket 85

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /networks/(name)` now returns an `EnableIPv6` field showing whether the network has ipv6 enabled or not. | 127 | * `GET /networks/(name)` now returns an `EnableIPv6` field showing whether the network has ipv6 enabled or not. |
| affected_surface | `GET /networks/(name)` | 127 | * `GET /networks/(name)` now returns an `EnableIPv6` field showing whether the network has ipv6 enabled or not. |
| affected_surface | `EnableIPv6` | 127 | * `GET /networks/(name)` now returns an `EnableIPv6` field showing whether the network has ipv6 enabled or not. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 127 |  |

## Ticket 86

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/(name)/update` now supports updating container's restart policy. | 128 | * `POST /containers/(name)/update` now supports updating container's restart policy. |
| affected_surface | `POST /containers/(name)/update` | 128 | * `POST /containers/(name)/update` now supports updating container's restart policy. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 128 |  |

## Ticket 87

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /networks/create` now supports enabling ipv6 on the network by setting the `EnableIPv6` field (doing this with a label will no longer work). | 129 | * `POST /networks/create` now supports enabling ipv6 on the network by setting the `EnableIPv6` field (doing this with a label will no longer work). |
| affected_surface | `POST /networks/create` | 129 | * `POST /networks/create` now supports enabling ipv6 on the network by setting the `EnableIPv6` field (doing this with a label will no longer work). |
| affected_surface | `EnableIPv6` | 129 | * `POST /networks/create` now supports enabling ipv6 on the network by setting the `EnableIPv6` field (doing this with a label will no longer work). |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 129 |  |

## Ticket 88

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` now returns `CgroupDriver` field showing what cgroup driver the daemon is using; `cgroupfs` or `systemd`. | 130 | * `GET /info` now returns `CgroupDriver` field showing what cgroup driver the daemon is using; `cgroupfs` or `systemd`. |
| affected_surface | `GET /info` | 130 | * `GET /info` now returns `CgroupDriver` field showing what cgroup driver the daemon is using; `cgroupfs` or `systemd`. |
| affected_surface | `CgroupDriver` | 130 | * `GET /info` now returns `CgroupDriver` field showing what cgroup driver the daemon is using; `cgroupfs` or `systemd`. |
| affected_surface | `cgroupfs` | 130 | * `GET /info` now returns `CgroupDriver` field showing what cgroup driver the daemon is using; `cgroupfs` or `systemd`. |
| affected_surface | `systemd` | 130 | * `GET /info` now returns `CgroupDriver` field showing what cgroup driver the daemon is using; `cgroupfs` or `systemd`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 130 |  |

## Ticket 89

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` now returns `KernelMemory` field, showing if "kernel memory limit" is supported. | 131 | * `GET /info` now returns `KernelMemory` field, showing if "kernel memory limit" is supported. |
| affected_surface | `GET /info` | 131 | * `GET /info` now returns `KernelMemory` field, showing if "kernel memory limit" is supported. |
| affected_surface | `KernelMemory` | 131 | * `GET /info` now returns `KernelMemory` field, showing if "kernel memory limit" is supported. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 131 |  |

## Ticket 90

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now takes `PidsLimit` field, if the kernel is >= 4.3 and the pids cgroup is supported. | 132 | * `POST /containers/create` now takes `PidsLimit` field, if the kernel is >= 4.3 and the pids cgroup is supported. |
| affected_surface | `POST /containers/create` | 132 | * `POST /containers/create` now takes `PidsLimit` field, if the kernel is >= 4.3 and the pids cgroup is supported. |
| affected_surface | `PidsLimit` | 132 | * `POST /containers/create` now takes `PidsLimit` field, if the kernel is >= 4.3 and the pids cgroup is supported. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 132 |  |

## Ticket 91

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/(id or name)/stats` now returns `pids_stats`, if the kernel is >= 4.3 and the pids cgroup is supported. | 133 | * `GET /containers/(id or name)/stats` now returns `pids_stats`, if the kernel is >= 4.3 and the pids cgroup is supported. |
| affected_surface | `GET /containers/(id or name)/stats` | 133 | * `GET /containers/(id or name)/stats` now returns `pids_stats`, if the kernel is >= 4.3 and the pids cgroup is supported. |
| affected_surface | `pids_stats` | 133 | * `GET /containers/(id or name)/stats` now returns `pids_stats`, if the kernel is >= 4.3 and the pids cgroup is supported. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 133 |  |

## Ticket 92

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now allows you to override usernamespaces remapping and use privileged options for the container. | 134 | * `POST /containers/create` now allows you to override usernamespaces remapping and use privileged options for the container. |
| affected_surface | `POST /containers/create` | 134 | * `POST /containers/create` now allows you to override usernamespaces remapping and use privileged options for the container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 134 |  |

## Ticket 93

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now allows specifying `nocopy` for named volumes, which disables automatic copying from the container path to the volume. | 135 | * `POST /containers/create` now allows specifying `nocopy` for named volumes, which disables automatic copying from the container path to the volume. |
| affected_surface | `POST /containers/create` | 135 | * `POST /containers/create` now allows specifying `nocopy` for named volumes, which disables automatic copying from the container path to the volume. |
| affected_surface | `nocopy` | 135 | * `POST /containers/create` now allows specifying `nocopy` for named volumes, which disables automatic copying from the container path to the volume. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 135 |  |

## Ticket 94

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /auth` now returns an `IdentityToken` when supported by a registry. | 136 | * `POST /auth` now returns an `IdentityToken` when supported by a registry. |
| affected_surface | `POST /auth` | 136 | * `POST /auth` now returns an `IdentityToken` when supported by a registry. |
| affected_surface | `IdentityToken` | 136 | * `POST /auth` now returns an `IdentityToken` when supported by a registry. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 136 |  |

## Ticket 95

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` with both `Hostname` and `Domainname` fields specified will result in the container's hostname being set to `Hostname`, rather than `Hostname.Domainname`. | 137 | * `POST /containers/create` with both `Hostname` and `Domainname` fields specified will result in the container's hostname being set to `Hostname`, rather than `Hostname.Domainname`. |
| affected_surface | `POST /containers/create` | 137 | * `POST /containers/create` with both `Hostname` and `Domainname` fields specified will result in the container's hostname being set to `Hostname`, rather than `Hostname.Domainname`. |
| affected_surface | `Hostname` | 137 | * `POST /containers/create` with both `Hostname` and `Domainname` fields specified will result in the container's hostname being set to `Hostname`, rather than `Hostname.Domainname`. |
| affected_surface | `Domainname` | 137 | * `POST /containers/create` with both `Hostname` and `Domainname` fields specified will result in the container's hostname being set to `Hostname`, rather than `Hostname.Domainname`. |
| affected_surface | `Hostname.Domainname` | 137 | * `POST /containers/create` with both `Hostname` and `Domainname` fields specified will result in the container's hostname being set to `Hostname`, rather than `Hostname.Domainname`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 137 |  |

## Ticket 96

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /volumes` now supports more filters, new added filters are `name` and `driver`. | 138 | * `GET /volumes` now supports more filters, new added filters are `name` and `driver`. |
| affected_surface | `GET /volumes` | 138 | * `GET /volumes` now supports more filters, new added filters are `name` and `driver`. |
| affected_surface | `name` | 138 | * `GET /volumes` now supports more filters, new added filters are `name` and `driver`. |
| affected_surface | `driver` | 138 | * `GET /volumes` now supports more filters, new added filters are `name` and `driver`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 138 |  |

## Ticket 97

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/(id or name)/logs` now accepts a `details` query parameter to stream the extra attributes that were provided to the containers `LogOpts`, such as environment variables and labels, with the logs. | 139 | * `GET /containers/(id or name)/logs` now accepts a `details` query parameter to stream the extra attributes that were provided to the containers `LogOpts`, such as environment variables and labels, with the logs. |
| affected_surface | `GET /containers/(id or name)/logs` | 139 | * `GET /containers/(id or name)/logs` now accepts a `details` query parameter to stream the extra attributes that were provided to the containers `LogOpts`, such as environment variables and labels, with the logs. |
| affected_surface | `details` | 139 | * `GET /containers/(id or name)/logs` now accepts a `details` query parameter to stream the extra attributes that were provided to the containers `LogOpts`, such as environment variables and labels, with the logs. |
| affected_surface | query | 139 | * `GET /containers/(id or name)/logs` now accepts a `details` query parameter to stream the extra attributes that were provided to the containers `LogOpts`, such as environment variables and labels, with the logs. |
| affected_surface | `LogOpts` | 139 | * `GET /containers/(id or name)/logs` now accepts a `details` query parameter to stream the extra attributes that were provided to the containers `LogOpts`, such as environment variables and labels, with the logs. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 139 |  |

## Ticket 98

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /images/load` now returns progress information as a JSON stream, and has a `quiet` query parameter to suppress progress details. | 140 | * `POST /images/load` now returns progress information as a JSON stream, and has a `quiet` query parameter to suppress progress details. |
| affected_surface | `POST /images/load` | 140 | * `POST /images/load` now returns progress information as a JSON stream, and has a `quiet` query parameter to suppress progress details. |
| affected_surface | `quiet` | 140 | * `POST /images/load` now returns progress information as a JSON stream, and has a `quiet` query parameter to suppress progress details. |
| affected_surface | query | 140 | * `POST /images/load` now returns progress information as a JSON stream, and has a `quiet` query parameter to suppress progress details. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 140 |  |

## Ticket 99

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /container/(name)/update` updates the resources of a container. | 146 | * `POST /container/(name)/update` updates the resources of a container. |
| affected_surface | `POST /container/(name)/update` | 146 | * `POST /container/(name)/update` updates the resources of a container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 146 |  |

## Ticket 100

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/json` supports filter `isolation` on Windows. | 147 | * `GET /containers/json` supports filter `isolation` on Windows. |
| affected_surface | `GET /containers/json` | 147 | * `GET /containers/json` supports filter `isolation` on Windows. |
| affected_surface | `isolation` | 147 | * `GET /containers/json` supports filter `isolation` on Windows. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 147 |  |

## Ticket 101

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/json` now returns the list of networks of containers. | 148 | * `GET /containers/json` now returns the list of networks of containers. |
| affected_surface | `GET /containers/json` | 148 | * `GET /containers/json` now returns the list of networks of containers. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 148 |  |

## Ticket 102

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` Now returns `Architecture` and `OSType` fields, providing information | 149 | * `GET /info` Now returns `Architecture` and `OSType` fields, providing information |
| affected_surface | `GET /info` | 149 | * `GET /info` Now returns `Architecture` and `OSType` fields, providing information |
| affected_surface | `Architecture` | 149 | * `GET /info` Now returns `Architecture` and `OSType` fields, providing information |
| affected_surface | `OSType` | 149 | * `GET /info` Now returns `Architecture` and `OSType` fields, providing information |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 149-150 |  |

## Ticket 103

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /networks/(name)` now returns a `Name` field for each container attached to the network. | 151 | * `GET /networks/(name)` now returns a `Name` field for each container attached to the network. |
| affected_surface | `GET /networks/(name)` | 151 | * `GET /networks/(name)` now returns a `Name` field for each container attached to the network. |
| affected_surface | `Name` | 151 | * `GET /networks/(name)` now returns a `Name` field for each container attached to the network. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 151 |  |

## Ticket 104

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /version` now returns the `BuildTime` field in RFC3339Nano format to make it | 152 | * `GET /version` now returns the `BuildTime` field in RFC3339Nano format to make it |
| affected_surface | `GET /version` | 152 | * `GET /version` now returns the `BuildTime` field in RFC3339Nano format to make it |
| affected_surface | `BuildTime` | 152 | * `GET /version` now returns the `BuildTime` field in RFC3339Nano format to make it |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 152-153 |  |

## Ticket 105

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `AuthConfig` now supports a `registrytoken` for token based authentication | 154 | * `AuthConfig` now supports a `registrytoken` for token based authentication |
| affected_surface | `AuthConfig` | 154 | * `AuthConfig` now supports a `registrytoken` for token based authentication |
| affected_surface | `registrytoken` | 154 | * `AuthConfig` now supports a `registrytoken` for token based authentication |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 154 |  |

## Ticket 106

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now has a 4M minimum value limit for `HostConfig.KernelMemory` | 155 | * `POST /containers/create` now has a 4M minimum value limit for `HostConfig.KernelMemory` |
| affected_surface | `POST /containers/create` | 155 | * `POST /containers/create` now has a 4M minimum value limit for `HostConfig.KernelMemory` |
| affected_surface | `HostConfig.KernelMemory` | 155 | * `POST /containers/create` now has a 4M minimum value limit for `HostConfig.KernelMemory` |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 155 |  |

## Ticket 107

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Pushes initiated with `POST /images/(name)/push` and pulls initiated with `POST /images/create` | 156 | * Pushes initiated with `POST /images/(name)/push` and pulls initiated with `POST /images/create` |
| affected_surface | `POST /images/(name)/push` | 156 | * Pushes initiated with `POST /images/(name)/push` and pulls initiated with `POST /images/create` |
| affected_surface | `POST /images/create` | 156 | * Pushes initiated with `POST /images/(name)/push` and pulls initiated with `POST /images/create` |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 156-158 |  |

## Ticket 108

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now allows you to set a read/write rate limit for a | 159 | * `POST /containers/create` now allows you to set a read/write rate limit for a |
| affected_surface | `POST /containers/create` | 159 | * `POST /containers/create` now allows you to set a read/write rate limit for a |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 159-160 |  |

## Ticket 109

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /networks` now supports filtering by `name`, `id` and `type`. | 161 | * `GET /networks` now supports filtering by `name`, `id` and `type`. |
| affected_surface | `GET /networks` | 161 | * `GET /networks` now supports filtering by `name`, `id` and `type`. |
| affected_surface | `name` | 161 | * `GET /networks` now supports filtering by `name`, `id` and `type`. |
| affected_surface | `id` | 161 | * `GET /networks` now supports filtering by `name`, `id` and `type`. |
| affected_surface | `type` | 161 | * `GET /networks` now supports filtering by `name`, `id` and `type`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 161 |  |

## Ticket 110

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now allows you to set the static IPv4 and/or IPv6 address for the container. | 162 | * `POST /containers/create` now allows you to set the static IPv4 and/or IPv6 address for the container. |
| affected_surface | `POST /containers/create` | 162 | * `POST /containers/create` now allows you to set the static IPv4 and/or IPv6 address for the container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 162 |  |

## Ticket 111

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /networks/(id)/connect` now allows you to set the static IPv4 and/or IPv6 address for the container. | 163 | * `POST /networks/(id)/connect` now allows you to set the static IPv4 and/or IPv6 address for the container. |
| affected_surface | `POST /networks/(id)/connect` | 163 | * `POST /networks/(id)/connect` now allows you to set the static IPv4 and/or IPv6 address for the container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 163 |  |

## Ticket 112

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` now includes the number of containers running, stopped, and paused. | 164 | * `GET /info` now includes the number of containers running, stopped, and paused. |
| affected_surface | `GET /info` | 164 | * `GET /info` now includes the number of containers running, stopped, and paused. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 164 |  |

## Ticket 113

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /networks/create` now supports restricting external access to the network by setting the `Internal` field. | 165 | * `POST /networks/create` now supports restricting external access to the network by setting the `Internal` field. |
| affected_surface | `POST /networks/create` | 165 | * `POST /networks/create` now supports restricting external access to the network by setting the `Internal` field. |
| affected_surface | `Internal` | 165 | * `POST /networks/create` now supports restricting external access to the network by setting the `Internal` field. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 165 |  |

## Ticket 114

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /networks/(id)/disconnect` now includes a `Force` option to forcefully disconnect a container from network | 166 | * `POST /networks/(id)/disconnect` now includes a `Force` option to forcefully disconnect a container from network |
| affected_surface | `POST /networks/(id)/disconnect` | 166 | * `POST /networks/(id)/disconnect` now includes a `Force` option to forcefully disconnect a container from network |
| affected_surface | `Force` | 166 | * `POST /networks/(id)/disconnect` now includes a `Force` option to forcefully disconnect a container from network |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 166 |  |

## Ticket 115

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/(id)/json` now returns the `NetworkID` of containers. | 167 | * `GET /containers/(id)/json` now returns the `NetworkID` of containers. |
| affected_surface | `GET /containers/(id)/json` | 167 | * `GET /containers/(id)/json` now returns the `NetworkID` of containers. |
| affected_surface | `NetworkID` | 167 | * `GET /containers/(id)/json` now returns the `NetworkID` of containers. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 167 |  |

## Ticket 116

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /networks/create` Now supports an options field in the IPAM config that provides options | 168 | * `POST /networks/create` Now supports an options field in the IPAM config that provides options |
| affected_surface | `POST /networks/create` | 168 | * `POST /networks/create` Now supports an options field in the IPAM config that provides options |
| affected_surface | options | 168 | * `POST /networks/create` Now supports an options field in the IPAM config that provides options |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 168-169 |  |

## Ticket 117

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /networks/{network-id}` Now returns IPAM config options for custom IPAM plugins if any | 170 | * `GET /networks/{network-id}` Now returns IPAM config options for custom IPAM plugins if any |
| affected_surface | `GET /networks/{network-id}` | 170 | * `GET /networks/{network-id}` Now returns IPAM config options for custom IPAM plugins if any |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 170-171 |  |

## Ticket 118

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /networks/<network-id>` now returns subnets info for user-defined networks. | 172 | * `GET /networks/<network-id>` now returns subnets info for user-defined networks. |
| affected_surface | `GET /networks/<network-id>` | 172 | * `GET /networks/<network-id>` now returns subnets info for user-defined networks. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 172 |  |

## Ticket 119

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` can now return a `SystemStatus` field useful for returning additional information about applications | 173 | * `GET /info` can now return a `SystemStatus` field useful for returning additional information about applications |
| affected_surface | `GET /info` | 173 | * `GET /info` can now return a `SystemStatus` field useful for returning additional information about applications |
| affected_surface | `SystemStatus` | 173 | * `GET /info` can now return a `SystemStatus` field useful for returning additional information about applications |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 173-174 |  |

## Ticket 120

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /volumes` lists volumes from all volume drivers. | 180 | * `GET /volumes` lists volumes from all volume drivers. |
| affected_surface | `GET /volumes` | 180 | * `GET /volumes` lists volumes from all volume drivers. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 180 |  |

## Ticket 121

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /volumes/create` to create a volume. | 181 | * `POST /volumes/create` to create a volume. |
| affected_surface | `POST /volumes/create` | 181 | * `POST /volumes/create` to create a volume. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 181 |  |

## Ticket 122

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /volumes/(name)` get low-level information about a volume. | 182 | * `GET /volumes/(name)` get low-level information about a volume. |
| affected_surface | `GET /volumes/(name)` | 182 | * `GET /volumes/(name)` get low-level information about a volume. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 182 |  |

## Ticket 123

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `DELETE /volumes/(name)` remove a volume with the specified name. | 183 | * `DELETE /volumes/(name)` remove a volume with the specified name. |
| affected_surface | `DELETE /volumes/(name)` | 183 | * `DELETE /volumes/(name)` remove a volume with the specified name. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 183 |  |

## Ticket 124

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `VolumeDriver` was moved from `config` to `HostConfig` to make the configuration portable. | 184 | * `VolumeDriver` was moved from `config` to `HostConfig` to make the configuration portable. |
| affected_surface | `VolumeDriver` | 184 | * `VolumeDriver` was moved from `config` to `HostConfig` to make the configuration portable. |
| affected_surface | `config` | 184 | * `VolumeDriver` was moved from `config` to `HostConfig` to make the configuration portable. |
| affected_surface | `HostConfig` | 184 | * `VolumeDriver` was moved from `config` to `HostConfig` to make the configuration portable. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 184 |  |

## Ticket 125

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /images/(name)/json` now returns information about an image's `RepoTags` and `RepoDigests`. | 185 | * `GET /images/(name)/json` now returns information about an image's `RepoTags` and `RepoDigests`. |
| affected_surface | `GET /images/(name)/json` | 185 | * `GET /images/(name)/json` now returns information about an image's `RepoTags` and `RepoDigests`. |
| affected_surface | `RepoTags` | 185 | * `GET /images/(name)/json` now returns information about an image's `RepoTags` and `RepoDigests`. |
| affected_surface | `RepoDigests` | 185 | * `GET /images/(name)/json` now returns information about an image's `RepoTags` and `RepoDigests`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 185 |  |

## Ticket 126

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The `config` option now accepts the field `StopSignal`, which specifies the signal to use to kill a container. | 186 | * The `config` option now accepts the field `StopSignal`, which specifies the signal to use to kill a container. |
| affected_surface | `config` | 186 | * The `config` option now accepts the field `StopSignal`, which specifies the signal to use to kill a container. |
| affected_surface | the | 186 | * The `config` option now accepts the field `StopSignal`, which specifies the signal to use to kill a container. |
| affected_surface | `StopSignal` | 186 | * The `config` option now accepts the field `StopSignal`, which specifies the signal to use to kill a container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 186 |  |

## Ticket 127

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/(id)/stats` will return networking information respectively for each interface. | 187 | * `GET /containers/(id)/stats` will return networking information respectively for each interface. |
| affected_surface | `GET /containers/(id)/stats` | 187 | * `GET /containers/(id)/stats` will return networking information respectively for each interface. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 187 |  |

## Ticket 128

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The `HostConfig` option now includes the `DnsOptions` field to configure the container's DNS options. | 188 | * The `HostConfig` option now includes the `DnsOptions` field to configure the container's DNS options. |
| affected_surface | `HostConfig` | 188 | * The `HostConfig` option now includes the `DnsOptions` field to configure the container's DNS options. |
| affected_surface | `DnsOptions` | 188 | * The `HostConfig` option now includes the `DnsOptions` field to configure the container's DNS options. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 188 |  |

## Ticket 129

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /build` now optionally takes a serialized map of build-time variables. | 189 | * `POST /build` now optionally takes a serialized map of build-time variables. |
| affected_surface | `POST /build` | 189 | * `POST /build` now optionally takes a serialized map of build-time variables. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 189 |  |

## Ticket 130

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /events` now includes a `timenano` field, in addition to the existing `time` field. | 190 | * `GET /events` now includes a `timenano` field, in addition to the existing `time` field. |
| affected_surface | `GET /events` | 190 | * `GET /events` now includes a `timenano` field, in addition to the existing `time` field. |
| affected_surface | `timenano` | 190 | * `GET /events` now includes a `timenano` field, in addition to the existing `time` field. |
| affected_surface | `time` | 190 | * `GET /events` now includes a `timenano` field, in addition to the existing `time` field. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 190 |  |

## Ticket 131

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /events` now supports filtering by image and container labels. | 191 | * `GET /events` now supports filtering by image and container labels. |
| affected_surface | `GET /events` | 191 | * `GET /events` now supports filtering by image and container labels. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 191 |  |

## Ticket 132

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` now lists engine version information and return the information of `CPUShares` and `Cpuset`. | 192 | * `GET /info` now lists engine version information and return the information of `CPUShares` and `Cpuset`. |
| affected_surface | `GET /info` | 192 | * `GET /info` now lists engine version information and return the information of `CPUShares` and `Cpuset`. |
| affected_surface | `CPUShares` | 192 | * `GET /info` now lists engine version information and return the information of `CPUShares` and `Cpuset`. |
| affected_surface | `Cpuset` | 192 | * `GET /info` now lists engine version information and return the information of `CPUShares` and `Cpuset`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 192 |  |

## Ticket 133

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/json` will return `ImageID` of the image used by container. | 193 | * `GET /containers/json` will return `ImageID` of the image used by container. |
| affected_surface | `GET /containers/json` | 193 | * `GET /containers/json` will return `ImageID` of the image used by container. |
| affected_surface | `ImageID` | 193 | * `GET /containers/json` will return `ImageID` of the image used by container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 193 |  |

## Ticket 134

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /exec/(name)/start` will now return an HTTP 409 when the container is either stopped or paused. | 194 | * `POST /exec/(name)/start` will now return an HTTP 409 when the container is either stopped or paused. |
| affected_surface | `POST /exec/(name)/start` | 194 | * `POST /exec/(name)/start` will now return an HTTP 409 when the container is either stopped or paused. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 194 |  |

## Ticket 135

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` now takes `KernelMemory` in HostConfig to specify kernel memory limit. | 195 | * `POST /containers/create` now takes `KernelMemory` in HostConfig to specify kernel memory limit. |
| affected_surface | `POST /containers/create` | 195 | * `POST /containers/create` now takes `KernelMemory` in HostConfig to specify kernel memory limit. |
| affected_surface | `KernelMemory` | 195 | * `POST /containers/create` now takes `KernelMemory` in HostConfig to specify kernel memory limit. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 195 |  |

## Ticket 136

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/(name)/json` now accepts a `size` parameter. Setting this parameter to '1' returns container size information in the `SizeRw` and `SizeRootFs` fields. | 196 | * `GET /containers/(name)/json` now accepts a `size` parameter. Setting this parameter to '1' returns container size information in the `SizeRw` and `SizeRootFs` fields. |
| affected_surface | `GET /containers/(name)/json` | 196 | * `GET /containers/(name)/json` now accepts a `size` parameter. Setting this parameter to '1' returns container size information in the `SizeRw` and `SizeRootFs` fields. |
| affected_surface | `size` | 196 | * `GET /containers/(name)/json` now accepts a `size` parameter. Setting this parameter to '1' returns container size information in the `SizeRw` and `SizeRootFs` fields. |
| affected_surface | this | 196 | * `GET /containers/(name)/json` now accepts a `size` parameter. Setting this parameter to '1' returns container size information in the `SizeRw` and `SizeRootFs` fields. |
| affected_surface | `SizeRw` | 196 | * `GET /containers/(name)/json` now accepts a `size` parameter. Setting this parameter to '1' returns container size information in the `SizeRw` and `SizeRootFs` fields. |
| affected_surface | `SizeRootFs` | 196 | * `GET /containers/(name)/json` now accepts a `size` parameter. Setting this parameter to '1' returns container size information in the `SizeRw` and `SizeRootFs` fields. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 196 |  |

## Ticket 137

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/(name)/json` now returns a `NetworkSettings.Networks` field, | 197 | * `GET /containers/(name)/json` now returns a `NetworkSettings.Networks` field, |
| affected_surface | `GET /containers/(name)/json` | 197 | * `GET /containers/(name)/json` now returns a `NetworkSettings.Networks` field, |
| affected_surface | `NetworkSettings.Networks` | 197 | * `GET /containers/(name)/json` now returns a `NetworkSettings.Networks` field, |
| affected_surface | This | 198 | detailing network settings per network. This field deprecates the |
| affected_surface | `NetworkSettings.Gateway` | 199 | `NetworkSettings.Gateway`, `NetworkSettings.IPAddress`, |
| affected_surface | `NetworkSettings.IPAddress` | 199 | `NetworkSettings.Gateway`, `NetworkSettings.IPAddress`, |
| affected_surface | `NetworkSettings.IPPrefixLen` | 200 | `NetworkSettings.IPPrefixLen`, and `NetworkSettings.MacAddress` fields, which |
| affected_surface | `NetworkSettings.MacAddress` | 200 | `NetworkSettings.IPPrefixLen`, and `NetworkSettings.MacAddress` fields, which |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | are still returned for backward-compatibility, but will be removed in a future version. | 201 | are still returned for backward-compatibility, but will be removed in a future version. |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 197-201 |  |

## Ticket 138

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /exec/(id)/json` now returns a `NetworkSettings.Networks` field, | 202 | * `GET /exec/(id)/json` now returns a `NetworkSettings.Networks` field, |
| affected_surface | `GET /exec/(id)/json` | 202 | * `GET /exec/(id)/json` now returns a `NetworkSettings.Networks` field, |
| affected_surface | `NetworkSettings.Networks` | 202 | * `GET /exec/(id)/json` now returns a `NetworkSettings.Networks` field, |
| affected_surface | This | 203 | detailing networksettings per network. This field deprecates the |
| affected_surface | `NetworkSettings.Gateway` | 204 | `NetworkSettings.Gateway`, `NetworkSettings.IPAddress`, |
| affected_surface | `NetworkSettings.IPAddress` | 204 | `NetworkSettings.Gateway`, `NetworkSettings.IPAddress`, |
| affected_surface | `NetworkSettings.IPPrefixLen` | 205 | `NetworkSettings.IPPrefixLen`, and `NetworkSettings.MacAddress` fields, which |
| affected_surface | `NetworkSettings.MacAddress` | 205 | `NetworkSettings.IPPrefixLen`, and `NetworkSettings.MacAddress` fields, which |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | are still returned for backward-compatibility, but will be removed in a future version. | 206 | are still returned for backward-compatibility, but will be removed in a future version. |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 202-206 |  |

## Ticket 139

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The `HostConfig` option now includes the `OomScoreAdj` field for adjusting the | 207 | * The `HostConfig` option now includes the `OomScoreAdj` field for adjusting the |
| affected_surface | `HostConfig` | 207 | * The `HostConfig` option now includes the `OomScoreAdj` field for adjusting the |
| affected_surface | `OomScoreAdj` | 207 | * The `HostConfig` option now includes the `OomScoreAdj` field for adjusting the |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 207-209 |  |

## Ticket 140

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/(id)/archive` get an archive of filesystem content from a container. | 215 | * `GET /containers/(id)/archive` get an archive of filesystem content from a container. |
| affected_surface | `GET /containers/(id)/archive` | 215 | * `GET /containers/(id)/archive` get an archive of filesystem content from a container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 215 |  |

## Ticket 141

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `PUT /containers/(id)/archive` upload an archive of content to be extracted to | 216 | * `PUT /containers/(id)/archive` upload an archive of content to be extracted to |
| affected_surface | `PUT /containers/(id)/archive` | 216 | * `PUT /containers/(id)/archive` upload an archive of content to be extracted to |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 216 |  |

## Ticket 142

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/(id)/copy` is deprecated in favor of the above `archive` | 218 | * `POST /containers/(id)/copy` is deprecated in favor of the above `archive` |
| affected_surface | `POST /containers/(id)/copy` | 218 | * `POST /containers/(id)/copy` is deprecated in favor of the above `archive` |
| affected_surface | `archive` | 218 | * `POST /containers/(id)/copy` is deprecated in favor of the above `archive` |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 218 |  |

## Ticket 143

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The `hostConfig` option now accepts the field `GroupAdd`, which specifies a | 220 | * The `hostConfig` option now accepts the field `GroupAdd`, which specifies a |
| affected_surface | `hostConfig` | 220 | * The `hostConfig` option now accepts the field `GroupAdd`, which specifies a |
| affected_surface | the | 220 | * The `hostConfig` option now accepts the field `GroupAdd`, which specifies a |
| affected_surface | `GroupAdd` | 220 | * The `hostConfig` option now accepts the field `GroupAdd`, which specifies a |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 220 |  |

## Ticket 144

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/(id)/stats` now accepts `stream` bool to get only one set of stats and disconnect. | 230 | * `GET /containers/(id)/stats` now accepts `stream` bool to get only one set of stats and disconnect. |
| affected_surface | `GET /containers/(id)/stats` | 230 | * `GET /containers/(id)/stats` now accepts `stream` bool to get only one set of stats and disconnect. |
| affected_surface | `stream` | 230 | * `GET /containers/(id)/stats` now accepts `stream` bool to get only one set of stats and disconnect. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 230 |  |

## Ticket 145

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /containers/(id)/logs` now accepts a `since` timestamp parameter. | 231 | * `GET /containers/(id)/logs` now accepts a `since` timestamp parameter. |
| affected_surface | `GET /containers/(id)/logs` | 231 | * `GET /containers/(id)/logs` now accepts a `since` timestamp parameter. |
| affected_surface | `since` | 231 | * `GET /containers/(id)/logs` now accepts a `since` timestamp parameter. |
| affected_surface | timestamp | 231 | * `GET /containers/(id)/logs` now accepts a `since` timestamp parameter. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 231 |  |

## Ticket 146

| field | value | line | quote |
| --- | --- | --- | --- |
| change | The `hostConfig` option now accepts the fields `CpuPeriod` and `CpuQuota` | 236 | * The `hostConfig` option now accepts the fields `CpuPeriod` and `CpuQuota` |
| affected_surface | `hostConfig` | 236 | * The `hostConfig` option now accepts the fields `CpuPeriod` and `CpuQuota` |
| affected_surface | `CpuPeriod` | 236 | * The `hostConfig` option now accepts the fields `CpuPeriod` and `CpuQuota` |
| affected_surface | `CpuQuota` | 236 | * The `hostConfig` option now accepts the fields `CpuPeriod` and `CpuQuota` |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 236 |  |

## Ticket 147

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /build` accepts `cpuperiod` and `cpuquota` options | 237 | * `POST /build` accepts `cpuperiod` and `cpuquota` options |
| affected_surface | `POST /build` | 237 | * `POST /build` accepts `cpuperiod` and `cpuquota` options |
| affected_surface | `cpuperiod` | 237 | * `POST /build` accepts `cpuperiod` and `cpuquota` options |
| affected_surface | `cpuquota` | 237 | * `POST /build` accepts `cpuperiod` and `cpuquota` options |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 237 |  |

## Ticket 148

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /version` now returns `Os`, `Arch` and `KernelVersion`. | 243 | * `GET /version` now returns `Os`, `Arch` and `KernelVersion`. |
| affected_surface | `GET /version` | 243 | * `GET /version` now returns `Os`, `Arch` and `KernelVersion`. |
| affected_surface | `Os` | 243 | * `GET /version` now returns `Os`, `Arch` and `KernelVersion`. |
| affected_surface | `Arch` | 243 | * `GET /version` now returns `Os`, `Arch` and `KernelVersion`. |
| affected_surface | `KernelVersion` | 243 | * `GET /version` now returns `Os`, `Arch` and `KernelVersion`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 243 |  |

## Ticket 149

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/create` and `POST /containers/(id)/start`allow you to  set ulimit settings for use in the container. | 244 | * `POST /containers/create` and `POST /containers/(id)/start`allow you to  set ulimit settings for use in the container. |
| affected_surface | `POST /containers/create` | 244 | * `POST /containers/create` and `POST /containers/(id)/start`allow you to  set ulimit settings for use in the container. |
| affected_surface | `POST /containers/(id)/start` | 244 | * `POST /containers/create` and `POST /containers/(id)/start`allow you to  set ulimit settings for use in the container. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 244 |  |

## Ticket 150

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /info` now returns `SystemTime`, `HttpProxy`,`HttpsProxy` and `NoProxy`. | 245 | * `GET /info` now returns `SystemTime`, `HttpProxy`,`HttpsProxy` and `NoProxy`. |
| affected_surface | `GET /info` | 245 | * `GET /info` now returns `SystemTime`, `HttpProxy`,`HttpsProxy` and `NoProxy`. |
| affected_surface | `SystemTime` | 245 | * `GET /info` now returns `SystemTime`, `HttpProxy`,`HttpsProxy` and `NoProxy`. |
| affected_surface | `HttpProxy` | 245 | * `GET /info` now returns `SystemTime`, `HttpProxy`,`HttpsProxy` and `NoProxy`. |
| affected_surface | `HttpsProxy` | 245 | * `GET /info` now returns `SystemTime`, `HttpProxy`,`HttpsProxy` and `NoProxy`. |
| affected_surface | `NoProxy` | 245 | * `GET /info` now returns `SystemTime`, `HttpProxy`,`HttpsProxy` and `NoProxy`. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 245 |  |

## Ticket 151

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `GET /images/json` added a `RepoDigests` field to include image digest information. | 246 | * `GET /images/json` added a `RepoDigests` field to include image digest information. |
| affected_surface | `GET /images/json` | 246 | * `GET /images/json` added a `RepoDigests` field to include image digest information. |
| affected_surface | `RepoDigests` | 246 | * `GET /images/json` added a `RepoDigests` field to include image digest information. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 246 |  |

## Ticket 152

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /build` can now set resource constraints for all containers created for the build. | 247 | * `POST /build` can now set resource constraints for all containers created for the build. |
| affected_surface | `POST /build` | 247 | * `POST /build` can now set resource constraints for all containers created for the build. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 247 |  |

## Ticket 153

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `CgroupParent` can be passed in the host config to setup container cgroups under a specific cgroup. | 248 | * `CgroupParent` can be passed in the host config to setup container cgroups under a specific cgroup. |
| affected_surface | `CgroupParent` | 248 | * `CgroupParent` can be passed in the host config to setup container cgroups under a specific cgroup. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 248 |  |

## Ticket 154

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /build` closing the HTTP request cancels the build | 249 | * `POST /build` closing the HTTP request cancels the build |
| affected_surface | `POST /build` | 249 | * `POST /build` closing the HTTP request cancels the build |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 249 |  |

## Ticket 155

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `POST /containers/(id)/exec` includes `Warnings` field to response. | 250 | * `POST /containers/(id)/exec` includes `Warnings` field to response. |
| affected_surface | `POST /containers/(id)/exec` | 250 | * `POST /containers/(id)/exec` includes `Warnings` field to response. |
| affected_surface | `Warnings` | 250 | * `POST /containers/(id)/exec` includes `Warnings` field to response. |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/moby/moby/60ccb2265b0574d6c1c1090876a1d1ab32bed60e/docs/api/version-history.md raw-githubusercontent-com-moby-moby-60ccb2265b0574d6c1c1090876a1d1ab32bed60e-doc-20260921T212216Z.txt | 250 |  |

## Unmapped

- 1: ---
- 2: title: "Engine API version history"
- 3: description: "Documentation of changes that have been made to Engine API."
- 4: keywords: "API, Docker, rcli, REST, documentation"
- 5: ---
- 7: <!-- This file is maintained within the docker/docker Github
- 8:      repository at https://github.com/docker/docker/. Make all
- 9:      pull requests against that repo. If you see this file in
- 10:      another repository, consider it read-only there, as it will
- 11:      periodically be overwritten by the definitive file. Pull
- 12:      requests which include edits to this file in other repositories
- 13:      will be rejected.
- 14: -->
- 16: ## v1.26 API changes
- 18: [Docker Engine API v1.26](https://docs.docker.com/engine/api/v1.26/) documentation
- 22: ## v1.25 API changes
- 24: [Docker Engine API v1.25](https://docs.docker.com/engine/api/v1.25/) documentation
- 46:   containers that are tasks (part of a service in swarm mode).
- 88: ## v1.24 API changes
- 90: [Docker Engine API v1.24](v1.24.md) documentation
- 95:   with ContainerD in Docker 1.11.
- 100:   if no command is specified (instead of an HTTP 500 "server error")
- 115:   and is no longer sent by the docker client.
- 118:   to have the container join the PID namespace of an existing container.
- 120: ## v1.23 API changes
- 122: [Docker Engine API v1.23](v1.23.md) documentation
- 142: ## v1.22 API changes
- 144: [Docker Engine API v1.22](v1.22.md) documentation
- 150:   about the host architecture and operating system type that the daemon runs on.
- 153:   consistent with other date/time values returned by the API.
- 157:   will be cancelled if the HTTP connection making the API request is closed before
- 158:   the push or pull completes.
- 160:   device (in bytes per second or IO per second).
- 169:   for custom IPAM plugins.
- 171:   are available.
- 174:   that are built on top of engine.
- 176: ## v1.21 API changes
- 178: [Docker Engine API v1.21](v1.21.md) documentation
- 208:   badness heuristic. This heuristic selects which processes the OOM killer kills
- 209:   under out-of-memory conditions.
- 211: ## v1.20 API changes
- 213: [Docker Engine API v1.20](v1.20.md) documentation
- 217: an existing directory inside a container's filesystem.
- 219: endpoint which can be used to download files and directories from a container.
- 221: list of additional groups that the container process will run as.
- 223: ## v1.19 API changes
- 225: [Docker Engine API v1.19](v1.19.md) documentation
- 227: * When the daemon detects a version mismatch with the client, usually when
- 228: the client is newer than the daemon, an HTTP 400 is now returned instead
- 229: of a 404.
- 232: * `GET /info` The fields `Debug`, `IPv4Forwarding`, `MemoryLimit`, and
- 233: `SwapLimit` are now returned as boolean instead of as an int. In addition, the
- 234: end point now returns the new boolean fields `CpuCfsPeriod`, `CpuCfsQuota`, and
- 235: `OomKillDisable`.
- 239: ## v1.18 API changes
- 241: [Docker Engine API v1.18](v1.18.md) documentation

```

## Pair 3

Input: raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt
```
source_url: https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md
final_url: https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md
http_status: 200
content_type: text/plain; charset=utf-8
retrieved: 20260921T212216Z
routine: as-served
routine_version: 1
sha256: 4c2654fbd035a350c1f1c67b40cf4cd46836a5edbd9d9bb18c89667b55ea7e41
--- body ---
      1: ### 2020-09-14_1.20.6
      2: - Added `format:` labels to all date and date-time strings
      3: - Fix missing title attributes
      4: - Converted some strings to enums
      5: ### 2020-09-14_1.20.5
      6: - Updated `Select Account` to `Account Select`
      7: ### 2020-09-14_1.20.4
      8: - Update Signal risk tier definitions
      9: ### 2020-09-14_1.20.3
     10: - Bug fixes to signal endpoints
     11: ### 2020-09-14_1.20.1
     12: - Added `/sandbox/oauth/select_accounts` endpoint.
     13: ### 2021-07-27_1.20.0
     14: - Added `liabilities_updates`, `liabilities`, and `investments` to institution schema
     15: ### 2020-09-14_1.20.0
     16: - Added `/signal/evaluate` endpoint
     17: - Added `/signal/decision/report` endpoint
     18: - Added `/signal/return/report` endpoint
     19: - Added `/income/verification/refresh` endpoint.
     20: ### 2020-09-14_1.19.12
     21: - Added `alpaca`, `astra` and `moov` processors.
     22: - Changed naming for some nullable parameters from `NullableParam` to `ParamNullable`.
     23: - Added `/processor/bank_transfer/create` endpoint.
     24: - Changed the inherited model for `AssetReportTransaction` from `Transaction` to `TransactionBase` which has fewer required fields.
     25: 
     26: ### 2020-09-14_1.19.11
     27: - Added `logo_url` as a required value of `ConnectedApplications`
     28: - Made `logo` a deprecated value of `ConnectedApplications` soon to be removed in future versions
     29: 
     30: ### 2020-09-14_1.19.10
     31: - Added `income` back to the list of possible products as it's in sandbox return values.
     32: - Made `switch_method` nullable as the sandbox deposit/switch response has it nulled.
     33: 
     34: ### 2021-07-1_1.19.9
     35: - Added `CountryCode` to the request fields of `deposit_switch/create` and `deposit_switch/alt/create`
     36: - Added `TransactionAccessTokens` to `DepositSwitchCreateOptions`
     37: 
     38: ### 2020-09-14_1.19.8
     39: - Added `options` field to request body for `deposit_switch/create` and `deposit_switch/alt/create` endpoints
     40: - Added webhook documentation for `deposit_switch/`
     41: - Added a new state to the list of possible values for the `state` field in the response body, and updated descriptions of all states
     42: 
     43: ### 2020-09-14_1.19.7
     44: - Added `ItemApplicationListUserAuth` component
     45: - Added `user_auth` as a private field in `/item/application/list` request
     46: - Changed `/item/application/list` request `access_token` field from `AccessToken` to `NullableAccessToken` to support `user_auth` flow (`/item/application/list` can be queried using `user_auth` instead of an access token for certain clients)
     47: 
     48: ### 2020-09-14_1.19.6
     49: - Added the following response fields to the `/deposit_switch/get` docs:
     50:     + `switch_method`
     51:     + `employer_name`
     52:     + `employer_id`
     53:     + `institution_name`
     54:     + `institution_id`
     55: 
     56: ### 2020-09-14_1.19.5
     57: - Added `required` to many fields where it was missing
     58: - Removed `nullable: true` annotation incorrectly applied to some fields
     59: - Added ``nullable: true` annotation incorrectly missing from some fields
     60: - Fixed invalid example for `/processor/balance/get`
     61: - Fixed incorrect formatting for certain `allOf` structures
     62: - Added enum values for some strings that were not treated as enums
     63: - Added missing `created_at` field to `Application`
     64: - Added missing `null` enum to some nullable enums
     65: - Added missing beta `include_original_description` and `original_description` fields to `Transaction`
     66: - Various small description fixes
     67: - Updated external docs URLs for Income endpoints
     68: 
     69: ### 2020-09-14_1.19.4
     70: - Fixed description for `close_price` field returned in `/investments/holdings/get` response
     71: 
     72: ### 2020-09-14_1.19.3
     73: - Updated the `/institutions/get/` description to explain filtering behavior
     74: 
     75: ### 2020-09-14_1.19.2
     76: - Added `error` field to `/income/verification/summary/get` response body
     77: 
     78: ### 2020-09-14_1.19.1
     79: - Fix links to income (beta) docs
     80: - add income webhook example
     81: 
     82: ### 2020-09-14_1.19.0
     83: - Added `/sandbox/income/fire_webhook` endpoint
     84: 
     85: ### 2020-09-14_1.18.2
     86: - Added Lithic and SVB to the list of supported processors for `/processor/token/create` endpoint
     87: 
     88: ### 2020-09-14_1.18.1
     89: - Fixed file to reflect that `category_id` and `next_payment_due_date` are nullable
     90: - Removed spurious `paystub_id` field
     91: - Added missing `SCHEDULED` value to `IncidentUpdate.status` enum
     92: - Various description fixes
     93: 
     94: ### 2020-09-14_1.18.0
     95: 
     96: - Added `/item/application/scopes/update` endpoint
     97: - Fixed incorrect enum values for `update_type`
     98: - Fixed file to reflect that `current` balance field is nullable.
     99: - Description and textual fixes
    100: - Fix invalid format errors
    101: - Add new investment subtypes
    102: 
    103: ### 2020-09-14_1.17.0
    104: - Small description fix for `/income/verification/create` and `/employers/search`
    105: - Fixed  `ytd_net_income` value in `IncomeVerificationSummaryGetResponse` example
    106: - Fixed references to `paystub` to be plural `paystubs` for `/income/verification/paystubs/get` route and schemas
    107: - Added `PaystubEmployer` schema referenced in the `Paystub` object
    108: 
    109: ### 2020-09-14_1.16.6
    110: - Added `ItemApplicationScopesUpdateRequest` and `ItemApplicationScopesUpdateResponse` schema
    111: 
    112: ### 2020-09-14_1.16.5
    113: - Added `emi_account_id` field to `PaymentInitiationPayment` model for `/payment_initiation/payment/get` and `/payment_initiation/payment/list` response
    114: - Added `emi_recipient_id` field to `PaymentInitiationRecipient` model for `/payment_initiation/recipient/get` and `/payment_initiation/recipient/list` response
    115: 
    116: ### 2020-09-14_1.16.4
    117: - Removes erroneous `request_id` that was incorrectly shown to be returned in items from `/payment_initiation/payment/list` and `/payment_initiation/recipient/list`.
    118: - Fix for `ExternalPaymentSchedule` to make `end_date` optional.
    119: 
    120: ### 2020-09-14_1.16.3
    121: - Updated `/investments/transactions/get` count minimum to be 1 instead of 0
    122: 
    123: ### 2020-09-14_1.16.2
    124: - Fixes for required parameters for `JWKPublicKey` and `Security`.
    125: - Fix for `BankTransferMetadata` to be nullable.
    126: 
    127: ### 2020-09-14_1.16.1
    128: - Fixes for descriptions and linter errors.
    129: 
    130: ### 2020-09-14_1.16.0
    131: - Updated `/payment_initiation/payment/create` with ability to pass in iban or account and sort code. If provided, the end user will be able to send payments only from the specified bank account.
    132: 
    133: ### 2020-09-14_1.15.1
    134: - Add clarifying max character line to client_name description.
    135: 
    136: ### 2020-09-14_1.15.0
    137: 
    138: - Removed erroneous `access_token` that was incorrectly shown to be returned by `/item/get`.
    139: - Added `business` loan type.
    140: - Clarified `date` format for `institution_price_as_of`.
    141: - Various small description fixes.
    142: 
    143: ### 2020-09-14_1.14.0
    144: 
    145: - Updated `institutions/get`, `institutions/get_by_id`, and `institutions/search` to introduce an optional flag to return Payment Initiation metadata
    146: - Updated `institutions/search` to accept additional options to filter institutions by various Payment Initiation configurations.
    147: 
    148: ### 2020-09-14_1.13.3
    149: 
    150: - Updated `/accounts/balance/get` documentation to show `INVALID_FIELD` and `LAST_UPDATED_DATETIME_OUT_OF_RANGE` errors that will be returned for `capone-oauth`
    151: 
    152: ### 2020-09-14_1.13.2
    153: 
    154: - Add specific format attribute to `date_of_birth` under `LinkTokenCreateRequestUser`.
    155: 
    156: ### 2020-09-14_1.13.1
    157: 
    158: - Remove `last_statement_balance` since it's never been populated and is being removed in the next version
    159: - Correct investment transaction sells quantity to be negative
    160: - Updated documentation to allow `minimum_payment_amount` to be set on loans with type `student`.
    161: 
    162: ### 2020-09-14_1.13.0
    163: 
    164: - Added `standing_orders` product type.
    165: 
    166: ### 2021-09-14_1.12.0
    167: 
    168: - Added `min_last_updated_datetime` option to `/accounts/balance/get` request.
    169: - Added `last_updated_datetime` field to `Account` model for `/accounts/balance/get` response.
    170: 
    171: ### 2020-09-14_1.11.0
    172: 
    173: - Removed erroneous inclusion of `account_filters` as a parameter to `/institutions/search`
    174: - Text fixes to descriptions
    175: - Fixed incorrect field names in some models currently used only for documentation
    176: 
    177: ### 2020-09-14_1.10.0
    178: 
    179: - Added `BankTransfersEventsUpdateWebhook` schema
    180: 
    181: ### 2020-09-14_1.9.0
    182: 
    183: - Added new `auth` property to `/link/token/create` request to support Flexible Auth (currently in closed beta).
    184: - Text fixes to descriptions.
    185: 
    186: ### 2020-09-14_1.8.0
    187: 
    188: - Added `additionalProperties` to all objects to prevent additive keys from breaking.
    189: - Added new propery to `Transaction` model, `authorized_datetime`, `datetime`.
    190: - Update `access_token` to `required` for `TransactionsGet`.
    191: - Require `origination_account_id` in `BankTransferBalanceGetResponse`
    192: - Add new endpoint `/sandbox/bank_transfer/fire_webhook`
    193: 
    194: ### 2020-09-14_1.5.3
    195: 
    196: - Added new payment processors.
    197: 
    198: ### 2020-09-14_1.5.0
    199: 
    200: Initial version

```

Output: raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.tickets.md
```
snapshot: raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt
sha256: 4c2654fbd035a350c1f1c67b40cf4cd46836a5edbd9d9bb18c89667b55ea7e41
source_url: https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md
body_range: 1-200
line_numbers: snapshot

## Ticket 1

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `format:` labels to all date and date-time strings | 2 | - Added `format:` labels to all date and date-time strings |
| affected_surface | `format:` | 2 | - Added `format:` labels to all date and date-time strings |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 1 | ### 2020-09-14_1.20.6 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 2 |  |

## Ticket 2

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fix missing title attributes | 3 | - Fix missing title attributes |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 1 | ### 2020-09-14_1.20.6 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 3 |  |

## Ticket 3

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Converted some strings to enums | 4 | - Converted some strings to enums |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 1 | ### 2020-09-14_1.20.6 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 4 |  |

## Ticket 4

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Updated `Select Account` to `Account Select` | 6 | - Updated `Select Account` to `Account Select` |
| affected_surface | `Select Account` | 6 | - Updated `Select Account` to `Account Select` |
| affected_surface | `Account Select` | 6 | - Updated `Select Account` to `Account Select` |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 5 | ### 2020-09-14_1.20.5 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 6 |  |

## Ticket 5

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Update Signal risk tier definitions | 8 | - Update Signal risk tier definitions |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 7 | ### 2020-09-14_1.20.4 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 8 |  |

## Ticket 6

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Bug fixes to signal endpoints | 10 | - Bug fixes to signal endpoints |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 9 | ### 2020-09-14_1.20.3 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 10 |  |

## Ticket 7

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `/sandbox/oauth/select_accounts` endpoint. | 12 | - Added `/sandbox/oauth/select_accounts` endpoint. |
| affected_surface | `/sandbox/oauth/select_accounts` | 12 | - Added `/sandbox/oauth/select_accounts` endpoint. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 11 | ### 2020-09-14_1.20.1 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 12 |  |

## Ticket 8

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `liabilities_updates`, `liabilities`, and `investments` to institution schema | 14 | - Added `liabilities_updates`, `liabilities`, and `investments` to institution schema |
| affected_surface | `liabilities_updates` | 14 | - Added `liabilities_updates`, `liabilities`, and `investments` to institution schema |
| affected_surface | `liabilities` | 14 | - Added `liabilities_updates`, `liabilities`, and `investments` to institution schema |
| affected_surface | `investments` | 14 | - Added `liabilities_updates`, `liabilities`, and `investments` to institution schema |
| breaking | not in source |  |  |
| entry_date | 2021-07-27 | 13 | ### 2021-07-27_1.20.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 14 |  |

## Ticket 9

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `/signal/evaluate` endpoint | 16 | - Added `/signal/evaluate` endpoint |
| affected_surface | `/signal/evaluate` | 16 | - Added `/signal/evaluate` endpoint |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 15 | ### 2020-09-14_1.20.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 16 |  |

## Ticket 10

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `/signal/decision/report` endpoint | 17 | - Added `/signal/decision/report` endpoint |
| affected_surface | `/signal/decision/report` | 17 | - Added `/signal/decision/report` endpoint |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 15 | ### 2020-09-14_1.20.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 17 |  |

## Ticket 11

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `/signal/return/report` endpoint | 18 | - Added `/signal/return/report` endpoint |
| affected_surface | `/signal/return/report` | 18 | - Added `/signal/return/report` endpoint |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 15 | ### 2020-09-14_1.20.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 18 |  |

## Ticket 12

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `/income/verification/refresh` endpoint. | 19 | - Added `/income/verification/refresh` endpoint. |
| affected_surface | `/income/verification/refresh` | 19 | - Added `/income/verification/refresh` endpoint. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 15 | ### 2020-09-14_1.20.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 19 |  |

## Ticket 13

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `alpaca`, `astra` and `moov` processors. | 21 | - Added `alpaca`, `astra` and `moov` processors. |
| affected_surface | `alpaca` | 21 | - Added `alpaca`, `astra` and `moov` processors. |
| affected_surface | `astra` | 21 | - Added `alpaca`, `astra` and `moov` processors. |
| affected_surface | `moov` | 21 | - Added `alpaca`, `astra` and `moov` processors. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 20 | ### 2020-09-14_1.19.12 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 21 |  |

## Ticket 14

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Changed naming for some nullable parameters from `NullableParam` to `ParamNullable`. | 22 | - Changed naming for some nullable parameters from `NullableParam` to `ParamNullable`. |
| affected_surface | `NullableParam` | 22 | - Changed naming for some nullable parameters from `NullableParam` to `ParamNullable`. |
| affected_surface | `ParamNullable` | 22 | - Changed naming for some nullable parameters from `NullableParam` to `ParamNullable`. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 20 | ### 2020-09-14_1.19.12 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 22 |  |

## Ticket 15

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `/processor/bank_transfer/create` endpoint. | 23 | - Added `/processor/bank_transfer/create` endpoint. |
| affected_surface | `/processor/bank_transfer/create` | 23 | - Added `/processor/bank_transfer/create` endpoint. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 20 | ### 2020-09-14_1.19.12 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 23 |  |

## Ticket 16

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Changed the inherited model for `AssetReportTransaction` from `Transaction` to `TransactionBase` which has fewer required fields. | 24 | - Changed the inherited model for `AssetReportTransaction` from `Transaction` to `TransactionBase` which has fewer required fields. |
| affected_surface | `AssetReportTransaction` | 24 | - Changed the inherited model for `AssetReportTransaction` from `Transaction` to `TransactionBase` which has fewer required fields. |
| affected_surface | `Transaction` | 24 | - Changed the inherited model for `AssetReportTransaction` from `Transaction` to `TransactionBase` which has fewer required fields. |
| affected_surface | `TransactionBase` | 24 | - Changed the inherited model for `AssetReportTransaction` from `Transaction` to `TransactionBase` which has fewer required fields. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 20 | ### 2020-09-14_1.19.12 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 24 |  |

## Ticket 17

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `logo_url` as a required value of `ConnectedApplications` | 27 | - Added `logo_url` as a required value of `ConnectedApplications` |
| affected_surface | `logo_url` | 27 | - Added `logo_url` as a required value of `ConnectedApplications` |
| affected_surface | `ConnectedApplications` | 27 | - Added `logo_url` as a required value of `ConnectedApplications` |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 26 | ### 2020-09-14_1.19.11 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 27 |  |

## Ticket 18

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Made `logo` a deprecated value of `ConnectedApplications` soon to be removed in future versions | 28 | - Made `logo` a deprecated value of `ConnectedApplications` soon to be removed in future versions |
| affected_surface | `logo` | 28 | - Made `logo` a deprecated value of `ConnectedApplications` soon to be removed in future versions |
| affected_surface | `ConnectedApplications` | 28 | - Made `logo` a deprecated value of `ConnectedApplications` soon to be removed in future versions |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 26 | ### 2020-09-14_1.19.11 |
| effective_date | not in source |  |  |
| sunset_date | Made `logo` a deprecated value of `ConnectedApplications` soon to be removed in future versions | 28 | - Made `logo` a deprecated value of `ConnectedApplications` soon to be removed in future versions |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 28 |  |

## Ticket 19

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `income` back to the list of possible products as it's in sandbox return values. | 31 | - Added `income` back to the list of possible products as it's in sandbox return values. |
| affected_surface | `income` | 31 | - Added `income` back to the list of possible products as it's in sandbox return values. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 30 | ### 2020-09-14_1.19.10 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 31 |  |

## Ticket 20

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Made `switch_method` nullable as the sandbox deposit/switch response has it nulled. | 32 | - Made `switch_method` nullable as the sandbox deposit/switch response has it nulled. |
| affected_surface | `switch_method` | 32 | - Made `switch_method` nullable as the sandbox deposit/switch response has it nulled. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 30 | ### 2020-09-14_1.19.10 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 32 |  |

## Ticket 21

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `CountryCode` to the request fields of `deposit_switch/create` and `deposit_switch/alt/create` | 35 | - Added `CountryCode` to the request fields of `deposit_switch/create` and `deposit_switch/alt/create` |
| affected_surface | `CountryCode` | 35 | - Added `CountryCode` to the request fields of `deposit_switch/create` and `deposit_switch/alt/create` |
| affected_surface | `deposit_switch/create` | 35 | - Added `CountryCode` to the request fields of `deposit_switch/create` and `deposit_switch/alt/create` |
| affected_surface | `deposit_switch/alt/create` | 35 | - Added `CountryCode` to the request fields of `deposit_switch/create` and `deposit_switch/alt/create` |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 35 |  |

## Ticket 22

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `TransactionAccessTokens` to `DepositSwitchCreateOptions` | 36 | - Added `TransactionAccessTokens` to `DepositSwitchCreateOptions` |
| affected_surface | `TransactionAccessTokens` | 36 | - Added `TransactionAccessTokens` to `DepositSwitchCreateOptions` |
| affected_surface | `DepositSwitchCreateOptions` | 36 | - Added `TransactionAccessTokens` to `DepositSwitchCreateOptions` |
| breaking | not in source |  |  |
| entry_date | not in source |  |  |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 36 |  |

## Ticket 23

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `options` field to request body for `deposit_switch/create` and `deposit_switch/alt/create` endpoints | 39 | - Added `options` field to request body for `deposit_switch/create` and `deposit_switch/alt/create` endpoints |
| affected_surface | `options` | 39 | - Added `options` field to request body for `deposit_switch/create` and `deposit_switch/alt/create` endpoints |
| affected_surface | `deposit_switch/create` | 39 | - Added `options` field to request body for `deposit_switch/create` and `deposit_switch/alt/create` endpoints |
| affected_surface | `deposit_switch/alt/create` | 39 | - Added `options` field to request body for `deposit_switch/create` and `deposit_switch/alt/create` endpoints |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 38 | ### 2020-09-14_1.19.8 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 39 |  |

## Ticket 24

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added webhook documentation for `deposit_switch/` | 40 | - Added webhook documentation for `deposit_switch/` |
| affected_surface | `deposit_switch/` | 40 | - Added webhook documentation for `deposit_switch/` |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 38 | ### 2020-09-14_1.19.8 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 40 |  |

## Ticket 25

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added a new state to the list of possible values for the `state` field in the response body, and updated descriptions of all states | 41 | - Added a new state to the list of possible values for the `state` field in the response body, and updated descriptions of all states |
| affected_surface | `state` | 41 | - Added a new state to the list of possible values for the `state` field in the response body, and updated descriptions of all states |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 38 | ### 2020-09-14_1.19.8 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 41 |  |

## Ticket 26

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `ItemApplicationListUserAuth` component | 44 | - Added `ItemApplicationListUserAuth` component |
| affected_surface | `ItemApplicationListUserAuth` | 44 | - Added `ItemApplicationListUserAuth` component |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 43 | ### 2020-09-14_1.19.7 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 44 |  |

## Ticket 27

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `user_auth` as a private field in `/item/application/list` request | 45 | - Added `user_auth` as a private field in `/item/application/list` request |
| affected_surface | `user_auth` | 45 | - Added `user_auth` as a private field in `/item/application/list` request |
| affected_surface | private | 45 | - Added `user_auth` as a private field in `/item/application/list` request |
| affected_surface | `/item/application/list` | 45 | - Added `user_auth` as a private field in `/item/application/list` request |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 43 | ### 2020-09-14_1.19.7 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 45 |  |

## Ticket 28

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Changed `/item/application/list` request `access_token` field from `AccessToken` to `NullableAccessToken` to support `user_auth` flow (`/item/application/list` can be queried using `user_auth` instead of an access token for certain clients) | 46 | - Changed `/item/application/list` request `access_token` field from `AccessToken` to `NullableAccessToken` to support `user_auth` flow (`/item/application/list` can be queried using `user_auth` instead of an access token for certain clients) |
| affected_surface | `/item/application/list` | 46 | - Changed `/item/application/list` request `access_token` field from `AccessToken` to `NullableAccessToken` to support `user_auth` flow (`/item/application/list` can be queried using `user_auth` instead of an access token for certain clients) |
| affected_surface | `access_token` | 46 | - Changed `/item/application/list` request `access_token` field from `AccessToken` to `NullableAccessToken` to support `user_auth` flow (`/item/application/list` can be queried using `user_auth` instead of an access token for certain clients) |
| affected_surface | `AccessToken` | 46 | - Changed `/item/application/list` request `access_token` field from `AccessToken` to `NullableAccessToken` to support `user_auth` flow (`/item/application/list` can be queried using `user_auth` instead of an access token for certain clients) |
| affected_surface | `NullableAccessToken` | 46 | - Changed `/item/application/list` request `access_token` field from `AccessToken` to `NullableAccessToken` to support `user_auth` flow (`/item/application/list` can be queried using `user_auth` instead of an access token for certain clients) |
| affected_surface | `user_auth` | 46 | - Changed `/item/application/list` request `access_token` field from `AccessToken` to `NullableAccessToken` to support `user_auth` flow (`/item/application/list` can be queried using `user_auth` instead of an access token for certain clients) |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 43 | ### 2020-09-14_1.19.7 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 46 |  |

## Ticket 29

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `switch_method` | 50 | + `switch_method` |
| affected_surface | `/deposit_switch/get` | 49 | - Added the following response fields to the `/deposit_switch/get` docs: |
| affected_surface | `switch_method` | 50 | + `switch_method` |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 48 | ### 2020-09-14_1.19.6 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 50 |  |

## Ticket 30

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `employer_name` | 51 | + `employer_name` |
| affected_surface | `/deposit_switch/get` | 49 | - Added the following response fields to the `/deposit_switch/get` docs: |
| affected_surface | `employer_name` | 51 | + `employer_name` |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 48 | ### 2020-09-14_1.19.6 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 51 |  |

## Ticket 31

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `employer_id` | 52 | + `employer_id` |
| affected_surface | `/deposit_switch/get` | 49 | - Added the following response fields to the `/deposit_switch/get` docs: |
| affected_surface | `employer_id` | 52 | + `employer_id` |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 48 | ### 2020-09-14_1.19.6 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 52 |  |

## Ticket 32

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `institution_name` | 53 | + `institution_name` |
| affected_surface | `/deposit_switch/get` | 49 | - Added the following response fields to the `/deposit_switch/get` docs: |
| affected_surface | `institution_name` | 53 | + `institution_name` |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 48 | ### 2020-09-14_1.19.6 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 53 |  |

## Ticket 33

| field | value | line | quote |
| --- | --- | --- | --- |
| change | `institution_id` | 54 | + `institution_id` |
| affected_surface | `/deposit_switch/get` | 49 | - Added the following response fields to the `/deposit_switch/get` docs: |
| affected_surface | `institution_id` | 54 | + `institution_id` |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 48 | ### 2020-09-14_1.19.6 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 54 |  |

## Ticket 34

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `required` to many fields where it was missing | 57 | - Added `required` to many fields where it was missing |
| affected_surface | `required` | 57 | - Added `required` to many fields where it was missing |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 56 | ### 2020-09-14_1.19.5 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 57 |  |

## Ticket 35

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Removed `nullable: true` annotation incorrectly applied to some fields | 58 | - Removed `nullable: true` annotation incorrectly applied to some fields |
| affected_surface | `nullable: true` | 58 | - Removed `nullable: true` annotation incorrectly applied to some fields |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 56 | ### 2020-09-14_1.19.5 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 58 |  |

## Ticket 36

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added ``nullable: true` annotation incorrectly missing from some fields | 59 | - Added ``nullable: true` annotation incorrectly missing from some fields |
| affected_surface | `` | 59 | - Added ``nullable: true` annotation incorrectly missing from some fields |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 56 | ### 2020-09-14_1.19.5 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 59 |  |

## Ticket 37

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fixed invalid example for `/processor/balance/get` | 60 | - Fixed invalid example for `/processor/balance/get` |
| affected_surface | `/processor/balance/get` | 60 | - Fixed invalid example for `/processor/balance/get` |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 56 | ### 2020-09-14_1.19.5 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 60 |  |

## Ticket 38

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fixed incorrect formatting for certain `allOf` structures | 61 | - Fixed incorrect formatting for certain `allOf` structures |
| affected_surface | `allOf` | 61 | - Fixed incorrect formatting for certain `allOf` structures |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 56 | ### 2020-09-14_1.19.5 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 61 |  |

## Ticket 39

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added enum values for some strings that were not treated as enums | 62 | - Added enum values for some strings that were not treated as enums |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 56 | ### 2020-09-14_1.19.5 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 62 |  |

## Ticket 40

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added missing `created_at` field to `Application` | 63 | - Added missing `created_at` field to `Application` |
| affected_surface | `created_at` | 63 | - Added missing `created_at` field to `Application` |
| affected_surface | `Application` | 63 | - Added missing `created_at` field to `Application` |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 56 | ### 2020-09-14_1.19.5 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 63 |  |

## Ticket 41

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added missing `null` enum to some nullable enums | 64 | - Added missing `null` enum to some nullable enums |
| affected_surface | `null` | 64 | - Added missing `null` enum to some nullable enums |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 56 | ### 2020-09-14_1.19.5 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 64 |  |

## Ticket 42

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added missing beta `include_original_description` and `original_description` fields to `Transaction` | 65 | - Added missing beta `include_original_description` and `original_description` fields to `Transaction` |
| affected_surface | `include_original_description` | 65 | - Added missing beta `include_original_description` and `original_description` fields to `Transaction` |
| affected_surface | `original_description` | 65 | - Added missing beta `include_original_description` and `original_description` fields to `Transaction` |
| affected_surface | `Transaction` | 65 | - Added missing beta `include_original_description` and `original_description` fields to `Transaction` |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 56 | ### 2020-09-14_1.19.5 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 65 |  |

## Ticket 43

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Various small description fixes | 66 | - Various small description fixes |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 56 | ### 2020-09-14_1.19.5 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 66 |  |

## Ticket 44

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Updated external docs URLs for Income endpoints | 67 | - Updated external docs URLs for Income endpoints |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 56 | ### 2020-09-14_1.19.5 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 67 |  |

## Ticket 45

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fixed description for `close_price` field returned in `/investments/holdings/get` response | 70 | - Fixed description for `close_price` field returned in `/investments/holdings/get` response |
| affected_surface | `close_price` | 70 | - Fixed description for `close_price` field returned in `/investments/holdings/get` response |
| affected_surface | `/investments/holdings/get` | 70 | - Fixed description for `close_price` field returned in `/investments/holdings/get` response |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 69 | ### 2020-09-14_1.19.4 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 70 |  |

## Ticket 46

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Updated the `/institutions/get/` description to explain filtering behavior | 73 | - Updated the `/institutions/get/` description to explain filtering behavior |
| affected_surface | `/institutions/get/` | 73 | - Updated the `/institutions/get/` description to explain filtering behavior |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 72 | ### 2020-09-14_1.19.3 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 73 |  |

## Ticket 47

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `error` field to `/income/verification/summary/get` response body | 76 | - Added `error` field to `/income/verification/summary/get` response body |
| affected_surface | `error` | 76 | - Added `error` field to `/income/verification/summary/get` response body |
| affected_surface | `/income/verification/summary/get` | 76 | - Added `error` field to `/income/verification/summary/get` response body |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 75 | ### 2020-09-14_1.19.2 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 76 |  |

## Ticket 48

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fix links to income (beta) docs | 79 | - Fix links to income (beta) docs |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 78 | ### 2020-09-14_1.19.1 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 79 |  |

## Ticket 49

| field | value | line | quote |
| --- | --- | --- | --- |
| change | add income webhook example | 80 | - add income webhook example |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 78 | ### 2020-09-14_1.19.1 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 80 |  |

## Ticket 50

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `/sandbox/income/fire_webhook` endpoint | 83 | - Added `/sandbox/income/fire_webhook` endpoint |
| affected_surface | `/sandbox/income/fire_webhook` | 83 | - Added `/sandbox/income/fire_webhook` endpoint |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 82 | ### 2020-09-14_1.19.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 83 |  |

## Ticket 51

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added Lithic and SVB to the list of supported processors for `/processor/token/create` endpoint | 86 | - Added Lithic and SVB to the list of supported processors for `/processor/token/create` endpoint |
| affected_surface | `/processor/token/create` | 86 | - Added Lithic and SVB to the list of supported processors for `/processor/token/create` endpoint |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 85 | ### 2020-09-14_1.18.2 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 86 |  |

## Ticket 52

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fixed file to reflect that `category_id` and `next_payment_due_date` are nullable | 89 | - Fixed file to reflect that `category_id` and `next_payment_due_date` are nullable |
| affected_surface | `category_id` | 89 | - Fixed file to reflect that `category_id` and `next_payment_due_date` are nullable |
| affected_surface | `next_payment_due_date` | 89 | - Fixed file to reflect that `category_id` and `next_payment_due_date` are nullable |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 88 | ### 2020-09-14_1.18.1 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 89 |  |

## Ticket 53

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Removed spurious `paystub_id` field | 90 | - Removed spurious `paystub_id` field |
| affected_surface | `paystub_id` | 90 | - Removed spurious `paystub_id` field |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 88 | ### 2020-09-14_1.18.1 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 90 |  |

## Ticket 54

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added missing `SCHEDULED` value to `IncidentUpdate.status` enum | 91 | - Added missing `SCHEDULED` value to `IncidentUpdate.status` enum |
| affected_surface | `SCHEDULED` | 91 | - Added missing `SCHEDULED` value to `IncidentUpdate.status` enum |
| affected_surface | `IncidentUpdate.status` | 91 | - Added missing `SCHEDULED` value to `IncidentUpdate.status` enum |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 88 | ### 2020-09-14_1.18.1 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 91 |  |

## Ticket 55

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Various description fixes | 92 | - Various description fixes |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 88 | ### 2020-09-14_1.18.1 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 92 |  |

## Ticket 56

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `/item/application/scopes/update` endpoint | 96 | - Added `/item/application/scopes/update` endpoint |
| affected_surface | `/item/application/scopes/update` | 96 | - Added `/item/application/scopes/update` endpoint |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 94 | ### 2020-09-14_1.18.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 96 |  |

## Ticket 57

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fixed incorrect enum values for `update_type` | 97 | - Fixed incorrect enum values for `update_type` |
| affected_surface | `update_type` | 97 | - Fixed incorrect enum values for `update_type` |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 94 | ### 2020-09-14_1.18.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 97 |  |

## Ticket 58

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fixed file to reflect that `current` balance field is nullable. | 98 | - Fixed file to reflect that `current` balance field is nullable. |
| affected_surface | `current` | 98 | - Fixed file to reflect that `current` balance field is nullable. |
| affected_surface | balance | 98 | - Fixed file to reflect that `current` balance field is nullable. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 94 | ### 2020-09-14_1.18.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 98 |  |

## Ticket 59

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Description and textual fixes | 99 | - Description and textual fixes |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 94 | ### 2020-09-14_1.18.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 99 |  |

## Ticket 60

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fix invalid format errors | 100 | - Fix invalid format errors |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 94 | ### 2020-09-14_1.18.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 100 |  |

## Ticket 61

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Add new investment subtypes | 101 | - Add new investment subtypes |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 94 | ### 2020-09-14_1.18.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 101 |  |

## Ticket 62

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Small description fix for `/income/verification/create` and `/employers/search` | 104 | - Small description fix for `/income/verification/create` and `/employers/search` |
| affected_surface | `/income/verification/create` | 104 | - Small description fix for `/income/verification/create` and `/employers/search` |
| affected_surface | `/employers/search` | 104 | - Small description fix for `/income/verification/create` and `/employers/search` |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 103 | ### 2020-09-14_1.17.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 104 |  |

## Ticket 63

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fixed  `ytd_net_income` value in `IncomeVerificationSummaryGetResponse` example | 105 | - Fixed  `ytd_net_income` value in `IncomeVerificationSummaryGetResponse` example |
| affected_surface | `ytd_net_income` | 105 | - Fixed  `ytd_net_income` value in `IncomeVerificationSummaryGetResponse` example |
| affected_surface | `IncomeVerificationSummaryGetResponse` | 105 | - Fixed  `ytd_net_income` value in `IncomeVerificationSummaryGetResponse` example |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 103 | ### 2020-09-14_1.17.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 105 |  |

## Ticket 64

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fixed references to `paystub` to be plural `paystubs` for `/income/verification/paystubs/get` route and schemas | 106 | - Fixed references to `paystub` to be plural `paystubs` for `/income/verification/paystubs/get` route and schemas |
| affected_surface | `paystub` | 106 | - Fixed references to `paystub` to be plural `paystubs` for `/income/verification/paystubs/get` route and schemas |
| affected_surface | `paystubs` | 106 | - Fixed references to `paystub` to be plural `paystubs` for `/income/verification/paystubs/get` route and schemas |
| affected_surface | `/income/verification/paystubs/get` | 106 | - Fixed references to `paystub` to be plural `paystubs` for `/income/verification/paystubs/get` route and schemas |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 103 | ### 2020-09-14_1.17.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 106 |  |

## Ticket 65

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `PaystubEmployer` schema referenced in the `Paystub` object | 107 | - Added `PaystubEmployer` schema referenced in the `Paystub` object |
| affected_surface | `PaystubEmployer` | 107 | - Added `PaystubEmployer` schema referenced in the `Paystub` object |
| affected_surface | `Paystub` | 107 | - Added `PaystubEmployer` schema referenced in the `Paystub` object |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 103 | ### 2020-09-14_1.17.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 107 |  |

## Ticket 66

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `ItemApplicationScopesUpdateRequest` and `ItemApplicationScopesUpdateResponse` schema | 110 | - Added `ItemApplicationScopesUpdateRequest` and `ItemApplicationScopesUpdateResponse` schema |
| affected_surface | `ItemApplicationScopesUpdateRequest` | 110 | - Added `ItemApplicationScopesUpdateRequest` and `ItemApplicationScopesUpdateResponse` schema |
| affected_surface | `ItemApplicationScopesUpdateResponse` | 110 | - Added `ItemApplicationScopesUpdateRequest` and `ItemApplicationScopesUpdateResponse` schema |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 109 | ### 2020-09-14_1.16.6 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 110 |  |

## Ticket 67

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `emi_account_id` field to `PaymentInitiationPayment` model for `/payment_initiation/payment/get` and `/payment_initiation/payment/list` response | 113 | - Added `emi_account_id` field to `PaymentInitiationPayment` model for `/payment_initiation/payment/get` and `/payment_initiation/payment/list` response |
| affected_surface | `emi_account_id` | 113 | - Added `emi_account_id` field to `PaymentInitiationPayment` model for `/payment_initiation/payment/get` and `/payment_initiation/payment/list` response |
| affected_surface | `PaymentInitiationPayment` | 113 | - Added `emi_account_id` field to `PaymentInitiationPayment` model for `/payment_initiation/payment/get` and `/payment_initiation/payment/list` response |
| affected_surface | `/payment_initiation/payment/get` | 113 | - Added `emi_account_id` field to `PaymentInitiationPayment` model for `/payment_initiation/payment/get` and `/payment_initiation/payment/list` response |
| affected_surface | `/payment_initiation/payment/list` | 113 | - Added `emi_account_id` field to `PaymentInitiationPayment` model for `/payment_initiation/payment/get` and `/payment_initiation/payment/list` response |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 112 | ### 2020-09-14_1.16.5 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 113 |  |

## Ticket 68

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `emi_recipient_id` field to `PaymentInitiationRecipient` model for `/payment_initiation/recipient/get` and `/payment_initiation/recipient/list` response | 114 | - Added `emi_recipient_id` field to `PaymentInitiationRecipient` model for `/payment_initiation/recipient/get` and `/payment_initiation/recipient/list` response |
| affected_surface | `emi_recipient_id` | 114 | - Added `emi_recipient_id` field to `PaymentInitiationRecipient` model for `/payment_initiation/recipient/get` and `/payment_initiation/recipient/list` response |
| affected_surface | `PaymentInitiationRecipient` | 114 | - Added `emi_recipient_id` field to `PaymentInitiationRecipient` model for `/payment_initiation/recipient/get` and `/payment_initiation/recipient/list` response |
| affected_surface | `/payment_initiation/recipient/get` | 114 | - Added `emi_recipient_id` field to `PaymentInitiationRecipient` model for `/payment_initiation/recipient/get` and `/payment_initiation/recipient/list` response |
| affected_surface | `/payment_initiation/recipient/list` | 114 | - Added `emi_recipient_id` field to `PaymentInitiationRecipient` model for `/payment_initiation/recipient/get` and `/payment_initiation/recipient/list` response |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 112 | ### 2020-09-14_1.16.5 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 114 |  |

## Ticket 69

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Removes erroneous `request_id` that was incorrectly shown to be returned in items from `/payment_initiation/payment/list` and `/payment_initiation/recipient/list`. | 117 | - Removes erroneous `request_id` that was incorrectly shown to be returned in items from `/payment_initiation/payment/list` and `/payment_initiation/recipient/list`. |
| affected_surface | `request_id` | 117 | - Removes erroneous `request_id` that was incorrectly shown to be returned in items from `/payment_initiation/payment/list` and `/payment_initiation/recipient/list`. |
| affected_surface | `/payment_initiation/payment/list` | 117 | - Removes erroneous `request_id` that was incorrectly shown to be returned in items from `/payment_initiation/payment/list` and `/payment_initiation/recipient/list`. |
| affected_surface | `/payment_initiation/recipient/list` | 117 | - Removes erroneous `request_id` that was incorrectly shown to be returned in items from `/payment_initiation/payment/list` and `/payment_initiation/recipient/list`. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 116 | ### 2020-09-14_1.16.4 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 117 |  |

## Ticket 70

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fix for `ExternalPaymentSchedule` to make `end_date` optional. | 118 | - Fix for `ExternalPaymentSchedule` to make `end_date` optional. |
| affected_surface | `ExternalPaymentSchedule` | 118 | - Fix for `ExternalPaymentSchedule` to make `end_date` optional. |
| affected_surface | `end_date` | 118 | - Fix for `ExternalPaymentSchedule` to make `end_date` optional. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 116 | ### 2020-09-14_1.16.4 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 118 |  |

## Ticket 71

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Updated `/investments/transactions/get` count minimum to be 1 instead of 0 | 121 | - Updated `/investments/transactions/get` count minimum to be 1 instead of 0 |
| affected_surface | `/investments/transactions/get` | 121 | - Updated `/investments/transactions/get` count minimum to be 1 instead of 0 |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 120 | ### 2020-09-14_1.16.3 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 121 |  |

## Ticket 72

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fixes for required parameters for `JWKPublicKey` and `Security`. | 124 | - Fixes for required parameters for `JWKPublicKey` and `Security`. |
| affected_surface | `JWKPublicKey` | 124 | - Fixes for required parameters for `JWKPublicKey` and `Security`. |
| affected_surface | `Security` | 124 | - Fixes for required parameters for `JWKPublicKey` and `Security`. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 123 | ### 2020-09-14_1.16.2 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 124 |  |

## Ticket 73

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fix for `BankTransferMetadata` to be nullable. | 125 | - Fix for `BankTransferMetadata` to be nullable. |
| affected_surface | `BankTransferMetadata` | 125 | - Fix for `BankTransferMetadata` to be nullable. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 123 | ### 2020-09-14_1.16.2 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 125 |  |

## Ticket 74

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fixes for descriptions and linter errors. | 128 | - Fixes for descriptions and linter errors. |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 127 | ### 2020-09-14_1.16.1 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 128 |  |

## Ticket 75

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Updated `/payment_initiation/payment/create` with ability to pass in iban or account and sort code. If provided, the end user will be able to send payments only from the specified bank account. | 131 | - Updated `/payment_initiation/payment/create` with ability to pass in iban or account and sort code. If provided, the end user will be able to send payments only from the specified bank account. |
| affected_surface | `/payment_initiation/payment/create` | 131 | - Updated `/payment_initiation/payment/create` with ability to pass in iban or account and sort code. If provided, the end user will be able to send payments only from the specified bank account. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 130 | ### 2020-09-14_1.16.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 131 |  |

## Ticket 76

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Add clarifying max character line to client_name description. | 134 | - Add clarifying max character line to client_name description. |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 133 | ### 2020-09-14_1.15.1 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 134 |  |

## Ticket 77

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Removed erroneous `access_token` that was incorrectly shown to be returned by `/item/get`. | 138 | - Removed erroneous `access_token` that was incorrectly shown to be returned by `/item/get`. |
| affected_surface | `access_token` | 138 | - Removed erroneous `access_token` that was incorrectly shown to be returned by `/item/get`. |
| affected_surface | `/item/get` | 138 | - Removed erroneous `access_token` that was incorrectly shown to be returned by `/item/get`. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 136 | ### 2020-09-14_1.15.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 138 |  |

## Ticket 78

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `business` loan type. | 139 | - Added `business` loan type. |
| affected_surface | `business` | 139 | - Added `business` loan type. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 136 | ### 2020-09-14_1.15.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 139 |  |

## Ticket 79

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Clarified `date` format for `institution_price_as_of`. | 140 | - Clarified `date` format for `institution_price_as_of`. |
| affected_surface | `date` | 140 | - Clarified `date` format for `institution_price_as_of`. |
| affected_surface | `institution_price_as_of` | 140 | - Clarified `date` format for `institution_price_as_of`. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 136 | ### 2020-09-14_1.15.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 140 |  |

## Ticket 80

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Various small description fixes. | 141 | - Various small description fixes. |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 136 | ### 2020-09-14_1.15.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 141 |  |

## Ticket 81

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Updated `institutions/get`, `institutions/get_by_id`, and `institutions/search` to introduce an optional flag to return Payment Initiation metadata | 145 | - Updated `institutions/get`, `institutions/get_by_id`, and `institutions/search` to introduce an optional flag to return Payment Initiation metadata |
| affected_surface | `institutions/get` | 145 | - Updated `institutions/get`, `institutions/get_by_id`, and `institutions/search` to introduce an optional flag to return Payment Initiation metadata |
| affected_surface | `institutions/get_by_id` | 145 | - Updated `institutions/get`, `institutions/get_by_id`, and `institutions/search` to introduce an optional flag to return Payment Initiation metadata |
| affected_surface | `institutions/search` | 145 | - Updated `institutions/get`, `institutions/get_by_id`, and `institutions/search` to introduce an optional flag to return Payment Initiation metadata |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 143 | ### 2020-09-14_1.14.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 145 |  |

## Ticket 82

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Updated `institutions/search` to accept additional options to filter institutions by various Payment Initiation configurations. | 146 | - Updated `institutions/search` to accept additional options to filter institutions by various Payment Initiation configurations. |
| affected_surface | `institutions/search` | 146 | - Updated `institutions/search` to accept additional options to filter institutions by various Payment Initiation configurations. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 143 | ### 2020-09-14_1.14.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 146 |  |

## Ticket 83

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Updated `/accounts/balance/get` documentation to show `INVALID_FIELD` and `LAST_UPDATED_DATETIME_OUT_OF_RANGE` errors that will be returned for `capone-oauth` | 150 | - Updated `/accounts/balance/get` documentation to show `INVALID_FIELD` and `LAST_UPDATED_DATETIME_OUT_OF_RANGE` errors that will be returned for `capone-oauth` |
| affected_surface | `/accounts/balance/get` | 150 | - Updated `/accounts/balance/get` documentation to show `INVALID_FIELD` and `LAST_UPDATED_DATETIME_OUT_OF_RANGE` errors that will be returned for `capone-oauth` |
| affected_surface | `INVALID_FIELD` | 150 | - Updated `/accounts/balance/get` documentation to show `INVALID_FIELD` and `LAST_UPDATED_DATETIME_OUT_OF_RANGE` errors that will be returned for `capone-oauth` |
| affected_surface | `LAST_UPDATED_DATETIME_OUT_OF_RANGE` | 150 | - Updated `/accounts/balance/get` documentation to show `INVALID_FIELD` and `LAST_UPDATED_DATETIME_OUT_OF_RANGE` errors that will be returned for `capone-oauth` |
| affected_surface | `capone-oauth` | 150 | - Updated `/accounts/balance/get` documentation to show `INVALID_FIELD` and `LAST_UPDATED_DATETIME_OUT_OF_RANGE` errors that will be returned for `capone-oauth` |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 148 | ### 2020-09-14_1.13.3 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 150 |  |

## Ticket 84

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Add specific format attribute to `date_of_birth` under `LinkTokenCreateRequestUser`. | 154 | - Add specific format attribute to `date_of_birth` under `LinkTokenCreateRequestUser`. |
| affected_surface | `date_of_birth` | 154 | - Add specific format attribute to `date_of_birth` under `LinkTokenCreateRequestUser`. |
| affected_surface | `LinkTokenCreateRequestUser` | 154 | - Add specific format attribute to `date_of_birth` under `LinkTokenCreateRequestUser`. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 152 | ### 2020-09-14_1.13.2 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 154 |  |

## Ticket 85

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Remove `last_statement_balance` since it's never been populated and is being removed in the next version | 158 | - Remove `last_statement_balance` since it's never been populated and is being removed in the next version |
| affected_surface | `last_statement_balance` | 158 | - Remove `last_statement_balance` since it's never been populated and is being removed in the next version |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 156 | ### 2020-09-14_1.13.1 |
| effective_date | not in source |  |  |
| sunset_date | Remove `last_statement_balance` since it's never been populated and is being removed in the next version | 158 | - Remove `last_statement_balance` since it's never been populated and is being removed in the next version |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 158 |  |

## Ticket 86

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Correct investment transaction sells quantity to be negative | 159 | - Correct investment transaction sells quantity to be negative |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 156 | ### 2020-09-14_1.13.1 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 159 |  |

## Ticket 87

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Updated documentation to allow `minimum_payment_amount` to be set on loans with type `student`. | 160 | - Updated documentation to allow `minimum_payment_amount` to be set on loans with type `student`. |
| affected_surface | `minimum_payment_amount` | 160 | - Updated documentation to allow `minimum_payment_amount` to be set on loans with type `student`. |
| affected_surface | `student` | 160 | - Updated documentation to allow `minimum_payment_amount` to be set on loans with type `student`. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 156 | ### 2020-09-14_1.13.1 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 160 |  |

## Ticket 88

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `standing_orders` product type. | 164 | - Added `standing_orders` product type. |
| affected_surface | `standing_orders` | 164 | - Added `standing_orders` product type. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 162 | ### 2020-09-14_1.13.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 164 |  |

## Ticket 89

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `min_last_updated_datetime` option to `/accounts/balance/get` request. | 168 | - Added `min_last_updated_datetime` option to `/accounts/balance/get` request. |
| affected_surface | `min_last_updated_datetime` | 168 | - Added `min_last_updated_datetime` option to `/accounts/balance/get` request. |
| affected_surface | `/accounts/balance/get` | 168 | - Added `min_last_updated_datetime` option to `/accounts/balance/get` request. |
| breaking | not in source |  |  |
| entry_date | 2021-09-14 | 166 | ### 2021-09-14_1.12.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 168 |  |

## Ticket 90

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `last_updated_datetime` field to `Account` model for `/accounts/balance/get` response. | 169 | - Added `last_updated_datetime` field to `Account` model for `/accounts/balance/get` response. |
| affected_surface | `last_updated_datetime` | 169 | - Added `last_updated_datetime` field to `Account` model for `/accounts/balance/get` response. |
| affected_surface | `Account` | 169 | - Added `last_updated_datetime` field to `Account` model for `/accounts/balance/get` response. |
| affected_surface | `/accounts/balance/get` | 169 | - Added `last_updated_datetime` field to `Account` model for `/accounts/balance/get` response. |
| breaking | not in source |  |  |
| entry_date | 2021-09-14 | 166 | ### 2021-09-14_1.12.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 169 |  |

## Ticket 91

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Removed erroneous inclusion of `account_filters` as a parameter to `/institutions/search` | 173 | - Removed erroneous inclusion of `account_filters` as a parameter to `/institutions/search` |
| affected_surface | `account_filters` | 173 | - Removed erroneous inclusion of `account_filters` as a parameter to `/institutions/search` |
| affected_surface | a | 173 | - Removed erroneous inclusion of `account_filters` as a parameter to `/institutions/search` |
| affected_surface | `/institutions/search` | 173 | - Removed erroneous inclusion of `account_filters` as a parameter to `/institutions/search` |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 171 | ### 2020-09-14_1.11.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 173 |  |

## Ticket 92

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Text fixes to descriptions | 174 | - Text fixes to descriptions |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 171 | ### 2020-09-14_1.11.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 174 |  |

## Ticket 93

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Fixed incorrect field names in some models currently used only for documentation | 175 | - Fixed incorrect field names in some models currently used only for documentation |
| affected_surface | incorrect | 175 | - Fixed incorrect field names in some models currently used only for documentation |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 171 | ### 2020-09-14_1.11.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 175 |  |

## Ticket 94

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `BankTransfersEventsUpdateWebhook` schema | 179 | - Added `BankTransfersEventsUpdateWebhook` schema |
| affected_surface | `BankTransfersEventsUpdateWebhook` | 179 | - Added `BankTransfersEventsUpdateWebhook` schema |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 177 | ### 2020-09-14_1.10.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 179 |  |

## Ticket 95

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added new `auth` property to `/link/token/create` request to support Flexible Auth (currently in closed beta). | 183 | - Added new `auth` property to `/link/token/create` request to support Flexible Auth (currently in closed beta). |
| affected_surface | `auth` | 183 | - Added new `auth` property to `/link/token/create` request to support Flexible Auth (currently in closed beta). |
| affected_surface | `/link/token/create` | 183 | - Added new `auth` property to `/link/token/create` request to support Flexible Auth (currently in closed beta). |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 181 | ### 2020-09-14_1.9.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 183 |  |

## Ticket 96

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Text fixes to descriptions. | 184 | - Text fixes to descriptions. |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 181 | ### 2020-09-14_1.9.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 184 |  |

## Ticket 97

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `additionalProperties` to all objects to prevent additive keys from breaking. | 188 | - Added `additionalProperties` to all objects to prevent additive keys from breaking. |
| affected_surface | `additionalProperties` | 188 | - Added `additionalProperties` to all objects to prevent additive keys from breaking. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 186 | ### 2020-09-14_1.8.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 188 |  |

## Ticket 98

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added new propery to `Transaction` model, `authorized_datetime`, `datetime`. | 189 | - Added new propery to `Transaction` model, `authorized_datetime`, `datetime`. |
| affected_surface | `Transaction` | 189 | - Added new propery to `Transaction` model, `authorized_datetime`, `datetime`. |
| affected_surface | `authorized_datetime` | 189 | - Added new propery to `Transaction` model, `authorized_datetime`, `datetime`. |
| affected_surface | `datetime` | 189 | - Added new propery to `Transaction` model, `authorized_datetime`, `datetime`. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 186 | ### 2020-09-14_1.8.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 189 |  |

## Ticket 99

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Update `access_token` to `required` for `TransactionsGet`. | 190 | - Update `access_token` to `required` for `TransactionsGet`. |
| affected_surface | `access_token` | 190 | - Update `access_token` to `required` for `TransactionsGet`. |
| affected_surface | `required` | 190 | - Update `access_token` to `required` for `TransactionsGet`. |
| affected_surface | `TransactionsGet` | 190 | - Update `access_token` to `required` for `TransactionsGet`. |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 186 | ### 2020-09-14_1.8.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 190 |  |

## Ticket 100

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Require `origination_account_id` in `BankTransferBalanceGetResponse` | 191 | - Require `origination_account_id` in `BankTransferBalanceGetResponse` |
| affected_surface | `origination_account_id` | 191 | - Require `origination_account_id` in `BankTransferBalanceGetResponse` |
| affected_surface | `BankTransferBalanceGetResponse` | 191 | - Require `origination_account_id` in `BankTransferBalanceGetResponse` |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 186 | ### 2020-09-14_1.8.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 191 |  |

## Ticket 101

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Add new endpoint `/sandbox/bank_transfer/fire_webhook` | 192 | - Add new endpoint `/sandbox/bank_transfer/fire_webhook` |
| affected_surface | `/sandbox/bank_transfer/fire_webhook` | 192 | - Add new endpoint `/sandbox/bank_transfer/fire_webhook` |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 186 | ### 2020-09-14_1.8.0 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 192 |  |

## Ticket 102

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added new payment processors. | 196 | - Added new payment processors. |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 194 | ### 2020-09-14_1.5.3 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md raw-githubusercontent-com-plaid-plaid-openapi-84a303ae4a48816951233ba0db0ce24c7e-20260921T212216Z.txt | 196 |  |

## Unmapped

- 34: ### 2021-07-1_1.19.9
- 198: ### 2020-09-14_1.5.0
- 200: Initial version

```
