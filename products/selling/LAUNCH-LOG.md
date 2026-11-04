# Launch log

Running checklist for the n8n products launch. Updated at the end of each task.

## Status

| # | Task | Status |
|---|---|---|
| 1 | Live test with real accounts | Done (optional extras: Speed-to-Lead Booked/Replied/duplicate paths, Twilio, WhatsApp) |
| 2 | Demo videos | Not started |
| 3 | Upwork profile | Not started |
| 4 | Fiverr gigs | Not started |
| 5 | n8n Creator Hub (free versions, affiliate) | Not started |
| 6 | Buyer finder workflow | Not started |
| 7 | Daily routine sheet + niche + first 50 businesses | Not started |
| 8 | Repo privacy | Not started |

## Task 1: live test

- n8n hosting: n8n Cloud trial, instance kwamena.app.n8n.cloud (14-day trial, started 2026-11-04)
- Accounts: n8n Cloud [x] · n8n Creator Hub [x] · Anthropic credential in n8n [x] (tested OK) · Google [x] signed in · Twilio [ ] (optional; email-only first if no A2P 10DLC)
- AI models: the trial includes $2 of n8n 'Gateway credits' that the OpenAI model nodes can use as shipped, so the live test runs the real OpenAI nodes with no swap. Anthropic credential is kept for later.
- Private repo for paid files: github.com/xueba-gh/n8n

### Per product

| Product | Imported | Credentials | Test run | Notes |
|---|---|---|---|---|
| 01 Speed-to-Lead | [x] (via raw GitHub URL) | [x] Sheets, Gmail (email-only; no Twilio yet) | [x] new-lead path and hourly follow-up #1 (backdated received_at: follow-up email sent, followups_sent=1, last_contact_at updated), 2026-11-04. Booking, replied/STOP and duplicate path not yet tested live | Leads sheet created: 'Speed-to-Lead test leads', tab Leads, 14 headers |
| 02 AI Support Chatbot | [x] (raw GitHub URL) | [x] Sheets (2 nodes), Gmail, OpenAI (gateway credits) | [x] 2026-11-04, website chat in n8n test panel | FAQ answer from sheet OK; off-sheet question ('Invisalign') -> says unsure and offers a human; callback request -> row in Conversations (name, contact, reason, summary, status=new) and owner email node ran. WhatsApp not tested (needs Meta setup). Test sheet 'Support Chatbot test sheet', tabs Knowledge + Conversations |
| 03 AI Inbox Assistant | [x] | [x] Gmail, Sheets, OpenAI (gateway credits) | [x] 2026-11-04 | Newsletter path (label AI/Newsletter created, no draft, logged) and sales-lead path (AI/Sales lead label, draft saved in thread, '[Inbox Assistant] New lead' alert, logged). Test sheet 'Inbox Assistant test log', tab 'Inbox log'. Credentials attach only when each node is opened once; first run fails with 'Node does not have any credentials set' until then. |
| shared/error-alert | [x] | [x] Gmail | [x] 2026-11-04, run with n8n sample error data: alert email sent | Not yet triggered by a real failing workflow (set as Error workflow in client workflows to verify end to end) |

### Only checked with mocks so far (verify live)

- [x] Real OpenAI structured output in the AI nodes (Speed-to-Lead scoring chain, via n8n gateway credits: score 10, hot, valid JSON). Follow-up chain and the other two products still to check
- [x] Chatbot handover tools `save_contact_request` and `notify_owner`: `$fromAI` values (name, contact, reason, summary) filled in correctly, row appended and email node succeeded
- [x] Gmail labels via `={{ [$json.label_id] }}` (label created and applied on both test emails)
- [x] Google Sheets append/update with auto-mapped columns

### SETUP.md troubleshooting to add

- Sheets 404 'Requested entity was not found' -> reconnect the Google credential (Switch account) with the account that owns the sheet
- 'Node does not have any credentials set' on first run -> open each node once so the credential attaches
- n8n Cloud session can expire; sign in again if the editor shows 'Unauthorized'

## Fixes made to workflow JSONs

None to the workflow JSONs so far.

Observation: the first test run failed at 'Already in the sheet?' with Google 404 'Requested entity was not found'. It ran fine after the Google Sheets credential was disconnected and reconnected (Switch account). Likely a stale or wrong-account authorisation from the first pop-up. Worth adding to the SETUP.md troubleshooting table: 'Sheets 404 -> reconnect the Google credential with the account that owns the sheet'.

Live test result (2026-11-04): test lead via webhook produced a Leads row (score 10, hot, status contacted), a reply email to the lead, and a hot-lead alert email to the owner. Connected Google account is a different address from the personal one, so mails arrived as sent from it.

## Demo videos (unlisted links)

- Speed-to-Lead: _
- AI Support Chatbot: _
- AI Inbox Assistant: _

## Links

- Upwork profile: _
- Fiverr gigs: _
- n8n Creator Hub templates: _
- Tracker sheet: _

## Next

Remaining: shared/error-alert test. Optional: Speed-to-Lead Booked/Replied/duplicate paths. (Done: follow-up path)

Old note: Test the follow-up path (set a row's last_contact_at back by 25h and run the hourly trigger), the Booked and Replied webhooks, and the duplicate check. Then import and test the AI Inbox Assistant (labels expression), then the Support Chatbot (handover tools), then shared/error-alert.
