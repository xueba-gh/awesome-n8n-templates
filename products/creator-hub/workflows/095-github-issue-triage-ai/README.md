# GitHub issue triage with AI labels and summary

Receives GitHub issue webhooks, has AI suggest a label and priority, logs them, and emails you for bugs marked high priority.

## What you need

- Google Sheets
- Gmail
- OpenAI API key

## Setup

1. Make a Google Sheet with a tab named **Issues** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets, Gmail, OpenAI).
4. In your GitHub repo go to Settings > Webhooks, add this **Webhook** URL, content type application/json, event: Issues.
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `title`, `body`, `html_url`, `user_login`, `label`, `priority`, `summary`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
