# Demo video scripts (60 to 90 seconds each)

Record with Loom (free, easiest) or OBS. 1080p, browser zoom 110%, close other tabs, hide your bookmarks bar. Use the demo business and fake data below, never real customer data. Upload as **unlisted** (Loom link or YouTube unlisted) and paste links into `LAUNCH-LOG.md`.

Honesty rules for every video: say it is a demo with test data, say you are new and building your first client installs, do not mention past clients or results.

Before recording: use a fresh test sheet with only the header row, keep the workflow open in n8n, and have your phone (or a second Gmail tab) ready to show the incoming email.

---

## 1. Speed-to-Lead (target 75 s)

Demo business: Acme Plumbing. Sheet: "Speed-to-Lead demo leads".

| Time | On screen | Say |
|---|---|---|
| 0:00 | Title card or the n8n canvas | "Most leads go to whoever replies first. This replies in under a minute, even at 11pm. Here is a demo with test data." |
| 0:10 | The empty Leads sheet and the Gmail inbox side by side | "Here is the lead sheet and the inbox. Both empty." |
| 0:18 | Submit a test lead (webhook / form): "Jo Martin, water heater leaking, can someone come Thursday?" | "A new enquiry comes in from the website form." |
| 0:28 | n8n execution lighting up node by node | "The AI scores it, writes a personal reply and checks it is not a duplicate." |
| 0:40 | Lead's inbox: reply email with booking link | "The customer gets a reply with the booking link, within seconds." |
| 0:52 | Owner inbox: hot-lead alert | "Hot leads alert the owner straight away." |
| 1:00 | Leads sheet: new row with score, temperature, status | "Everything is logged in a sheet: score, summary, status." |
| 1:08 | Row with follow-up count 1 | "If the lead goes quiet, it follows up politely after 24 and 72 hours, then stops." |
| 1:15 | End card | "I'm new, so I'm offering the first few installs at a discount. Link below." |

## 2. AI Support Chatbot (target 80 s)

Demo business: Acme Dental, assistant "Ava". Sheet: "Support Chatbot demo" (Knowledge + Conversations).

| Time | On screen | Say |
|---|---|---|
| 0:00 | Chat page (production chat URL) | "This chatbot answers customer questions from your own FAQ sheet. Demo with test data." |
| 0:10 | Knowledge sheet | "The business keeps its hours, prices and policies in a simple sheet. Edit it and the bot changes instantly." |
| 0:22 | Chat: "What are your opening hours?" | "It answers from the sheet." |
| 0:35 | Chat: "Do you offer Invisalign?" (not in sheet) | "If it is not in the sheet it does not guess. It offers a person." |
| 0:48 | Chat: "Yes, I'm Sam, 555 123 4567" | "It collects the contact details." |
| 0:58 | Conversations sheet: new row | "The request is saved to the sheet..." |
| 1:05 | Owner inbox: notification email | "...and the owner gets an email." |
| 1:12 | End card | "Works on your website, and WhatsApp can be added. Link below." |

## 3. AI Inbox Assistant (target 80 s)

Demo business: a small consultancy. Sheet: "Inbox Assistant demo log".

| Time | On screen | Say |
|---|---|---|
| 0:00 | Gmail inbox | "This reads every new email, labels it, summarises it, and drafts replies. It never sends anything itself. Demo with test emails." |
| 0:12 | Send two test emails from a second account: a newsletter and "How much to replace a water heater this week?" | "Two emails arrive: a newsletter and a customer asking for a price." |
| 0:25 | n8n execution | "The AI reads each one." |
| 0:35 | Inbox with labels AI/Newsletter and AI/Sales lead | "They are labelled automatically." |
| 0:45 | Open the sales email, then Drafts: reply draft in the thread | "The customer email gets a reply draft, ready for you to check and send." |
| 0:58 | Alert email "[Inbox Assistant] New lead" | "Sales leads trigger an alert so you reply fast." |
| 1:05 | Log sheet | "Every email is logged." |
| 1:12 | End card | "I'm new, so early installs are discounted. Link below." |

---

## Recording checklist
- [ ] Demo sheets created with fake data only (names like Jo Martin, Sam Carter; phone 555 numbers)
- [ ] Credentials and account emails not visible (close n8n credential pages)
- [ ] Each video 60 to 90 seconds, unlisted upload
- [ ] Link pasted in `LAUNCH-LOG.md`
