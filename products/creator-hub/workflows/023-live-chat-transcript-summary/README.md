# Live chat transcript summary and follow-up log

Send finished chat transcripts to a webhook. AI writes a short summary, outcome and follow-up task, saved to your sheet.

## What you need

- Google Sheets
- Gmail
- OpenAI API key

## Setup

1. Make a Google Sheet with a tab named **Chat summaries** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets, Gmail, OpenAI).
4. Most chat tools (Crisp, Tidio, Intercom, Tawk.to) can send a webhook when a chat ends. Map the transcript to the **transcript** field.
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `customer`, `email`, `transcript`, `summary`, `outcome`, `follow_up`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
