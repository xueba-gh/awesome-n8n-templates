# Deployment notifications to Slack and a sheet

Any CI/CD tool can send a webhook. Every deployment is logged in a sheet and announced in Slack.

## What you need

- Google Sheets
- Slack

## Setup

1. Make a Google Sheet with a tab named **Deployments** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets, Slack).
4. Add a webhook step to your pipeline (GitHub Actions, GitLab CI, Vercel, Netlify) that POSTs project, environment, status, commit and author.
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `project`, `environment`, `status`, `commit`, `author`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
