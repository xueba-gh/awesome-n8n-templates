# Purchase order request log with Slack approval ping

Team members request a purchase through a form. The request is logged and posted to Slack for the approver.

## What you need

- Google Sheets
- Slack

## Setup

1. Make a Google Sheet with a tab named **Purchase orders** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets, Slack).
4. Fill in the built-in form (open the form URL from the **Form** node).
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `name`, `email`, `item`, `cost`, `supplier`, `reason`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
