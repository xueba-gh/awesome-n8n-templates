# Stripe failed-payment recovery email

When a Stripe payment fails, emails the customer a friendly note with a link to update their card, and alerts you.

## What you need

- Google Sheets
- Gmail

## Setup

1. Make a Google Sheet with a tab named **Failed payments** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets, Gmail).
4. In Stripe add this **Webhook** URL and send the `invoice.payment_failed` or `payment_intent.payment_failed` event.
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `id`, `customer_email`, `amount`, `currency`, `failure_message`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
