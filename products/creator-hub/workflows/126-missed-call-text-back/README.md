# Missed call text-back (Twilio): never lose a caller

Calls to your Twilio number ring your phone. If you don't answer, the caller instantly gets a friendly text, the call is logged and you get an email.

## What you need

- Google Sheets
- Gmail
- Twilio account and phone number

## Setup

1. Open **Settings** and **Settings for texts** (keep them the same): your phone, Twilio number, email, sheet URL. Make a sheet tab **Missed calls** with the headers in `sheet-headers.csv`.
2. Activate the workflow. Copy the production URL of **Call finished** into `dial_result_url` in **Settings**.
3. In Twilio, set your number's *A call comes in* webhook (POST) to the production URL of **Incoming call**.
4. Connect Twilio, Google Sheets and Gmail. Call your Twilio number and don't answer to test.
5. US numbers: texting needs A2P 10DLC registration in Twilio first.

## Google Sheet columns (row 1)

`called_at`, `caller`, `status`, `texted_back`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
