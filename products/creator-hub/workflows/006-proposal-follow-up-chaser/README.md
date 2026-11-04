# Proposal follow-up chaser (sends a nudge after 3 and 7 days)

Looks at your proposals sheet and emails a friendly nudge when a proposal has had no answer for 3 days, and a last note after 7.

## What you need

- Google Sheets
- Gmail

## Setup

1. Use a Google Sheet with a tab named **Proposals** and these headers in row 1: see `sheet-headers.csv`.
2. Open **Settings** and fill in your sheet URL, your email and names.
3. Connect Google Sheets and Gmail on the nodes with warnings.
4. Check the rule in **Find rows to act on** (it shows exactly which rows get an email) and the wording in **Send email**.
5. Run it once by hand with a test row, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`client_name`, `email`, `proposal`, `sent_date`, `status`, `nudges_sent`, `last_nudge_at`

## Good to know

After each send the **nudges_sent** column should go up by one. Add a number to that cell yourself or extend **Mark rows as done** if you want it automatic.

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
