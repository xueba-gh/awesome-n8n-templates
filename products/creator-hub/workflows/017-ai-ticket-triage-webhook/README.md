# AI ticket triage for any helpdesk or form (priority and category)

Send any support request to a webhook. AI sets the priority and category, logs it, and emails you only about high-priority tickets. The sender gets an automatic acknowledgement.

## What you need

- Google Sheets
- Gmail
- OpenAI API key

## Setup

1. Make a Google Sheet with a tab named **Tickets** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets, Gmail, OpenAI).
4. Send a POST request with the fields below to the **Webhook** URL (any form tool, Zapier, Make, or your own site can do this).
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `name`, `email`, `subject`, `message`, `priority`, `category`, `summary`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
