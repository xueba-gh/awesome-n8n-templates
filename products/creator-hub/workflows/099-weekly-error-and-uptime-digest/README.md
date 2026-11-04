# Weekly digest of logged errors and incidents

Reads an incident or error log sheet and sends a weekly summary: counts, repeat offenders and suggested fixes.

## What you need

- Google Sheets
- Gmail
- OpenAI API key

## Setup

1. Use a Google Sheet with a tab named **Incidents** and these headers in row 1 (see `sheet-headers.csv`).
2. Open **Settings**: sheet URL and the email that should receive the summary.
3. Connect Google Sheets, Gmail and OpenAI on the nodes with warnings.
4. Run once by hand to see the email, then switch the workflow to **Active** (it runs on the schedule in the first node).

## Google Sheet columns (row 1)

`date`, `system`, `severity`, `message`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
