# Telegram FAQ bot that answers from your Google Sheet

A Telegram bot that answers customer questions using only the facts in your Google Sheet, and gives your phone number when it doesn't know.

## What you need

- Google Sheets
- OpenAI API key
- Telegram bot (from @BotFather)

## Setup

1. Create a bot with **@BotFather** in Telegram and copy its token into a Telegram credential in n8n (you paste it, nobody else).
2. Make a Google Sheet with a tab **Knowledge** and two headers: `topic`, `answer`. Add your real facts.
3. Open **Settings**: business name, phone, booking link, sheet URL.
4. Connect Telegram, Google Sheets and OpenAI, then switch to **Active** and message your bot.

## Google Sheet columns (row 1)

`topic`, `answer`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
