# Speed-to-Lead Lite: instant AI email reply, lead score and Google Sheets log

Reply to every website lead within a minute with a personal AI-written email, score the lead, log it to Google Sheets and get an alert for hot leads.

**Free template.** Want it installed for you? I set up the full version on your own accounts. Message me through my n8n Creator profile.

## What it does
- Catches leads from your website form (webhook) or a built-in n8n form
- Cleans up names, emails and phone numbers from any form tool
- AI scores the lead 1 to 10 and writes a short personal email with your booking link
- Sends the email, saves the lead to Google Sheets, and emails you when the score is 8 or higher

## What you need
n8n, an OpenAI API key, a Google account (Sheets and Gmail).

## Setup
1. Make a Google Sheet with a tab `Leads` and these headers in row 1: received_at, lead_id, name, email, phone, source, message, score, temperature, summary, status, notes
2. Open **Settings**: business details, booking link, your email, sheet URL.
3. Connect credentials: OpenAI, Google Sheets, Gmail (open each node once so the credential attaches).
4. Point your website form at the **New lead (webhook)** URL, or share the built-in form's URL.
5. Activate.

## Full version
- Text or WhatsApp reply via Twilio
- Automatic follow-ups after 24 and 72 hours
- Stops when the lead books (Cal.com / Calendly) or texts back
- Duplicate-lead check and text alerts to your phone

Want it installed for you? I set up the full version on your own accounts. Message me through my n8n Creator profile.
