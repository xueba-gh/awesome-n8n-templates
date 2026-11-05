# Save Gmail attachments to Google Drive with a log sheet

Every attachment you receive (optionally only from chosen senders) is saved to a Drive folder with a clear name and logged in a sheet.

## What you need

- Google Sheets
- Gmail
- Google Drive

## Setup

1. Create a Drive folder and copy the ID from its URL (the part after /folders/) into **Settings**. Optional: `only_from` limits it to certain senders or `@domain.com`.
2. Make a sheet tab **Saved attachments** with the headers in `sheet-headers.csv` and put its URL in **Settings**.
3. Connect Gmail, Google Drive and Google Sheets.
4. Send yourself an email with an attachment, then switch to **Active**.

## Google Sheet columns (row 1)

`saved_at`, `from`, `subject`, `file_name`, `drive_link`

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
