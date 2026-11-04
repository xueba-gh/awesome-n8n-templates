# Lead company enrichment with AI (industry and size guess)

For each new lead with a company name and website, fills in a likely industry and a short outreach angle. Meant as a quick first pass, always double-check.

## What you need

- Google Sheets
- OpenAI API key

## Setup

1. Use a Google Sheet with a tab named **Leads** and these headers in row 1 (see `sheet-headers.csv`).
2. Fill the input columns (company). Leave industry, outreach_angle empty: the AI fills it.
3. Open **Settings**: sheet URL and how many rows to process per run.
4. Connect Google Sheets and OpenAI on the nodes with warnings.
5. Run once by hand, check the results, then switch to **Active**. It only touches rows where industry is empty.

## Google Sheet columns (row 1)

`name`, `email`, `company`, `website`, `industry`, `outreach_angle`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
