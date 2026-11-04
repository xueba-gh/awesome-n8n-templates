# Quote follow-up for tradespeople (plumbers, electricians, builders)

Follows up on quotes you sent: a polite check-in after 3 days and a last note after 8 days.

## What you need

- Google Sheets
- Gmail

## Setup

1. Use a Google Sheet with a tab named **Quotes** and these headers in row 1: see `sheet-headers.csv`.
2. Open **Settings** and fill in your sheet URL, your email and names.
3. Connect Google Sheets and Gmail on the nodes with warnings.
4. Check the rule in **Find rows to act on** (it shows exactly which rows get an email) and the wording in **Send email**.
5. Run it once by hand with a test row, then switch the workflow to **Active**.

## Google Sheet columns (row 1)

`customer`, `email`, `job`, `quote_amount`, `sent_date`, `status`, `last_follow_up`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
