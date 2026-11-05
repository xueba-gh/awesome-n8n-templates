# Appointment reminder text 24 hours before (Twilio)

Texts each client a reminder about 24 hours before their appointment, once, from your appointments sheet. Cuts no-shows.

## What you need

- Google Sheets
- Twilio account and phone number

## Setup

1. Make a sheet tab **Appointments** with the headers in `sheet-headers.csv`. Phone numbers in international format (+15551234567).
2. Open **Settings**: your business name, Twilio number, sheet URL.
3. Connect Twilio and Google Sheets. US numbers need A2P 10DLC registration in Twilio before texting.
4. Only text people who agreed to receive texts, and honour STOP replies. Run once with your own number, then switch to **Active**.

## Google Sheet columns (row 1)

`name`, `phone`, `appointment_at`, `service`, `reminder_sent`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
