# Receipt and invoice emails to an expense sheet (AI extraction)

Finds receipts in your inbox and logs vendor, date, amount and category into a sheet for bookkeeping.

## What you need

- Google Sheets
- Gmail
- OpenAI API key

## Setup

1. Make a Google Sheet with a tab named **Expenses** and paste the header row from `sheet-headers.csv`.
2. Open **Settings**: sheet URL and your email.
3. Connect Gmail (trigger and any Gmail node), Google Sheets and OpenAI on the nodes with warnings.
4. The trigger checks unread mail matching `in:inbox (receipt OR invoice OR "order confirmation" OR "payment received")` every minute. Change that search in **New email** to match your inbox.
5. Send yourself a test from another address, check the result, then switch to **Active**.

## Google Sheet columns (row 1)

`received_at`, `from_address`, `subject`, `message_id`, `is_receipt`, `vendor`, `date`, `total_amount`, `currency`, `category`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
