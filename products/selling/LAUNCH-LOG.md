# Launch log

Running checklist for the n8n products launch. Updated at the end of each task.

## Status

| # | Task | Status |
|---|---|---|
| 1 | Live test with real accounts | In progress |
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
| 01 Speed-to-Lead | [x] (via raw GitHub URL) | [ ] Google Sheets/Gmail pending | [ ] | Leads sheet created: 'Speed-to-Lead test leads', tab Leads, 14 headers |
| 02 AI Support Chatbot | [ ] | [ ] | [ ] | |
| 03 AI Inbox Assistant | [ ] | [ ] | [ ] | |
| shared/error-alert | [ ] | [ ] | [ ] | |

### Only checked with mocks so far (verify live)

- [ ] Real OpenAI structured output in the AI nodes
- [ ] Chatbot handover tools `save_contact_request` and `notify_owner` (do `$fromAI` values fill in?)
- [ ] Gmail labels via `={{ [$json.label_id] }}`
- [ ] Google Sheets append/update with auto-mapped columns

### Fixes made to workflow JSONs

_None yet._

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

Connect Google Sheets and Gmail credentials in n8n, fill the Settings node, send a test lead (email-only).
