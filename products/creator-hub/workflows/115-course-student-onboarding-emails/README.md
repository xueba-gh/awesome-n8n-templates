# Course student onboarding: welcome email and enrolment log

When someone enrols (form or payment webhook), they get a welcome email with access details and the enrolment is logged.

## What you need

- Google Sheets
- Gmail

## Setup

1. Make a Google Sheet with a tab named **Enrolments** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets, Gmail).
4. Point your checkout or course platform's webhook at the **Webhook** URL (name, email, course).
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `name`, `email`, `course`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
