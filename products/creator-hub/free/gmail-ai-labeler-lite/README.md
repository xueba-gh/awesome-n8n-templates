# Gmail AI Labeler Lite: auto-label, summarise and log every new email

Auto-label every new Gmail email with AI, summarise it in one line and log it to Google Sheets.

**Free template.** Want it installed for you? I set up the full version on your own accounts. Message me through my n8n Creator profile.

## What it does
- Reads each new email (Gmail trigger)
- AI picks a category (sales lead, support, billing, scheduling, newsletter, notification, spam...), urgency and whether it needs a reply
- Applies a Gmail label like AI/Sales lead, creating it the first time
- Logs sender, subject, category, urgency and summary to a Google Sheet
- Never sends or deletes email

## What you need
n8n, an OpenAI API key, a Google account (Gmail and Sheets).

## Setup
1. Make a Google Sheet with a tab `Inbox log` and these headers: processed_at, from, subject, category, urgency, needs_reply, summary, message_id
2. Open **Settings**: your name and business, sheet URL.
3. Connect credentials: Gmail, OpenAI, Google Sheets.
4. Activate. Labels are created automatically the first time they're needed.

## Full version
- Reply drafts saved in Gmail for you to approve
- Instant alerts for sales leads and urgent emails

Want it installed for you? I set up the full version on your own accounts. Message me through my n8n Creator profile.
