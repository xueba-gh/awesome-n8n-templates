# Event and booking confirmations summary to a sheet

Finds booking confirmations (flights, hotels, appointments) in Gmail and logs what, when and where in a sheet.

## What you need

- Google Sheets
- Gmail
- OpenAI API key

## Setup

1. Make a Google Sheet with a tab named **Bookings** and paste the header row from `sheet-headers.csv`.
2. Open **Settings**: sheet URL and your email.
3. Connect Gmail (trigger and any Gmail node), Google Sheets and OpenAI on the nodes with warnings.
4. The trigger checks unread mail matching `in:inbox (confirmation OR booking OR reservation OR itinerary)` every minute. Change that search in **New email** to match your inbox.
5. Send yourself a test from another address, check the result, then switch to **Active**.

## Google Sheet columns (row 1)

`received_at`, `from_address`, `subject`, `message_id`, `is_booking`, `what`, `date_time`, `location`, `confirmation_code`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
