# Order shipped email with tracking link

When an order ships (webhook from your shop or courier), emails the customer the tracking details and logs it.

## What you need

- Google Sheets
- Gmail

## Setup

1. Make a Google Sheet with a tab named **Shipments** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets, Gmail).
4. Send a POST from your shop's fulfilment webhook with the fields shown.
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `order_number`, `name`, `email`, `carrier`, `tracking_number`, `tracking_url`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
