# Launch log

Running checklist for the n8n products launch. Updated at the end of each task.

## Status

| # | Task | Status |
|---|---|---|
| 1 | Live test with real accounts | Done (optional extras: Speed-to-Lead Booked/Replied/duplicate paths, Twilio, WhatsApp) |
| 2 | Demo videos | In progress: shot scripts written (selling/DEMO-VIDEO-SCRIPTS.md); fake-data demo CSVs for all three products in selling/demo-data/; Google demo sheets and recordings next |
| 3 | Upwork profile | Not started |
| 4 | Fiverr gigs | Not started |
| 5 | n8n Creator Hub (free versions, affiliate) | Free Lite versions built (creator-hub/free/); submission waits on the Terms checkbox (user); affiliate application not started |
| 6 | Buyer finder workflow | Done: built, logic-tested, live run 2026-11-05 (n8n forum branch end to end; Reddit needs the user's Reddit app credential) |
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

## Creator Hub bulk templates (100+ plan)

- Demand research done; 130 ideas ranked in `products/creator-hub/IDEAS.md`.
- User said: build all products without asking questions. 115 workflows generated by `products/creator-hub/build.py` (specs in `specs/`) into `products/creator-hub/workflows/NNN-slug/` (workflow.json, README.md, sheet-headers.csv); catalog in `CATALOG.csv`. Static checks pass (JSON, connections, no credentials, JS syntax, template fields exist). Live-tested in n8n Cloud (import from raw GitHub URL, real run, 2026-11-04): intake (001 lead form: webhook -> sheet -> thank-you email -> owner alert), Gmail+AI (016 support triage: AI, combine, sheet log, alert/draft branches), row enrichment (071 product descriptions written back to correct rows), monitor (091 uptime: 404 routed to alert email). Scheduled-reminder and digest archetypes: JS logic simulated in Node with sample rows (filter picks the right rows); not yet run live. Slack nodes and Stripe/Shopify/Calendly payload shapes not tested live.

## Creator Hub batch 2 (2026-11-05): 24 more workflows, 139 total

- New apps: RSS (6), Telegram (4), Twilio SMS incl. missed-call text-back (3), HubSpot (2), Airtable (2), Notion (2), Google Drive (2), utilities: error alert, sheet duplicate finder, CSV upload cleaner (3). Specs in `creator-hub/specs/s10_integrations.py`; folders 116-139.
- Checks: build.py (0 errors), node-reference/orphan check on all 139, `node creator-hub/test/batch2-logic.js` (Code-node logic for 10 of them passes).
- n8n Cloud import of all 24 together: every node type recognised; HubSpot, Airtable, Notion, Telegram, Twilio and Drive parameter panels open with the intended fields (only missing credentials flagged).
- Live run: 120 industry news digest with two real feeds (n8n blog, hnrss automation): 35 items read, AI digest written, email sent.
- Not live-tested (need accounts the user doesn't have yet): Telegram, Twilio, HubSpot, Airtable, Notion.

## Task 5: free Creator Hub versions (2026-11-05)

Built by `products/creator-hub/free/build_free.py` from the tested paid JSONs (kept nodes are unchanged, the rest removed and rewired):
- `speed-to-lead-lite`: webhook/form -> clean -> AI score + email reply -> sheet -> hot-lead email. Full version adds SMS/WhatsApp, 24h/72h follow-ups, booking/reply stop, duplicate check.
- `faq-chatbot-lite`: website chat -> FAQ sheet -> AI with memory. Full version adds WhatsApp, hand-over (contact capture, log, owner email), embed snippet.
- `gmail-ai-labeler-lite`: Gmail -> AI category/urgency/summary -> label (auto-created) -> sheet log. Full version adds reply drafts and alerts.
Each has a 'Full version adds' sticky note. The setup-service line says "message me through my n8n Creator profile" until `SETUP_URL` is set to the Fiverr/Upwork link (then rebuild).
Static checks pass (connections, node references, no credentials, JS syntax). Not yet live-run.
Creator Hub submit form: JSON file upload + pricing + a Terms checkbox. Uploading works by script; the Terms box is for the user to tick.

## Task 6: buyer finder (2026-11-05)

- `products/buyer-finder/`: workflow, SETUP.md, `seen-sheet-headers.csv`, builder, `test/run-tests.js` (logic tests pass).
- Sources: official Reddit node (user's own Reddit OAuth app, 5 requests/hour) and n8n community Jobs JSON (`/c/jobs/13.json`, 1 request/hour, User-Agent `n8n-buyer-finder/1.0`, no email). Never posts or messages.
- Live run in n8n Cloud: forum fetch OK (30 topics), AI scored 5 posts (10, 10 for real n8n hiring posts; 3 for a full-time role and a volunteer post), 5 rows saved to sheet 'Buyer finder test' tab Seen, digest email sent with 2 posts and honest drafts ("I'm new to freelancing..."). Reddit branch failed safely without a credential.
- Bug found and fixed in the live run: n8n Jobs topics are all marked closed (replies go by DM), so the closed filter dropped everything; closed topics are now kept.
- User to do: create a Reddit app and add the Reddit OAuth2 credential; set the workflow Active.

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
