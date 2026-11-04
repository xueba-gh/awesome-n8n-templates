# FAQ answer writer from rough notes in a sheet

Turn your rough notes into clear, customer-friendly FAQ answers, one per row.

## What you need

- Google Sheets
- OpenAI API key

## Setup

1. Use a Google Sheet with a tab named **FAQ** and these headers in row 1 (see `sheet-headers.csv`).
2. Fill the input columns (question, notes). Leave answer empty: the AI fills it.
3. Open **Settings**: sheet URL and how many rows to process per run.
4. Connect Google Sheets and OpenAI on the nodes with warnings.
5. Run once by hand, check the results, then switch to **Active**. It only touches rows where answer is empty.

## Google Sheet columns (row 1)

`question`, `notes`, `answer`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
