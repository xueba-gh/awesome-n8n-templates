# Emails that ask you to do something become Notion tasks (AI)

AI reads each new email; when it asks you to do something, a task with a due date and context is created in your Notion database.

## What you need

- Gmail
- OpenAI API key
- Notion (internal integration shared with the database)

## Setup

1. In Notion, create a database (a table) and an internal integration at notion.so/my-integrations. Share the database with the integration (... > Connections).
2. Add a Notion credential in n8n with the integration secret (you paste it). Open **Settings** and paste the database URL.
3. Connect Gmail and OpenAI. Only emails that really ask you to do something become tasks.
4. Test once, check the new page in Notion, then switch to **Active**.

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
