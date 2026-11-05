"""Builds buyer-finder.workflow.json.

Every hour: read new posts from chosen subreddits (official Reddit node, your own Reddit app
credential) and the n8n community Jobs category (public Discourse JSON, one request an hour,
custom User-Agent) -> keep posts from the last 24 hours that show buying intent -> skip posts
already in the 'Seen' sheet -> AI scores the fit 1-10 and drafts an honest reply -> every scored
post is saved to the sheet -> one digest email with the posts that scored 7 or more.
It NEVER posts, comments or messages anyone. You read the digest and reply by hand.

Run:  python3 build_buyer_finder.py
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "creator-hub"))
from lib import WF, n_settings, n_schedule, n_code, n_sheet, n_ai  # noqa: E402

CFG = {
    "subreddits": ["n8n", "automation", "smallbusiness", "forhire", "Entrepreneur"],
    "n8n_forum_jobs_url": "https://community.n8n.io/c/jobs/13.json",
    "user_agent": "n8n-buyer-finder/1.0 (personal hourly lead digest; replies are written by hand)",
    "max_age_hours": 24,
    "max_posts_scored_per_run": 25,
    "min_fit_score": 7,
    "intent_keywords": ["looking for", "hire", "hiring", "need someone", "need help", "need a", "freelancer",
                        "consultant", "developer", "expert", "paid", "budget", "will pay", "recommend",
                        "anyone who can", "can someone", "help me automate", "who can build", "quote"],
    "topic_keywords": ["n8n", "automation", "automate", "zapier", "make.com", "integromat", "workflow", "crm",
                       "chatbot", "chat bot", "ai agent", "ai assistant", "lead", "follow up", "follow-up",
                       "gmail", "inbox", "google sheets", "airtable", "webhook", "api", "whatsapp bot"],
    "exclude_keywords": ["[for hire]", "for hire", "[offer]", "i will build", "i'm offering", "my agency offers",
                         "hiring a full-time", "full time position", "unpaid", "equity only", "free of charge"],
    "topic_always_relevant": ["n8n", "automation", "n8n_forum"],
    "about_me": "I'm new to freelancing. I build n8n automations for small businesses: AI lead follow-up (instant reply, scoring, follow-ups), "
                "AI website chatbots that answer from the business's own FAQ sheet, and Gmail inbox assistants that label mail and draft replies. "
                "I have working demos of all three but no past clients yet.",
    "digest_email": "you@example.com",
    "sheet_url": "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit",
    "sheet_tab": "Seen",
}

COLS = ["post_id", "source", "title", "url", "author", "posted_at", "found_at", "fit_score", "why", "draft_reply", "status"]

LIST_SUBS = """// One item per subreddit, so the Reddit node makes one request each.
const cfg = $('Settings').first().json.config;
return (cfg.subreddits || []).map((s) => ({ json: { subreddit: String(s).replace(/^r\\//i, '').trim() } }));"""

FILTER = """// Normalise Reddit + n8n forum posts, keep recent ones with buying intent, drop ones already seen.
const cfg = $('Settings').first().json.config;
const lc = (s) => String(s || '').toLowerCase();
const has = (text, words) => (words || []).some((w) => text.includes(lc(w)));
const maxAgeMs = (Number(cfg.max_age_hours) || 24) * 3600 * 1000;
const now = Date.now();

const seen = new Set();
for (const { json: r } of $('Read seen posts').all()) if (r && r.post_id) seen.add(String(r.post_id));

const posts = [];
// Reddit (official node output)
let reddit = [];
try { reddit = $('Get new Reddit posts').all(); } catch (e) { reddit = []; }
for (const { json: p } of reddit) {
  if (!p || !p.id || p.stickied) continue;
  posts.push({
    post_id: 'reddit_' + p.id,
    source: 'r/' + (p.subreddit || ''),
    group: lc(p.subreddit),
    title: String(p.title || ''),
    body: String(p.selftext || '').slice(0, 3000),
    url: 'https://www.reddit.com' + (p.permalink || ''),
    author: p.author ? 'u/' + p.author : '',
    posted_ms: Number(p.created_utc) * 1000,
    flair: String(p.link_flair_text || ''),
  });
}
// n8n community Jobs category (Discourse JSON)
let forum = [];
try { forum = $('Get n8n forum jobs').all(); } catch (e) { forum = []; }
for (const { json: page } of forum) {
  const topics = (page && page.topic_list && page.topic_list.topics) || [];
  for (const t of topics) {
    if (!t || !t.id || t.pinned || t.closed) continue;
    posts.push({
      post_id: 'n8nforum_' + t.id,
      source: 'n8n community (Jobs)',
      group: 'n8n_forum',
      title: String(t.title || ''),
      body: String(t.excerpt || '').slice(0, 3000),
      url: 'https://community.n8n.io/t/' + t.slug + '/' + t.id,
      author: '',
      posted_ms: Date.parse(t.created_at),
      flair: (t.tags || []).join(', '),
    });
  }
}

const picked = [];
const thisRun = new Set();
for (const p of posts) {
  if (seen.has(p.post_id) || thisRun.has(p.post_id)) continue;
  if (!p.posted_ms || now - p.posted_ms > maxAgeMs) continue;
  const text = lc(p.title + ' ' + p.flair + ' ' + p.body);
  const title = lc(p.title + ' ' + p.flair);
  if (has(text, cfg.exclude_keywords)) continue;
  if (p.group === 'forhire' && !title.includes('hiring')) continue; // r/forhire: only [Hiring] posts
  if (!has(text, cfg.intent_keywords) && p.group !== 'n8n_forum') continue;
  const topicOk = (cfg.topic_always_relevant || []).map(lc).includes(p.group) || has(text, cfg.topic_keywords);
  if (!topicOk) continue;
  thisRun.add(p.post_id);
  picked.push(p);
}
picked.sort((a, b) => b.posted_ms - a.posted_ms);
return picked.slice(0, Number(cfg.max_posts_scored_per_run) || 25).map((p) => ({ json: {
  post_id: p.post_id, source: p.source, title: p.title, body: p.body, url: p.url, author: p.author,
  posted_at: new Date(p.posted_ms).toISOString(),
} }));"""

PROMPT = """You help a freelancer find people who might want to pay for an n8n automation.

About the freelancer (be truthful, never add anything to this):
{{ $('Settings').first().json.config.about_me }}

Post from {{ $json.source }}:
Title: {{ $json.title }}
{{ $json.body }}

Return:
- fit_score: a whole number 1-10. 9-10 = they clearly want to pay someone to build an automation the freelancer can build. 6-8 = a real need the freelancer could help with, budget unclear. 1-5 = not a buyer (they are selling, just chatting, want a full-time employee, want something unrelated, or it's a school project).
- why: one short sentence explaining the score.
- draft_reply: a short, friendly, honest reply (3-5 sentences) the freelancer could post or DM by hand. Answer their actual problem with one useful tip first, then offer to help. Say plainly that the freelancer is new if experience comes up. Never claim past clients, results, reviews or years of experience. No links, no hard sell, no emojis. If fit_score is 5 or lower, return an empty string."""

BUILD_ROW = """const post = $('Find new buying posts').item.json;
const ai = $json.output || {};
const score = Math.max(1, Math.min(10, Math.round(Number(ai.fit_score)) || 1));
return { json: {
  post_id: post.post_id, source: post.source, title: post.title, url: post.url, author: post.author,
  posted_at: post.posted_at, found_at: new Date().toISOString(), fit_score: score,
  why: String(ai.why || ''), draft_reply: score > 5 ? String(ai.draft_reply || '') : '', status: 'new',
} };"""

DIGEST = """// One email with every post at or above the minimum fit score. Nothing is posted anywhere.
const cfg = $('Settings').first().json.config;
const min = Number(cfg.min_fit_score) || 7;
const good = $input.all().map((i) => i.json).filter((r) => r.fit_score >= min).sort((a, b) => b.fit_score - a.fit_score);
if (!good.length) return [];
const blocks = good.map((r, i) => [
  `${i + 1}. [${r.fit_score}/10] ${r.title}`,
  `   ${r.source}${r.author ? ' - ' + r.author : ''} - posted ${String(r.posted_at || '').slice(0, 16).replace('T', ' ')} UTC`,
  `   ${r.url}`,
  `   Why: ${r.why}`,
  '   Draft reply (edit before using, check the community rules first):',
  r.draft_reply.split('\\n').map((l) => '   > ' + l).join('\\n'),
].join('\\n'));
return [{ json: {
  subject: `Buyer finder: ${good.length} post${good.length === 1 ? '' : 's'} worth a look`,
  body: blocks.join('\\n\\n') + '\\n\\nAll scored posts are in your "Seen" sheet. Reply by hand; this workflow never posts or messages anyone.',
} }];"""


def build():
    w = WF("buyer-finder", "Buyer finder: hourly digest of people asking for automation help")
    trig = n_schedule(w, "every 1 hours", 0, 0)
    st = n_settings(w, CFG, 220, 0)
    seen = n_sheet(w, "Read seen posts", "read", 440, 0)
    for n in w.nodes:
        if n["name"] == seen:
            n["executeOnce"] = True
    subs = n_code(w, "List subreddits", LIST_SUBS, 680, -120)
    reddit = w.add("Get new Reddit posts", "n8n-nodes-base.reddit", 1,
                   {"resource": "post", "operation": "getAll",
                    "subreddit": "={{ $json.subreddit }}", "returnAll": False, "limit": 50,
                    "filters": {"category": "new"}},
                   900, -120, onError="continueRegularOutput", retryOnFail=True, waitBetweenTries=5000, alwaysOutputData=True)
    forum = w.add("Get n8n forum jobs", "n8n-nodes-base.httpRequest", 4.2,
                  {"url": "={{ $('Settings').first().json.config.n8n_forum_jobs_url }}",
                   "sendHeaders": True,
                   "headerParameters": {"parameters": [
                       {"name": "User-Agent", "value": "={{ $('Settings').first().json.config.user_agent }}"},
                       {"name": "Accept", "value": "application/json"}]},
                   "options": {"timeout": 20000}},
                  900, 120, executeOnce=True, onError="continueRegularOutput", alwaysOutputData=True)
    merge = w.add("Wait for both sources", "n8n-nodes-base.merge", 3.2, {"numberInputs": 2}, 1140, 0)
    filt = n_code(w, "Find new buying posts", FILTER, 1360, 0)
    for n in w.nodes:
        if n["name"] == filt:
            n["alwaysOutputData"] = False
    ai = n_ai(w, "AI: score fit and draft reply", PROMPT, {
        "fit_score": 8, "why": "Small business owner wants an n8n flow that replies to new leads; budget mentioned.",
        "draft_reply": "Hi! For instant replies, the usual setup is a webhook from your form into n8n..."}, 1600, 0)
    # n_ai uses sx() which rewrites {x} shorthand; the prompt above is already n8n syntax, so restore it as-is.
    for n in w.nodes:
        if n["name"] == ai:
            n["parameters"]["text"] = "=" + PROMPT
    row = w.add("Build sheet row", "n8n-nodes-base.code", 2, {"mode": "runOnceForEachItem", "jsCode": BUILD_ROW}, 1900, 0)
    save = n_sheet(w, "Save to Seen sheet", "append", 2140, -120)
    dig = n_code(w, "Build the digest", DIGEST, 2140, 120)
    mail = w.add("Email the digest", "n8n-nodes-base.gmail", 2.2,
                 {"sendTo": "={{ $('Settings').first().json.config.digest_email }}",
                  "subject": "={{ $json.subject }}", "emailType": "text", "message": "={{ $json.body }}",
                  "options": {"appendAttribution": False}}, 2380, 120)
    w.chain(trig, st, seen)
    w.link(seen, subs)
    w.link(seen, forum)
    w.link(subs, reddit)
    w.link(reddit, merge)
    w.conns[forum] = {"main": [[{"node": merge, "type": "main", "index": 1}]]}
    w.chain(merge, filt, ai, row)
    w.link(row, save)
    w.link(row, dig)
    w.link(dig, mail)
    w.sticky("Note: what this does",
             "## Buyer finder\nEvery hour it reads the newest posts in your chosen subreddits and the n8n community **Jobs** category, "
             "keeps posts from the last 24 hours where someone is asking for paid help with automation, skips anything already in your sheet, "
             "and has AI score each one 1-10 and draft an honest reply.\n\nYou get **one email** with the posts that scored 7+. "
             "**It never posts, comments or messages anyone.** Read the post, check the community's rules, and reply by hand.",
             -60, -480, 460, 330, 4)
    w.sticky("Note: setup",
             "## Setup (about 15 minutes)\n1. Google Sheet with a tab **Seen** and the headers from `seen-sheet-headers.csv`.\n"
             "2. Reddit: create a 'web app' at reddit.com/prefs/apps, then add a **Reddit OAuth2** credential in n8n and select it on **Get new Reddit posts**.\n"
             "3. Open **Settings**: subreddits, your email, sheet URL, and `about_me` (keep it true).\n"
             "4. Connect Google Sheets, Gmail and OpenAI on the nodes with warnings.\n"
             "5. Run once by hand, then set the workflow to **Active**.\n\n"
             "Load: 5 Reddit requests + 1 forum request an hour, well under both sites' limits. AI scores at most 25 posts per run.",
             440, -480, 520, 330, 7)
    return w


def main():
    w = build()
    with open(os.path.join(HERE, "buyer-finder.workflow.json"), "w") as f:
        json.dump(w.json(), f, indent=2, ensure_ascii=False)
    with open(os.path.join(HERE, "seen-sheet-headers.csv"), "w") as f:
        f.write(",".join(COLS) + "\n")
    # export the code for tests
    with open(os.path.join(HERE, "test", "code.json"), "w") as f:
        json.dump({"FILTER": FILTER, "BUILD_ROW": BUILD_ROW, "DIGEST": DIGEST, "LIST_SUBS": LIST_SUBS, "CFG": CFG}, f, indent=1)
    print("nodes:", len(w.nodes))


if __name__ == "__main__":
    main()
