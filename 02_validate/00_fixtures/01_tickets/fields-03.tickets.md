snapshot: changelog-01.txt
sha256: 4c2654fbd035a350c1f1c67b40cf4cd46836a5edbd9d9bb18c89667b55ea7e41
source_url: https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md
body_range: 1-200
line_numbers: snapshot

## Ticket 1

| field | value | line | quote |
| --- | --- | --- | --- |
| change | Added `format:` labels to all date and date-time strings | 2 | - Added `format:` labels to all date and date-time strings |
| affected_surface | not in source |  |  |
| breaking | not in source |  |  |
| entry_date | 2020-09-14 | 1 | ### 2020-09-14_1.20.6 |
| effective_date | not in source |  |  |
| sunset_date | not in source |  |  |
| required_action | not in source |  |  |
| priority | high | 2 | - Added `format:` labels to all date and date-time strings |
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md changelog-01.txt | 2 |  |

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
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md changelog-01.txt | 3 |  |

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
| source | https://raw.githubusercontent.com/plaid/plaid-openapi/84a303ae4a48816951233ba0db0ce24c7e633c9d/CHANGELOG.md changelog-01.txt | 4 |  |

## Unmapped

- 5: ### 2020-09-14_1.20.5
- 6: - Updated `Select Account` to `Account Select`
- 7: ### 2020-09-14_1.20.4
- 8: - Update Signal risk tier definitions
- 9: ### 2020-09-14_1.20.3
- 10: - Bug fixes to signal endpoints
- 11: ### 2020-09-14_1.20.1
- 12: - Added `/sandbox/oauth/select_accounts` endpoint.
- 13: ### 2021-07-27_1.20.0
- 14: - Added `liabilities_updates`, `liabilities`, and `investments` to institution schema
- 15: ### 2020-09-14_1.20.0
- 16: - Added `/signal/evaluate` endpoint
- 17: - Added `/signal/decision/report` endpoint
- 18: - Added `/signal/return/report` endpoint
- 19: - Added `/income/verification/refresh` endpoint.
- 20: ### 2020-09-14_1.19.12
- 21: - Added `alpaca`, `astra` and `moov` processors.
- 22: - Changed naming for some nullable parameters from `NullableParam` to `ParamNullable`.
- 23: - Added `/processor/bank_transfer/create` endpoint.
- 24: - Changed the inherited model for `AssetReportTransaction` from `Transaction` to `TransactionBase` which has fewer required fields.
- 26: ### 2020-09-14_1.19.11
- 27: - Added `logo_url` as a required value of `ConnectedApplications`
- 28: - Made `logo` a deprecated value of `ConnectedApplications` soon to be removed in future versions
- 30: ### 2020-09-14_1.19.10
- 31: - Added `income` back to the list of possible products as it's in sandbox return values.
- 32: - Made `switch_method` nullable as the sandbox deposit/switch response has it nulled.
- 34: ### 2021-07-1_1.19.9
- 35: - Added `CountryCode` to the request fields of `deposit_switch/create` and `deposit_switch/alt/create`
- 36: - Added `TransactionAccessTokens` to `DepositSwitchCreateOptions`
- 38: ### 2020-09-14_1.19.8
- 39: - Added `options` field to request body for `deposit_switch/create` and `deposit_switch/alt/create` endpoints
- 40: - Added webhook documentation for `deposit_switch/`
- 41: - Added a new state to the list of possible values for the `state` field in the response body, and updated descriptions of all states
- 43: ### 2020-09-14_1.19.7
- 44: - Added `ItemApplicationListUserAuth` component
- 45: - Added `user_auth` as a private field in `/item/application/list` request
- 46: - Changed `/item/application/list` request `access_token` field from `AccessToken` to `NullableAccessToken` to support `user_auth` flow (`/item/application/list` can be queried using `user_auth` instead of an access token for certain clients)
- 48: ### 2020-09-14_1.19.6
- 49: - Added the following response fields to the `/deposit_switch/get` docs:
- 50:     + `switch_method`
- 51:     + `employer_name`
- 52:     + `employer_id`
- 53:     + `institution_name`
- 54:     + `institution_id`
- 56: ### 2020-09-14_1.19.5
- 57: - Added `required` to many fields where it was missing
- 58: - Removed `nullable: true` annotation incorrectly applied to some fields
- 59: - Added ``nullable: true` annotation incorrectly missing from some fields
- 60: - Fixed invalid example for `/processor/balance/get`
- 61: - Fixed incorrect formatting for certain `allOf` structures
- 62: - Added enum values for some strings that were not treated as enums
- 63: - Added missing `created_at` field to `Application`
- 64: - Added missing `null` enum to some nullable enums
- 65: - Added missing beta `include_original_description` and `original_description` fields to `Transaction`
- 66: - Various small description fixes
- 67: - Updated external docs URLs for Income endpoints
- 69: ### 2020-09-14_1.19.4
- 70: - Fixed description for `close_price` field returned in `/investments/holdings/get` response
- 72: ### 2020-09-14_1.19.3
- 73: - Updated the `/institutions/get/` description to explain filtering behavior
- 75: ### 2020-09-14_1.19.2
- 76: - Added `error` field to `/income/verification/summary/get` response body
- 78: ### 2020-09-14_1.19.1
- 79: - Fix links to income (beta) docs
- 80: - add income webhook example
- 82: ### 2020-09-14_1.19.0
- 83: - Added `/sandbox/income/fire_webhook` endpoint
- 85: ### 2020-09-14_1.18.2
- 86: - Added Lithic and SVB to the list of supported processors for `/processor/token/create` endpoint
- 88: ### 2020-09-14_1.18.1
- 89: - Fixed file to reflect that `category_id` and `next_payment_due_date` are nullable
- 90: - Removed spurious `paystub_id` field
- 91: - Added missing `SCHEDULED` value to `IncidentUpdate.status` enum
- 92: - Various description fixes
- 94: ### 2020-09-14_1.18.0
- 96: - Added `/item/application/scopes/update` endpoint
- 97: - Fixed incorrect enum values for `update_type`
- 98: - Fixed file to reflect that `current` balance field is nullable.
- 99: - Description and textual fixes
- 100: - Fix invalid format errors
- 101: - Add new investment subtypes
- 103: ### 2020-09-14_1.17.0
- 104: - Small description fix for `/income/verification/create` and `/employers/search`
- 105: - Fixed  `ytd_net_income` value in `IncomeVerificationSummaryGetResponse` example
- 106: - Fixed references to `paystub` to be plural `paystubs` for `/income/verification/paystubs/get` route and schemas
- 107: - Added `PaystubEmployer` schema referenced in the `Paystub` object
- 109: ### 2020-09-14_1.16.6
- 110: - Added `ItemApplicationScopesUpdateRequest` and `ItemApplicationScopesUpdateResponse` schema
- 112: ### 2020-09-14_1.16.5
- 113: - Added `emi_account_id` field to `PaymentInitiationPayment` model for `/payment_initiation/payment/get` and `/payment_initiation/payment/list` response
- 114: - Added `emi_recipient_id` field to `PaymentInitiationRecipient` model for `/payment_initiation/recipient/get` and `/payment_initiation/recipient/list` response
- 116: ### 2020-09-14_1.16.4
- 117: - Removes erroneous `request_id` that was incorrectly shown to be returned in items from `/payment_initiation/payment/list` and `/payment_initiation/recipient/list`.
- 118: - Fix for `ExternalPaymentSchedule` to make `end_date` optional.
- 120: ### 2020-09-14_1.16.3
- 121: - Updated `/investments/transactions/get` count minimum to be 1 instead of 0
- 123: ### 2020-09-14_1.16.2
- 124: - Fixes for required parameters for `JWKPublicKey` and `Security`.
- 125: - Fix for `BankTransferMetadata` to be nullable.
- 127: ### 2020-09-14_1.16.1
- 128: - Fixes for descriptions and linter errors.
- 130: ### 2020-09-14_1.16.0
- 131: - Updated `/payment_initiation/payment/create` with ability to pass in iban or account and sort code. If provided, the end user will be able to send payments only from the specified bank account.
- 133: ### 2020-09-14_1.15.1
- 134: - Add clarifying max character line to client_name description.
- 136: ### 2020-09-14_1.15.0
- 138: - Removed erroneous `access_token` that was incorrectly shown to be returned by `/item/get`.
- 139: - Added `business` loan type.
- 140: - Clarified `date` format for `institution_price_as_of`.
- 141: - Various small description fixes.
- 143: ### 2020-09-14_1.14.0
- 145: - Updated `institutions/get`, `institutions/get_by_id`, and `institutions/search` to introduce an optional flag to return Payment Initiation metadata
- 146: - Updated `institutions/search` to accept additional options to filter institutions by various Payment Initiation configurations.
- 148: ### 2020-09-14_1.13.3
- 150: - Updated `/accounts/balance/get` documentation to show `INVALID_FIELD` and `LAST_UPDATED_DATETIME_OUT_OF_RANGE` errors that will be returned for `capone-oauth`
- 152: ### 2020-09-14_1.13.2
- 154: - Add specific format attribute to `date_of_birth` under `LinkTokenCreateRequestUser`.
- 156: ### 2020-09-14_1.13.1
- 158: - Remove `last_statement_balance` since it's never been populated and is being removed in the next version
- 159: - Correct investment transaction sells quantity to be negative
- 160: - Updated documentation to allow `minimum_payment_amount` to be set on loans with type `student`.
- 162: ### 2020-09-14_1.13.0
- 164: - Added `standing_orders` product type.
- 166: ### 2021-09-14_1.12.0
- 168: - Added `min_last_updated_datetime` option to `/accounts/balance/get` request.
- 169: - Added `last_updated_datetime` field to `Account` model for `/accounts/balance/get` response.
- 171: ### 2020-09-14_1.11.0
- 173: - Removed erroneous inclusion of `account_filters` as a parameter to `/institutions/search`
- 174: - Text fixes to descriptions
- 175: - Fixed incorrect field names in some models currently used only for documentation
- 177: ### 2020-09-14_1.10.0
- 179: - Added `BankTransfersEventsUpdateWebhook` schema
- 181: ### 2020-09-14_1.9.0
- 183: - Added new `auth` property to `/link/token/create` request to support Flexible Auth (currently in closed beta).
- 184: - Text fixes to descriptions.
- 186: ### 2020-09-14_1.8.0
- 188: - Added `additionalProperties` to all objects to prevent additive keys from breaking.
- 189: - Added new propery to `Transaction` model, `authorized_datetime`, `datetime`.
- 190: - Update `access_token` to `required` for `TransactionsGet`.
- 191: - Require `origination_account_id` in `BankTransferBalanceGetResponse`
- 192: - Add new endpoint `/sandbox/bank_transfer/fire_webhook`
- 194: ### 2020-09-14_1.5.3
- 196: - Added new payment processors.
- 198: ### 2020-09-14_1.5.0
- 200: Initial version
