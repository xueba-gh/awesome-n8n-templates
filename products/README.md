# Products: n8n automations built to sell

Three original, tested n8n workflows aimed at the automations businesses pay for most often, plus an error-alert helper and a selling playbook. Unlike the rest of this repository (community templates collected from the internet), everything in `products/` was written from scratch for this repo, so it can be sold.

| # | Product | What it does | Setup guide |
|---|---|---|---|
| 01 | **Speed-to-Lead** | Replies to every new lead within a minute by text/WhatsApp and email, scores it with AI, logs it to Google Sheets, alerts the owner about hot leads, follows up after 24h and 72h, stops when the lead books or replies. | [SETUP](01-speed-to-lead/SETUP.md) |
| 02 | **AI Support Chatbot** | Website chat bubble (+ optional WhatsApp) that answers from the business's FAQ sheet, remembers the conversation and hands over to a human. | [SETUP](02-ai-support-chatbot/SETUP.md) |
| 03 | **AI Inbox Assistant** | Labels and summarises every Gmail email, drafts replies for approval, alerts on sales leads and urgent mail, logs everything. | [SETUP](03-ai-inbox-assistant/SETUP.md) |
| – | **Error alert** | Emails you when any of the above fails, with a link to the failed run. | [workflow](shared/error-alert.workflow.json) |

**How to sell them:** see [selling/SELLING-PLAYBOOK.md](selling/SELLING-PLAYBOOK.md) (prices, platforms, listing copy, outreach scripts, and a 30-day test to see whether the money comes).

## How they were tested
Each workflow was imported into n8n 2.42.5 and run end to end with test data:
- Google Sheets, Gmail, Twilio and WhatsApp steps were replaced by stand-ins that record exactly what would have been sent.
- The OpenAI model was pointed at a local mock.
- Every route was exercised:

| Product | Routes tested |
|---|---|
| Speed-to-Lead | New lead (webhook and built-in form); duplicate lead; lead without contact details; Cal.com and Calendly bookings; text reply; STOP; hourly follow-ups (due, not due, booked, maxed out) |
| Support Chatbot | Website chat with memory across messages; WhatsApp text; WhatsApp voice note; read receipts ignored; handover tool calls |
| Inbox Assistant | Sales lead (draft + alert); newsletter (new label created, no draft); no-reply sender (no draft); its own alert emails skipped |

The untouched workflow files also open in the n8n editor with **no warnings** once credentials are attached.

What was **not** tested here: real Google, Gmail, Twilio, WhatsApp and OpenAI accounts. Do one live run with your own accounts (each SETUP guide has a "Test it" section) before selling or installing for a client.
