# VIP email alert to Telegram

When an email arrives from someone on your VIP list (or a whole company domain), you get a Telegram message with the subject and first lines.

## What you need

- Gmail
- Telegram bot (from @BotFather)

## Setup

1. Create a Telegram bot with **@BotFather** and add its token as a Telegram credential in n8n. Send your bot a message, then get your chat ID (for example from @userinfobot).
2. Open **Settings**: your Telegram chat ID and the VIP list (full addresses, or `@domain.com` for a whole company).
3. Connect Gmail and Telegram.
4. Run it once with test data, then switch to **Active**.

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
