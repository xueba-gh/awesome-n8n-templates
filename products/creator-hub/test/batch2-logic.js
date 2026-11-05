// Logic tests for the Code nodes of workflows 116-139 (node test/batch2-logic.js)
const fs = require('fs'), path = require('path'), assert = require('assert');
const W = (slug) => JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'workflows', slug, 'workflow.json')));
const code = (w, name) => w.nodes.find((n) => n.name === name).parameters.jsCode;
const cfgOf = (w, name = 'Settings') => JSON.parse(w.nodes.find((n) => n.name === name).parameters.jsonOutput).config;
function run(js, nodes, input, json) {
  const $ = (n) => { const a = (nodes[n] || []).map((x) => (x.json ? x : { json: x })); return { all: () => a, first: () => a[0], item: a[0] }; };
  const $input = { all: () => input.map((x) => (x.json ? x : { json: x })) };
  return new Function('$', '$input', '$json', js)($, $input, json);
}
const now = new Date().toISOString(), old = new Date(Date.now() - 10 * 86400000).toISOString();

// RSS digest
let w = W('120-industry-news-daily-digest'); let cfg = cfgOf(w);
let out = run(code(w, 'Keep new items'), { Settings: [{ config: cfg }] },
  [{ title: 'A', link: 'l1', isoDate: now, contentSnippet: 'x' }, { title: 'A', link: 'l1', isoDate: now }, { title: 'Old', link: 'l2', isoDate: old }, { error: 'feed down' }]);
assert.strictEqual(out.length, 1); assert.strictEqual(out[0].json.count, 1);
assert.strictEqual(run(code(w, 'Keep new items'), { Settings: [{ config: cfg }] }, [{ title: 'Old', link: 'l2', isoDate: old }]).length, 0);
// RSS keyword alert
w = W('121-rss-keyword-job-alerts'); cfg = cfgOf(w);
out = run(code(w, 'Keep new items'), { Settings: [{ config: cfg }] },
  [{ title: 'Need n8n dev', link: 'a', isoDate: now }, { title: 'Bakery for sale', link: 'b', isoDate: now }]);
assert.deepStrictEqual(out.map((o) => o.json.link), ['a']);
// VIP
w = W('123-gmail-vip-alert-to-telegram'); cfg = cfgOf(w);
const mail = (a) => ({ from: { value: [{ address: a }], text: a }, subject: 's', text: 'hello' });
out = run(code(w, 'Is it from a VIP?'), { Settings: [{ config: cfg }], 'New email': [mail('Boss@example.com'), mail('x@bigclient.com'), mail('spam@foo.com')] }, []);
assert.strictEqual(out.length, 2);
// Dispatch
w = W('124-daily-job-dispatch-telegram');
const today = now.slice(0, 10);
out = run(code(w, "Group today's jobs by worker"), {}, [
  { date: today, time: '10:00', worker: 'Ana', worker_chat_id: '1', client: 'B', address: 'x' },
  { date: today, time: '08:00', worker: 'Ana', worker_chat_id: '1', client: 'A', address: 'y' },
  { date: '2000-01-01', worker: 'Bo', worker_chat_id: '2' }]);
assert.strictEqual(out.length, 1); assert.ok(out[0].json.text.indexOf('A') < out[0].json.text.indexOf('2. 10:00'));
// Missed call
w = W('126-missed-call-text-back');
assert.strictEqual(run(code(w, 'Was it missed?'), {}, [], { body: { DialCallStatus: 'no-answer', From: '+1555' } })[0].json.missed, true);
assert.strictEqual(run(code(w, 'Was it missed?'), {}, [], { body: { DialCallStatus: 'completed', From: '+1555' } })[0].json.missed, false);
// SMS reminder filter
w = W('127-appointment-reminder-sms'); cfg = cfgOf(w);
const soon = new Date(Date.now() + 5 * 3600000).toISOString(), later = new Date(Date.now() + 3 * 86400000).toISOString();
out = run(code(w, 'Find rows to text'), { Settings: [{ config: cfg }] },
  [{ phone: '+1', appointment_at: soon }, { phone: '+1', appointment_at: later }, { phone: '+1', appointment_at: soon, reminder_sent: 'x' }]);
assert.strictEqual(out.length, 1);
// Attachments
w = W('135-gmail-attachments-to-google-drive'); cfg = cfgOf(w);
out = run(code(w, 'One item per attachment'), { Settings: [{ config: cfg }], 'New email with attachment': [{ json: { from: { value: [{ address: 'a@b.com' }] }, subject: 'Inv', date: now }, binary: { attachment_0: { fileName: 'x.pdf' }, attachment_1: { fileName: 'y.pdf' } } }] }, []);
assert.strictEqual(out.length, 2); assert.ok(out[0].binary.data);
// Airtable flatten
w = W('132-airtable-to-google-sheets-sync');
out = run(code(w, 'Flatten for the sheet'), {}, [{ id: 'rec1', createdTime: 't', fields: { Name: 'A', Tags: ['x', 'y'] } }]);
assert.deepStrictEqual([out[0].json.airtable_id, out[0].json.Name, out[0].json.Tags], ['rec1', 'A', 'x, y']);
// Dedupe
w = W('138-google-sheet-duplicate-finder'); cfg = cfgOf(w);
out = run(code(w, 'Find duplicates'), { Settings: [{ config: cfg }] }, [{ email: 'A@x.com ', row_number: 2 }, { email: 'a@x.com', row_number: 5 }, { email: 'b@x.com', row_number: 6 }, { email: '', row_number: 7 }, { email: '', row_number: 8 }]);
assert.strictEqual(out[0].json.count, 1); assert.ok(out[0].json.list.includes('rows 2, 5'));
// CSV cleaner
w = W('139-csv-upload-cleaner-to-google-sheets'); cfg = cfgOf(w);
out = run(code(w, 'Clean the rows'), { Settings: [{ config: cfg }] }, [
  { 'First Name': '  jOHN  ', 'Email': ' John@X.com ', Phone: '(555) 123-4567' }, { 'First Name': 'John', Email: 'john@x.com', Phone: '5551234567' },
  { 'First Name': 'No mail', Email: 'bad' }]);
assert.strictEqual(out.length, 1); assert.deepStrictEqual([out[0].json.first_name, out[0].json.email, out[0].json.phone], ['John', 'john@x.com', '5551234567']);
console.log('Batch 2 logic tests passed (10 workflows).');
