# Webinar or event reminder email the day before

Emails registrants a reminder the day before the event, once.

## What you need

- Google Sheets
- Gmail

## Setup

1. Use a Google Sheet with a tab named **Registrants** and these headers in row 1: see `sheet-headers.csv`.
2. Open **Settings** and fill in your sheet URL, your email and names.
3. Connect Google Sheets and Gmail on the nodes with warnings.
4. Check the rule in **Find rows to act on** (it shows exactly which rows get an email) and the wording in **Send email**.
5. Run it once by hand with a test row, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`name`, `email`, `event_date`, `reminded`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
