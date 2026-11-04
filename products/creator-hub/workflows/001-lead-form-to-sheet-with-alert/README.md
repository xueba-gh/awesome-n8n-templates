# Website form to Google Sheet with instant thank-you email and owner alert

Every new website enquiry is saved to a Google Sheet, the person gets an instant thank-you email, and you get an alert email.

## What you need

- Google Sheets
- Gmail

## Setup

1. Make a Google Sheet with a tab named **Leads** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets, Gmail).
4. Send a POST request with the fields below to the **Webhook** URL (any form tool, Zapier, Make, or your own site can do this).
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `name`, `email`, `phone`, `message`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
