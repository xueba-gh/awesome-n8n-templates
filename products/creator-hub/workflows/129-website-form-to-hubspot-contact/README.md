# Website form to HubSpot contact with welcome email and owner alert

Each website enquiry creates or updates a HubSpot contact, sends the lead a thank-you email and alerts you with the details.

## What you need

- Gmail
- HubSpot (private app token)

## Setup

1. Create a HubSpot **private app** (Settings > Integrations > Private apps) with contacts read/write scope, and paste its token into a HubSpot App Token credential in n8n.
2. Open **Settings**: business name, your name and email.
3. Connect Gmail on the two email nodes. Send your form's POST to the **Webhook** URL.
4. Submit a test entry, check the record, then switch to **Active**.

## About this template

Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.

Need help installing or customising it? Message me via my n8n Creator profile.
