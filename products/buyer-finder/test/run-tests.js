// Runs the buyer-finder Code-node logic with sample data (no network, no n8n).
// node test/run-tests.js
const assert = require('assert');
const code = require('./code.json');

function run(js, nodes, input = [], item = null) {
  const $ = (name) => {
    if (!(name in nodes)) throw new Error('no node ' + name);
    const arr = nodes[name].map((j) => ({ json: j }));
    return { all: () => arr, first: () => arr[0], item: arr[0] };
  };
  const $input = { all: () => input.map((j) => ({ json: j })) };
  const $json = item;
  return new Function('$', '$input', '$json', js)($, $input, $json);
}

const now = Date.now() / 1000;
const cfg = code.CFG;
const reddit = [
  { id: 'a1', subreddit: 'smallbusiness', title: 'Looking for someone to automate lead follow up', selftext: 'We use Gmail and Google Sheets, budget $500', permalink: '/r/smallbusiness/a1', author: 'jo', created_utc: now - 3600 },
  { id: 'a2', subreddit: 'smallbusiness', title: 'How do you price cupcakes?', selftext: 'need help with pricing', permalink: '/r/smallbusiness/a2', author: 'x', created_utc: now - 3600 },
  { id: 'a3', subreddit: 'forhire', title: '[For Hire] n8n developer available', selftext: 'hire me', permalink: '/r/forhire/a3', author: 'y', created_utc: now - 100 },
  { id: 'a4', subreddit: 'forhire', title: '[Hiring] n8n expert to build CRM workflow', selftext: 'paid project', permalink: '/r/forhire/a4', author: 'z', created_utc: now - 200 },
  { id: 'a5', subreddit: 'n8n', title: 'Need help with my webhook', selftext: 'can someone look at this', permalink: '/r/n8n/a5', author: 'q', created_utc: now - 90000 }, // too old
  { id: 'a6', subreddit: 'n8n', title: 'Can someone build me a WhatsApp bot? Will pay', selftext: '', permalink: '/r/n8n/a6', author: 'r', created_utc: now - 60 },
  { id: 'seen1', subreddit: 'n8n', title: 'Looking for n8n freelancer', selftext: '', permalink: '/r/n8n/seen1', author: 's', created_utc: now - 60 },
  { error: 'rate limited' },
];
const forum = [{ topic_list: { topics: [
  { id: 101, slug: 'need-n8n-dev', title: 'Need n8n dev for Shopify sync', created_at: new Date().toISOString(), pinned: false },
  { id: 103, slug: 'closed-job', title: 'Looking for n8n help', created_at: new Date().toISOString(), pinned: false, closed: true },
  { id: 102, slug: 'guidelines', title: 'Jobs category guidelines', created_at: new Date().toISOString(), pinned: true },
] } }];

// 1. List subreddits
const subs = run(code.LIST_SUBS, { Settings: [{ config: cfg }] });
assert.deepStrictEqual(subs.map((s) => s.json.subreddit), ['n8n', 'automation', 'smallbusiness', 'forhire', 'Entrepreneur']);

// 2. Filter
const picked = run(code.FILTER, {
  Settings: [{ config: cfg }],
  'Read seen posts': [{ post_id: 'reddit_seen1', row_number: 2 }],
  'Get new Reddit posts': reddit,
  'Get n8n forum jobs': forum,
}).map((i) => i.json.post_id).sort();
assert.deepStrictEqual(picked, ['n8nforum_101', 'n8nforum_103', 'reddit_a1', 'reddit_a4', 'reddit_a6'].sort(), 'picked: ' + picked);

// empty sheet (alwaysOutputData gives one empty item) and failed sources
const none = run(code.FILTER, { Settings: [{ config: cfg }], 'Read seen posts': [{}], 'Get new Reddit posts': [{}], 'Get n8n forum jobs': [{}] });
assert.strictEqual(none.length, 0);

// 3. Build row clamps score and blanks drafts for low scores
const post = { post_id: 'reddit_a1', source: 'r/smallbusiness', title: 't', url: 'u', author: 'u/jo', posted_at: new Date().toISOString() };
const row = run(code.BUILD_ROW, { 'Find new buying posts': [post] }, [], { output: { fit_score: '12', why: 'w', draft_reply: 'd' } });
assert.strictEqual(row.json.fit_score, 10);
const low = run(code.BUILD_ROW, { 'Find new buying posts': [post] }, [], { output: { fit_score: 3, why: 'w', draft_reply: 'd' } });
assert.strictEqual(low.json.draft_reply, '');

// 4. Digest only includes 7+, and nothing when none qualify
const rows = [{ ...row.json, fit_score: 9, draft_reply: 'Hi\nthere' }, { ...row.json, fit_score: 6 }, { ...row.json, fit_score: 7, title: 'second' }];
const dig = run(code.DIGEST, { Settings: [{ config: cfg }] }, rows);
assert.strictEqual(dig.length, 1);
assert.ok(dig[0].json.subject.includes('2 posts'));
assert.ok(dig[0].json.body.startsWith('1. [9/10]'));
assert.strictEqual(run(code.DIGEST, { Settings: [{ config: cfg }] }, [{ ...row.json, fit_score: 4 }]).length, 0);

console.log('All buyer-finder logic tests passed.');
console.log(dig[0].json.subject + '\n\n' + dig[0].json.body);
