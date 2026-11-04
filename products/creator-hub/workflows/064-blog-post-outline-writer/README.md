# Blog post outline writer from topic ideas in a sheet

Add topic ideas to a sheet and get an SEO-minded outline for each: title options, headings and key points.

## What you need

- Google Sheets
- OpenAI API key

## Setup

1. Use a Google Sheet with a tab named **Blog ideas** and these headers in row 1 (see `sheet-headers.csv`).
2. Fill the input columns (topic). Leave title_options, outline empty: the AI fills it.
3. Open **Settings**: sheet URL and how many rows to process per run.
4. Connect Google Sheets and OpenAI on the nodes with warnings.
5. Run once by hand, check the results, then switch to **Active**. It only touches rows where title_options is empty.

## Google Sheet columns (row 1)

`topic`, `audience`, `title_options`, `outline`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
