# SEO title and meta description writer for a list of pages

List your page URLs and topics in a sheet. The AI writes an SEO title and meta description for each one that does not have one.

## What you need

- Google Sheets
- OpenAI API key

## Setup

1. Use a Google Sheet with a tab named **Pages** and these headers in row 1 (see `sheet-headers.csv`).
2. Fill the input columns (topic). Leave seo_title, meta_description empty: the AI fills it.
3. Open **Settings**: sheet URL and how many rows to process per run.
4. Connect Google Sheets and OpenAI on the nodes with warnings.
5. Run once by hand, check the results, then switch to **Active**. It only touches rows where seo_title is empty.

## Google Sheet columns (row 1)

`url`, `topic`, `keyword`, `seo_title`, `meta_description`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
