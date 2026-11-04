# Calendly booking to Google Sheet with prep email

When someone books a call in Calendly, saves them to a sheet and emails a short prep note so the call starts well.

## What you need

- Google Sheets
- Gmail

## Setup

1. Make a Google Sheet with a tab named **Bookings** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets, Gmail).
4. In Calendly add a webhook subscription (invitee.created) to this workflow's **Webhook** URL. Calendly nests the data; the workflow flattens it, so keys like name, email, start_time and event_type are picked up.
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `name`, `email`, `start_time`, `event_type`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
