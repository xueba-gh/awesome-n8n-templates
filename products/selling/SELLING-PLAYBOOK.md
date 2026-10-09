# Selling Playbook: three n8n products, five channels, one 30-day money test

This playbook covers the three products in `products/`:

| Product | What the buyer gets | Who buys it |
|---|---|---|
| **01 Speed-to-Lead** | Every new lead gets an AI-written text/WhatsApp and email within a minute, is scored, logged to a sheet, and followed up twice if they go quiet. Hot leads ping the owner straight away. | Local service businesses that pay for leads: home services, real estate, clinics, dentists, med spas, gyms, coaches, agencies |
| **02 AI Support Chatbot** | A chat bubble for their website (and optionally WhatsApp) that answers from their own FAQ sheet, collects contact details and hands over to a human. | Any business answering the same questions all day: clinics, restaurants, salons, e-commerce, property managers |
| **03 AI Inbox Assistant** | Gmail sorted and labelled automatically, reply drafts waiting for approval, urgent mail and sales leads flagged to the owner, a log sheet of everything. | Busy owners, consultants, agencies, small teams living in Gmail |

All three were written from scratch for this repo, so you own them and can sell them. (Do not sell the other templates in this repo: they belong to their original creators.)

---

## 1. The honest money picture

The money is in **installing and running these for businesses**, not in selling the JSON files. Selling the file alone earns $10 to $100 a copy; setting it up for a business earns $300 to $2,000, plus a monthly fee. So:

- **Templates** (Gumroad, Lemon Squeezy, the n8n Creator Hub) = visibility and small income. They make strangers trust you.
- **Done-for-you setups** (Upwork, Fiverr, direct outreach) = the real income.
- **Monthly care plans** = the income that compounds.

Price figures below come from public rate cards and marketplace listings seen in October 2026. They are starting points; adjust after your first 5 sales conversations.

---

## 2. Price list (start here, raise after 3 happy clients)

| Offer | Speed-to-Lead | Support Chatbot | Inbox Assistant |
|---|---|---|---|
| **Template only** (JSON + setup guide + sheet template) | $49 | $49 | $29 |
| **Template + 30-min setup call** | $149 | $149 | $99 |
| **Done-for-you install** (their accounts, their wording, tested, 14 days of fixes) | $497 to $997 | $497 to $1,500 | $297 to $497 |
| **Monthly care plan** (hosting/monitoring, prompt tweaks, fixes, monthly report) | $149 to $300/mo | $149 to $300/mo | $49 to $99/mo |
| **Bundle**: all three installed | $1,500 to $2,500 + $300/mo | | |

Running costs the client pays (tell them upfront): n8n Cloud from about $24/month or a $5 to $10/month server; OpenAI usage, typically a few dollars a month at small-business volume; Twilio about $1/month per number plus a cent or so per text.

Always set up accounts **in the client's name** (n8n, OpenAI, Google, Twilio) and give yourself access. They own their data, you avoid paying their bills, and the care plan is what keeps you involved. For US clients texting leads, budget a few days for Twilio's A2P 10DLC registration (see the Speed-to-Lead SETUP guide).

---

## 3. The channels, ranked by how fast money can come

### Channel A: Direct outreach to local businesses (fastest real money)
**Why first:** no platform fees, no competing with 500 freelancers, and the pitch ("you're losing leads you answer late") is easy to understand.

1. Pick **one niche** for 30 days. Good first picks: roofers/HVAC/plumbers, dentists, med spas, real estate agents.
2. Build a list of 100 businesses in that niche (Google Maps: "dentist near [city]"). Note those with a website contact form and paid ads (they are paying for leads).
3. **Mystery-shop 20 of them**: fill in their contact form, note how long they take to reply. This becomes your pitch: "I filled in your form on Tuesday at 2pm. You replied Thursday. Here is a 90-second video of what would have happened with my system."
4. Send the outreach script (section 6), follow up twice, offer a 15-minute demo.
5. Close at the done-for-you price + care plan. Offer the first 2 clients 50% off in exchange for a testimonial and a case study.

### Channel B: Upwork (real buyers already searching)
Live postings in Sept/Oct 2026 included "AI Lead Qualification Workflow" ($800 fixed), RAG chatbots, and WhatsApp/email automation.

- **Cost:** free account with 10 Connects/month; extra Connects $0.15 each; jobs typically need 2 to 16 Connects to apply. Service fee 0 to 15% per contract.
- **Profile title:** `n8n Automation Expert | AI Lead Follow-up, Chatbots & Gmail Automation`
- **Portfolio:** add all three products with a screenshot of the workflow and the 90-second demo video.
- **Daily routine:** search `n8n`, filter to "posted in last 24 hours" and "payment verified", apply to 3 to 5 jobs with the proposal template (section 6). Apply within the first hour of posting where possible; early proposals get read.
- **Project Catalog:** list each product as a fixed-price project (use the "Done-for-you install" prices).

### Channel C: Fiverr (buyers come to you, slower start)
Observed n8n gigs: roughly $80 to $350 per workflow for new sellers, with 2 to 5 day delivery and 14-day bug-fix guarantees common.

- Create **3 gigs**, one per product, each with 3 packages: Basic = template installed on their n8n; Standard = customised wording + their tools; Premium = Standard + 30-day care.
- Gig titles (lead with the result, not the tool):
  - `I will build an AI speed to lead system that texts and emails every new lead in 60 seconds`
  - `I will build an AI website chatbot trained on your FAQ using n8n`
  - `I will automate your Gmail inbox with AI labels, reply drafts and alerts`
- Start below market (about $150 Basic) for the first 5 reviews, then raise prices.

### Channel D: n8n Creator Hub (credibility + free traffic)
- Templates on n8n.io rank well on Google and are where n8n users look first.
- Community reports say you need to publish **about 3 approved free templates** before you can sell paid ones, and reviewers reject simple workflows. Paid templates seen there sell for around $20.
- Plan: publish **cut-down free versions** (for example Speed-to-Lead without the follow-up engine, Inbox Assistant without the log sheet), with a link in the description to the full version and your setup service.
- Also join the **n8n affiliate programme** (30% of n8n Cloud subscriptions for the first year) and use your link when clients sign up for n8n Cloud.

### Channel E: Gumroad or Lemon Squeezy (sell the full template)
- **Lemon Squeezy:** about 5% + $0.50 per sale, handles sales tax. Cheaper.
- **Gumroad:** about 10% + $0.50 per sale (plus card processing); 30% if the buyer found you via Gumroad's own marketplace. Simpler to start.
- Product = ZIP with the workflow JSON, SETUP.md (exported as PDF), the sheet templates and a short video. Add an "Upgrade: I'll install it for you" option at the setup-call price.
- Drive traffic from: the Creator Hub free versions, YouTube/LinkedIn demo videos, Reddit (r/n8n, r/automation: share the free version, not ads).

### Skip for now
Third-party "n8n marketplaces" (n8nmarket, n8nplace, managen8n and similar): community members report several are quiet or inactive. List there only after the channels above are running.

---

## 4. Ready-to-paste listing copy

### Speed-to-Lead
**Headline:** Reply to every lead in 60 seconds, even at 11pm.
**Description:**
> Most leads buy from whoever answers first. This system answers for you.
> When someone fills in your website form (or any form, ad or landing page), it:
> - scores the lead with AI (hot / warm / cold) and writes a personal reply,
> - texts or WhatsApps them, and emails them your booking link, within a minute,
> - logs everything in a Google Sheet you can see from your phone,
> - pings you instantly when a hot lead comes in,
> - follows up automatically after 1 day and again after 3 days if they go quiet,
> - stops following up the moment they book (works with Cal.com).
> Built on n8n, with error alerts and duplicate protection. Setup guide included.

### AI Support Chatbot
**Headline:** A website assistant that knows your business and never sleeps.
**Description:**
> Paste one snippet into your website and get a chat assistant that:
> - answers questions from your own FAQ sheet (hours, prices, services, policies), so you control what it says,
> - never invents prices or promises: if it does not know, it offers to get a human,
> - collects the visitor's name and contact details and saves them to your sheet,
> - emails you when someone wants a callback,
> - optional: the same assistant on WhatsApp.
> Update the answers any time by editing a Google Sheet; no code.

### AI Inbox Assistant
**Headline:** Open Gmail to a sorted inbox and replies already drafted.
**Description:**
> Every new email is read by AI and:
> - labelled (Sales lead, Customer support, Billing, Newsletter, Personal, Other),
> - given a one-line summary and an urgency level,
> - answered with a draft reply in your tone, waiting in Drafts for you to check and send (it never sends on its own),
> - flagged to you instantly when it is urgent or a new sales lead,
> - logged to a Google Sheet so nothing slips through.

---

## 5. Demo assets to make once (reuse everywhere)

1. **90-second screen recording per product** (Loom or OBS): trigger it (fill in the form / send an email / open the chat), show the text arriving on your phone and the row appearing in the sheet.
2. **Screenshot of each workflow** in the n8n editor (zoom to fit, hide credentials).
3. **One-page PDF per product**: problem, what it does, price, what the client needs (accounts), timeline.
4. **A demo sheet** with fake leads so prospects see the end result.

---

## 6. Scripts

### Cold email / DM (direct outreach)
> Subject: your contact form on [website]
>
> Hi [name], I filled in the contact form on [website] on [day] at [time] as a test. The first reply came [X hours/days] later.
>
> People who fill in a form usually contact two or three businesses and go with whoever answers first. I set up a small system for [niche] businesses that texts and emails every new enquiry within a minute, with your booking link, and alerts you when it's a hot one. It runs on your existing website and Gmail.
>
> Here is a 90-second video of it working: [link]
>
> Worth a 15-minute call this week? If it doesn't fit, no worries.
>
> [Your name]

Follow up after 3 days ("Did you get a chance to look at the video?") and after 7 days ("Last note from me: happy to set it up on a trial for your next 20 leads.").

### Upwork proposal
> Hi [client name], I've built exactly this: an n8n workflow that [restate their need in one line, e.g. "qualifies inbound leads with AI and routes them to your CRM with an instant follow-up"].
>
> Here's a short video of my version running: [link]
>
> For your setup I would:
> 1. [step tied to their tools, e.g. connect your Typeform + HubSpot]
> 2. [customise the AI scoring to your criteria]
> 3. Add error alerts and duplicate protection so it doesn't fail silently.
>
> I can deliver in [3 to 5] days, including 14 days of fixes. One question: [one smart question about their process].

### Discovery call checklist (15 minutes)
- Where do leads/emails/questions come from today? How many a week?
- Who answers them, and how fast?
- What does one new customer earn them? (Use this to justify the price: "if this wins you one extra job a month it pays for itself.")
- Which tools do they already use (forms, CRM, calendar, Gmail/Outlook, WhatsApp)?
- Who will own the accounts (n8n, OpenAI, Twilio)? Always the client.

---

## 7. The 30-day money test (so you know if the money will come)

Track these numbers in a sheet every day. Decide on day 30 using the rules at the bottom.

| Week | Do | Target |
|---|---|---|
| 1 | Import and test all three products on your own accounts. Record the 3 demo videos. Set up Upwork profile + 3 Fiverr gigs. Publish free version #1 on the Creator Hub. | All assets live |
| 2 | Contact 50 businesses in your niche (mystery-shop 20 first). Apply to 15 Upwork jobs. List the full templates on Lemon Squeezy/Gumroad. | 5 replies, 2 calls |
| 3 | Contact 50 more. Apply to 15 more Upwork jobs. Publish free versions #2 and #3. Post one demo on LinkedIn/Reddit. | 1 paid install (discount is fine) |
| 4 | Deliver, get a testimonial, turn it into a case study. Pitch the care plan. Contact 50 more. | 1 to 2 paid installs, 1 care plan |

**Metrics to track:** messages sent, replies, calls booked, proposals sent, deals won, revenue, care plans active, template sales, Creator Hub views.

**Decision rules on day 30:**
- **0 replies from 150 messages** → the message or niche is wrong. Change the niche or the opening line, not the product.
- **Replies but no calls** → your video/offer is unclear. Lead with their own mystery-shop result.
- **Calls but no sales** → price or trust. Offer a pay-after-results trial for the next 2.
- **1+ sale** → it works. Do more of whatever channel produced it, raise prices 20% after every 3 clients, and push every client onto a care plan.

A realistic first-month outcome for a newcomer is 1 to 3 paid setups ($500 to $2,500) and a few template sales. The care plans are what make month 6 much better than month 1.
