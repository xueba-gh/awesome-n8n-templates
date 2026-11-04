# Payment received thank-you email with receipt details

When a payment webhook arrives (Stripe, PayPal, Gumroad, Paddle, Lemon Squeezy) sends a plain thank-you with the details and logs it.

## What you need

- Google Sheets
- Gmail

## Setup

1. Make a Google Sheet with a tab named **Sales log** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets, Gmail).
4. Point your payment provider's webhook at the **Webhook** URL. Map the field names or rename keys to match.
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `customer_name`, `customer_email`, `product`, `amount`, `currency`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
