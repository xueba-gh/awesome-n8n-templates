# Webhook logger: save any incoming webhook to Google Sheets

A tiny, reusable starting point. Point any service at the webhook and its fields land in a sheet, so you can see exactly what it sends.

## What you need

- Google Sheets

## Setup

1. Make a Google Sheet with a tab named **Webhook log** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets).
4. Send a POST with any of the fields listed. Edit the field list in **Clean up details** to match your service.
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `event`, `id`, `email`, `name`, `status`, `amount`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
