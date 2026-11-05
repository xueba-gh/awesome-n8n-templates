# Airtable table to Google Sheets sync (hourly)

Copies every record of an Airtable table into a Google Sheet each hour, adding new records and updating changed ones.

## What you need

- Google Sheets
- Airtable (personal access token)

## Setup

1. Make a Google Sheet tab **Airtable copy** with headers `airtable_id`, `synced_at` and then your Airtable field names, spelt exactly the same.
2. Open **Settings**: Airtable base and table URLs, sheet URL.
3. Add an Airtable personal access token credential (data.records:read) and connect Google Sheets.
4. Run once: every record appears in the sheet, then each hour new records are added and changed ones updated (matched on airtable_id).

## Google Sheet columns (row 1)

`airtable_id`, `synced_at`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
