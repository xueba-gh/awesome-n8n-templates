# Daily digest: which logged emails still need a reply

Every morning emails you a short list of logged messages that are still waiting for an answer, most urgent first.

## What you need

- Google Sheets
- Gmail
- OpenAI API key

## Setup

1. Use a Google Sheet with a tab named **Inbox log** and these headers in row 1 (see `sheet-headers.csv`).
2. Open **Settings**: sheet URL and the email that should receive the summary.
3. Connect Google Sheets, Gmail and OpenAI on the nodes with warnings.
4. Run once by hand to see the email, then switch the workflow to **Active** (it runs on the schedule in the first node).

## Google Sheet columns (row 1)

`received_at`, `from_address`, `subject`, `summary`, `needs_reply`, `urgent`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
