# New website lead to Google Sheet with instant Telegram alert

Every form submission is saved to a sheet and pinged to your Telegram straight away, so you can call while the lead is hot.

## What you need

- Google Sheets
- Telegram bot (from @BotFather)

## Setup

1. Create a Telegram bot with **@BotFather** and add its token as a Telegram credential in n8n. Send your bot a message, then get your chat ID (for example from @userinfobot).
2. Open **Settings**: your Telegram chat ID, sheet URL. Send the form's POST to the **Webhook** URL.
3. Make a sheet tab **Leads** with the headers in `sheet-headers.csv`, then connect Google Sheets and Telegram.
4. Run it once with test data, then switch to **Active**.

## Google Sheet columns (row 1)

`received_at`, `name`, `email`, `phone`, `message`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
