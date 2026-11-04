# Lead routing to sales reps by territory, with Slack alert

Logs each new lead and posts it in Slack so a rep can act in minutes. Add your own routing rule (see notes) to assign by country or keyword.

## What you need

- Google Sheets
- Slack

## Setup

1. Make a Google Sheet with a tab named **Routed leads** and paste the header row from `sheet-headers.csv` (first row).
2. Open **Settings** and fill in your sheet URL, email and names.
3. Connect your accounts on every node with a warning (Google Sheets, Slack).
4. Send a POST request with the fields below to the **Webhook** URL (any form tool, Zapier, Make, or your own site can do this).
5. Click **Execute workflow**, send a test, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`received_at`, `name`, `email`, `company`, `country`, `message`

## Good to know

This template logs and alerts. To assign by rule, add an IF/Switch node on the **country** field after **Clean up details**.

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
