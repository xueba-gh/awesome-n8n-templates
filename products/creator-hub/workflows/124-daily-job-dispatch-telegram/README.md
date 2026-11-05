# Daily job list to each cleaner or field worker on Telegram

Every morning sends each worker their jobs for the day (time, client, address, notes) on Telegram, from one schedule sheet.

## What you need

- Google Sheets
- Telegram bot (from @BotFather)

## Setup

1. Create a Telegram bot with **@BotFather** and add its token as a Telegram credential in n8n. Send your bot a message, then get your chat ID (for example from @userinfobot).
2. Make a sheet tab **Jobs** with the headers in `sheet-headers.csv`. Each worker messages your bot once; put their chat ID in `worker_chat_id`.
3. Open **Settings**: sheet URL. Connect Google Sheets and Telegram.
4. Run it once with test data, then switch to **Active**.

## Google Sheet columns (row 1)

`date`, `time`, `worker`, `worker_chat_id`, `client`, `address`, `notes`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
