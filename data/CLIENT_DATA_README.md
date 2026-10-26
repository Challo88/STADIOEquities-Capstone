# STADIOEquities — Account Activation Prediction: Data Extract

Extract supplied in response to the Part C data request. Five tables covering registrations from September 2023 to August 2025. All datetimes are UTC (`yyyy-MM-dd HH:mm:ss`); nulls are empty fields. Join all tables on `account_id`. PII has been excluded.

## Files

### `01_account_registration.csv`
Account-level registration, KYC and first-deposit records. Target variable: `activated_30day_flag`.  
Rows: 1,882

| Column | Description |
|---|---|
| `account_id` | String |
| `registration_datetime` | Datetime |
| `registration_source` | Categorical |
| `acquisition_channel` | Categorical |
| `campaign_id` | String |
| `onboarding_steps_completed` | Integer |
| `kyc_status` | Categorical |
| `kyc_completion_datetime` | Datetime |
| `kyc_time_to_complete_hours` | Numeric |
| `first_login_datetime` | Datetime |
| `first_deposit_datetime` | Datetime |
| `first_deposit_amount_zar` | Numeric |
| `time_to_first_deposit_hours` | Numeric |
| `activated_30day_flag` | Boolean |
| `days_since_registration` | Integer |
| `account_status` | Categorical |

### `02_behavioural_events.csv`
Event-level app/web interactions in the first 30 days, with account-level aggregate features carried on each row.  
Rows: 11,071

| Column | Description |
|---|---|
| `event_id` | String |
| `account_id` | String |
| `event_datetime` | Datetime |
| `event_type` | Categorical |
| `page_screen_name` | Categorical |
| `days_since_registration` | Integer |
| `session_id` | String |
| `session_duration_seconds` | Integer |
| `num_sessions_first_7_days` | Integer |
| `num_sessions_days_8_30` | Integer |
| `deepest_onboarding_screen_reached` | Categorical |
| `tutorial_completion` | Boolean |
| `stocks_searched` | Integer |
| `portfolio_page_views` | Integer |
| `deposit_page_views` | Integer |
| `notification_opens_first_7_days` | Integer |
| `error_events_first_7_days` | Integer |
| `days_since_last_session` | Integer |

### `03_client_demographics.csv`
Self-reported demographic and investor-profile attributes captured at registration.  
Rows: 1,882

| Column | Description |
|---|---|
| `account_id` | String |
| `age` | Integer |
| `age_group` | Categorical |
| `gender` | Categorical |
| `province` | Categorical |
| `country` | Categorical |
| `employment_status` | Categorical |
| `income_bracket` | Categorical |
| `investment_experience` | Categorical |
| `investment_goal` | Categorical |
| `risk_appetite` | Categorical |
| `referral_code` | String |

### `04_marketing_engagement.csv`
Marketing communications sent per account and engagement outcomes.  
Rows: 13,582

| Column | Description |
|---|---|
| `communication_id` | String |
| `account_id` | String |
| `communication_datetime` | Datetime |
| `communication_channel` | Categorical |
| `communication_type` | Categorical |
| `days_since_registration` | Integer |
| `opened` | Boolean |
| `clicked` | Boolean |
| `opened_within_1_hour` | Boolean |
| `total_emails_sent_30d` | Integer |
| `total_emails_opened_30d` | Integer |
| `total_push_sent_30d` | Integer |
| `total_push_opened_30d` | Integer |
| `total_nudges_sent_30d` | Integer |
| `cost_per_acquisition_zar` | Numeric |

### `05_product_subscription.csv`
Premium subscription status and value-added product interaction counts.  
Rows: 1,877

| Column | Description |
|---|---|
| `account_id` | String |
| `premium_subscription_status` | Categorical |
| `premium_offer_shown` | Boolean |
| `premium_offer_click` | Boolean |
| `premium_subscription_date` | Datetime |
| `value_added_products_viewed` | Integer |
| `product_comparison_page_views` | Integer |

## Data quality notes

This is an extract from live operational systems and has **not** been cleaned. Expect:

- Missing values in optional / conditionally-populated fields
- Inconsistent casing and stray whitespace in some free-text and categorical fields
- A small number of duplicate records
- Occasional out-of-range or implausible values from data-capture errors
- Some date fields captured in inconsistent formats

**Target variable:** `activated_30day_flag` in `01_account_registration.csv` — True if the account made its first deposit within 30 days of registration.

_Synthetic data supplied for the CAP182 capstone project. Not real client data._