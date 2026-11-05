# CSV upload cleaner to Google Sheets

Upload a CSV through a form: headers are normalised, emails checked, names tidied, duplicates and incomplete rows dropped, and the rest appended to your sheet.

## What you need

- Google Sheets

## Setup

1. Make a sheet tab **Imported** whose headers match your CSV columns in lower_snake_case (for example `First Name` becomes `first_name`).
2. Open **Settings**: sheet URL and the columns a row must have to be kept.
3. Connect Google Sheets. Open the form URL from **CSV upload form** and upload a test file.
4. Cleans: trims spaces, lower-cases emails and drops invalid ones, title-cases names, strips phone formatting, removes exact duplicates and rows missing required columns.

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
