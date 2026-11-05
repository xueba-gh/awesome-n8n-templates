# Buyer finder: setup

An hourly n8n workflow that finds people asking for paid automation help and emails you one digest. **It never posts, comments or sends messages.** You read each post, check that community's rules, and reply by hand.

## What it does each hour

1. Reads the newest 50 posts from each subreddit in Settings (default: r/n8n, r/automation, r/smallbusiness, r/forhire, r/Entrepreneur) through the official Reddit node and your own Reddit app.
2. Reads the n8n community **Jobs** category (public JSON, one request, User-Agent `n8n-buyer-finder/1.0`).
3. Keeps posts from the last 24 hours that:
   - show buying intent ("looking for", "hire", "need someone", "budget", "will pay"...), and
   - are about automation (n8n, Zapier, Make, workflow, CRM, chatbot, AI agent, Gmail, Sheets...). Posts in r/n8n, r/automation and the n8n Jobs category count as on-topic automatically.
   - r/forhire: only `[Hiring]` posts. Posts with "for hire", "I will build", "unpaid" or "equity only" are dropped.
4. Skips anything already in the **Seen** sheet. At most 25 posts are scored per run, to keep AI costs low.
5. AI scores each post's fit from 1 to 10 and drafts a short, honest reply based on `about_me`. The reply gives one useful tip first, says you're new if experience comes up, and claims no past clients.
6. Saves every scored post to the **Seen** sheet. It emails you once with the posts that scored **7 or more**. If none qualify, no email is sent.

## Setup (about 15 minutes)

1. **Sheet:** make a Google Sheet with a tab named `Seen` and paste the headers from `seen-sheet-headers.csv` into row 1.
2. **Reddit app** (free, needed by Reddit's API rules):
   1. Signed in to Reddit, open https://www.reddit.com/prefs/apps and choose **create another app**.
   2. Type **web app**. Name `n8n buyer finder`. For the redirect URI, paste the OAuth Redirect URL that n8n shows in the next step.
   3. In n8n: **Credentials > Add credential > Reddit OAuth2 API**. Paste the client ID and secret yourself, then click **Connect**.
   4. Open the **Get new Reddit posts** node and select that credential.
3. **Import** `buyer-finder.workflow.json` (n8n: ... > Import from File or URL).
4. **Settings** node: set `digest_email`, `sheet_url`, your subreddits and keywords. Rewrite `about_me` so it is true for you. The AI uses only what is written there.
5. Connect **Google Sheets**, **Gmail** and **OpenAI**. Open each node with a warning once, so the credential attaches.
6. Click **Execute workflow** once. Check the Seen sheet and your inbox, then switch the workflow to **Active**.

## Rules this workflow follows, and rules for you

- Uses Reddit's official API with your own app credential, at about 5 requests an hour, far under the free limit. No scraping.
- Makes 1 request an hour to the n8n forum, with a User-Agent that names the tool. Your email is not sent anywhere.
- Never auto-replies. Each subreddit has its own rules about self-promotion, so read them before you reply. Many forbid promotional DMs.
- Use the drafts as a starting point only. Answer the person's problem first and say honestly that you're new. Never claim clients or results you don't have.

## Tuning

| Setting | Default | Change it when |
|---|---|---|
| `min_fit_score` | 7 | The digest is too noisy (raise it) or always empty (lower it) |
| `max_age_hours` | 24 | You check less often than daily |
| `max_posts_scored_per_run` | 25 | AI costs matter more, or you add many subreddits |
| `intent_keywords` / `topic_keywords` / `exclude_keywords` | see Settings | Good posts are missed, or junk gets through |

To mark a post you replied to, set its `status` cell in the sheet to `replied`. The workflow only adds rows. It never changes rows that already exist.

## Tested

- `node test/run-tests.js` checks the Code-node logic with sample data:
  - the intent and topic filter, the r/forhire rules, the 24-hour window and the duplicate skip
  - empty sources and a failed request
  - score clamping, and blank drafts for low scores
  - the digest only lists posts scoring 7+, and no email is sent when none qualify
- The live run in n8n is logged in `products/selling/LAUNCH-LOG.md`.
