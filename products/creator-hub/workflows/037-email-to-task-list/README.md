# Turn emails into a task list (action items extracted by AI)

Reads new emails and adds a row for each one that contains something you must do, with a due date if mentioned.

## What you need

- Google Sheets
- Gmail
- OpenAI API key

## Setup

1. Make a Google Sheet with a tab named **Tasks** and paste the header row from `sheet-headers.csv`.
2. Open **Settings**: sheet URL and your email.
3. Connect Gmail (trigger and any Gmail node), Google Sheets and OpenAI on the nodes with warnings.
4. The trigger checks unread mail matching `in:inbox -from:me` every minute. Change that search in **New email** to match your inbox.
5. Send yourself a test from another address, check the result, then switch to **Active**.

## Google Sheet columns (row 1)

`received_at`, `from_address`, `subject`, `message_id`, `has_task`, `task`, `due_date`, `priority`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
