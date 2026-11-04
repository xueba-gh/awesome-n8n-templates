# Deal won / lost log with email notification

Send a webhook when a deal closes. It is logged in a sheet and you get a short email, so you can keep a simple win/loss record.

## What you need

- Google Sheets
- Gmail

## Setup

1. Make a Google Sheet with a tab named **Closed deals** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets, Gmail).
4. Send a POST from your CRM (HubSpot, Pipedrive, GoHighLevel workflows can all call a webhook) with deal, contact, outcome (won or lost), value and reason.
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `deal`, `contact`, `outcome`, `value`, `reason`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
