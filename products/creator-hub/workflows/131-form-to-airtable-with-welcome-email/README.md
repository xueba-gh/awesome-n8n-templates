# Form submissions to Airtable with welcome email and owner alert

A hosted form saves every submission as an Airtable record, emails the person a welcome message and alerts you.

## What you need

- Gmail
- Airtable (personal access token)

## Setup

1. In Airtable, make a table with fields named exactly: received_at, name, email, phone, message. Create a personal access token (data.records:write, schema.bases:read) and add it as an Airtable credential.
2. Open **Settings**: business name, your name and email, Airtable base and table URLs.
3. Connect Gmail on the two email nodes. Share the form URL from the **Form** node.
4. Submit a test entry, check the record, then switch to **Active**.

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
