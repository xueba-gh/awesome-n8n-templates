# Stripe payments to Google Sheet ledger with thank-you email

Logs every successful Stripe payment in a sheet and optionally emails a thank-you. A simple ledger without exporting CSVs.

## What you need

- Google Sheets
- Gmail

## Setup

1. Make a Google Sheet with a tab named **Payments** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets, Gmail).
4. In Stripe go to Developers > Webhooks, add this **Webhook** URL and send the `payment_intent.succeeded` event. Amounts from Stripe are in cents.
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `id`, `customer_email`, `amount`, `currency`, `status`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
