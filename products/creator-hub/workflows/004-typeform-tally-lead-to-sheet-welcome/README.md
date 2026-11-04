# Typeform / Tally / Jotform submission to Google Sheet with welcome email

Works with any form tool that can send a webhook. Saves the answers to a sheet and sends a welcome email.

## What you need

- Google Sheets
- Gmail

## Setup

1. Make a Google Sheet with a tab named **Form leads** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets, Gmail).
4. In Typeform, Tally or Jotform add a webhook pointing at this workflow's **Webhook** URL. Answers are matched by field name (name, email, company, interest).
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `name`, `email`, `company`, `interest`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
