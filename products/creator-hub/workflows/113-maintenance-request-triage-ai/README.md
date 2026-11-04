# Property maintenance request triage with AI urgency

Tenants submit a request. AI rates the urgency and trade needed, and you are emailed immediately for emergencies.

## What you need

- Google Sheets
- Gmail
- OpenAI API key

## Setup

1. Make a Google Sheet with a tab named **Maintenance requests** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets, Gmail, OpenAI).
4. Fill in the built-in form (open the form URL from the **Form** node).
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `name`, `email`, `unit`, `issue`, `urgency`, `trade`, `summary`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
