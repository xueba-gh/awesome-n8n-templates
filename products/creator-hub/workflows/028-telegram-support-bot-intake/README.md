# Support request intake from Telegram, WhatsApp or any chat tool

Receives messages from any chat bot that can call a webhook, logs them with AI category and urgency, and acknowledges by email if an address is given.

## What you need

- Google Sheets
- Gmail
- OpenAI API key

## Setup

1. Make a Google Sheet with a tab named **Chat requests** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets, Gmail, OpenAI).
4. Connect your chat bot platform (Telegram bot via n8n, Botpress, ManyChat, WhatsApp provider) to the **Webhook** URL.
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `name`, `email`, `message`, `category`, `urgency`, `summary`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
