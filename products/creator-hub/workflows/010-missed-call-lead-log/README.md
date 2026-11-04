# Missed call log with instant follow-up email task

Logs every missed call (from any phone system that can send a webhook) and emails you a ready-to-use call-back note.

## What you need

- Google Sheets
- Gmail

## Setup

1. Make a Google Sheet with a tab named **Missed calls** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets, Gmail).
4. Most phone systems (Twilio, CallRail, Aircall, JustCall) can send a webhook on missed calls. Point it at the **Webhook** URL.
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `caller_name`, `phone`, `called_at`, `line`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
