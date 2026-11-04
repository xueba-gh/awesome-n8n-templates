# Abandoned cart recovery email

When a checkout is abandoned, emails the customer a friendly reminder with a link back to the cart.

## What you need

- Google Sheets
- Gmail

## Setup

1. Make a Google Sheet with a tab named **Abandoned carts** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets, Gmail).
4. Shopify can send a webhook on checkout creation or abandonment; WooCommerce needs a cart-abandonment plugin that calls a webhook. Point it at the **Webhook** URL.
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `email`, `name`, `cart_url`, `total_price`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
