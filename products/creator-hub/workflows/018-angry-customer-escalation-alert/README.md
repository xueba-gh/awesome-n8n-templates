# Angry or at-risk customer email escalation alert

Spots emails that sound angry, threaten to cancel, or mention refunds or legal action, and alerts you right away with a calm suggested reply.

## What you need

- Google Sheets
- Gmail
- OpenAI API key

## Setup

1. Make a Google Sheet with a tab named **Escalations** and paste the header row from `sheet-headers.csv`.
2. Open **Settings**: sheet URL and your email.
3. Connect Gmail (trigger and any Gmail node), Google Sheets and OpenAI on the nodes with warnings.
4. The trigger checks unread mail matching `in:inbox -from:me` every minute. Change that search in **New email** to match your inbox.
5. Send yourself a test from another address, check the result, then switch to **Active**. Nothing is ever sent to customers: replies are saved as drafts.

## Google Sheet columns (row 1)

`received_at`, `from_address`, `subject`, `message_id`, `mood`, `churn_risk`, `needs_reply`, `summary`, `reply_draft`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
