# New order to Google Sheet with Slack alert (Shopify or WooCommerce webhook)

Logs every new order in a sheet and pings Slack, so your team sees sales as they happen.

## What you need

- Google Sheets
- Slack

## Setup

1. Make a Google Sheet with a tab named **Orders** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets, Slack).
4. In Shopify (Settings > Notifications > Webhooks, event Order creation) or WooCommerce (Settings > Advanced > Webhooks) add this **Webhook** URL.
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `order_number`, `name`, `email`, `total_price`, `currency`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
