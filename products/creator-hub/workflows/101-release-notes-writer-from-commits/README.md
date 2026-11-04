# Release notes writer from commit messages

Paste commit messages or ticket titles into a sheet row. AI turns them into friendly, customer-facing release notes.

## What you need

- Google Sheets
- OpenAI API key

## Setup

1. Use a Google Sheet with a tab named **Releases** and these headers in row 1 (see `sheet-headers.csv`).
2. Fill the input columns (raw_changes). Leave release_notes empty: the AI fills it.
3. Open **Settings**: sheet URL and how many rows to process per run.
4. Connect Google Sheets and OpenAI on the nodes with warnings.
5. Run once by hand, check the results, then switch to **Active**. It only touches rows where release_notes is empty.

## Google Sheet columns (row 1)

`version`, `raw_changes`, `release_notes`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
