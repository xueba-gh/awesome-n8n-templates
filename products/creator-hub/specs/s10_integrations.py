"""Batch 2: workflows for the apps buyers search for most after Sheets and Gmail
(RSS, Telegram, Twilio SMS, HubSpot, Airtable, Notion, Google Drive) plus three utilities.
Each spec has type "X" and its own build function."""
import json
from lib import (WF, ex, n_settings, n_webhook, n_form, n_schedule, n_code, n_if, n_sheet,
                 n_gmail_send, n_slack, n_ai, setup_notes, FLATTEN, uid)
from arch import needs_from, SHEET_URL, DX

C_CONTENT = "Marketing & content"
C_SALES = "Lead capture & sales"
C_SUPPORT = "Customer support"
C_OPS = "Operations & HR"
C_DEV = "Monitoring, data & dev"
C_LOCAL = "Local business"
C_GMAIL = "Gmail & inbox"

HELPERS = ("const daysSince = (v) => { const t = Date.parse(v); return isNaN(t) ? null : (Date.now() - t) / 86400000; };\n"
           "const daysUntil = (v) => { const t = Date.parse(v); return isNaN(t) ? null : (t - Date.now()) / 86400000; };\n"
           "const has = (v) => v !== undefined && v !== null && String(v).trim() !== '';\n"
           "const cfg = $('Settings').first().json.config;\n")


def _set(w, name, **kw):
    for n in w.nodes:
        if n["name"] == name:
            n.update(kw)
            return n
    raise KeyError(name)


def clean_fields(w, fields, x, y, name="Clean up details"):
    js = (FLATTEN +
          "const FIELDS = %s;\n"
          "return $input.all().map((item) => {\n"
          "  const { config, headers, params, query, webhookUrl, executionMode, submittedAt, formMode, ...rest } = item.json;\n"
          "  const d = flatten(rest.body || rest);\n"
          "  const out = { received_at: new Date().toISOString() };\n"
          "  for (const f of FIELDS) out[f] = d[f] === undefined || d[f] === null ? '' : String(d[f]).trim();\n"
          "  if (out.email !== undefined) out.email = out.email.toLowerCase();\n"
          "  return { json: out };\n"
          "});" % json.dumps(fields))
    return n_code(w, name, js, x, y)


def ai_text(w, name, prompt, schema, x, y):
    """n_ai, but the prompt is already n8n syntax except {cfg.x} shorthand."""
    a = n_ai(w, name, "", schema, x, y)
    import re
    _set(w, a)["parameters"]["text"] = "=" + re.sub(r"\{cfg\.(\w+)\}", lambda m: "{{ $('Settings').first().json.config.%s }}" % m.group(1), prompt)
    return a


# =================================================================== RSS

def build_rss(spec):
    w = WF(spec["slug"], spec["name"])
    mode = spec["mode"]  # digest | alert | per_item
    cfg = {"feeds": spec["feeds"], "hours_back": spec.get("hours_back", 24), "keywords": spec.get("keywords", []),
           "max_items": spec.get("max_items", 20), "owner_email": "you@example.com"}
    if spec.get("out") == "slack":
        cfg["slack_channel_id"] = "C0123456789"
    if mode == "per_item":
        cfg["sheet_url"] = SHEET_URL
        cfg["sheet_tab"] = spec["tab"]
    cfg.update(spec.get("cfg", {}))
    x = 0
    trig = n_schedule(w, spec.get("when", "daily 7"), x, 0)
    st = n_settings(w, cfg, x + DX, 0)
    lst = n_code(w, "List feeds", "return $('Settings').first().json.config.feeds.map((url) => ({ json: { url } }));", x + 2 * DX, 0)
    rss = w.add("Read the feed", "n8n-nodes-base.rssFeedRead", 1.1, {"url": "={{ $json.url }}", "options": {}},
                x + 3 * DX, 0, onError="continueRegularOutput")
    keep = ("const cfg = $('Settings').first().json.config;\n"
            "const since = Date.now() - Number(cfg.hours_back || 24) * 3600000;\n"
            "const kws = (cfg.keywords || []).map((k) => String(k).toLowerCase()).filter(Boolean);\n"
            "const seen = new Set();\n"
            "const items = [];\n"
            "for (const { json: it } of $input.all()) {\n"
            "  if (!it || !it.link || it.error) continue;\n"
            "  const t = Date.parse(it.isoDate || it.pubDate || '');\n"
            "  if (!isNaN(t) && t < since) continue;\n"
            "  if (seen.has(it.link)) continue;\n"
            "  const text = String((it.title || '') + ' ' + (it.contentSnippet || it.content || '')).replace(/<[^>]+>/g, ' ');\n"
            "  if (kws.length && !kws.some((k) => text.toLowerCase().includes(k))) continue;\n"
            "  seen.add(it.link);\n"
            "  items.push({ title: String(it.title || '').trim(), link: it.link, published: it.isoDate || it.pubDate || '',\n"
            "    source: String(it.creator || it.author || '').trim(), snippet: text.replace(/\\s+/g, ' ').trim().slice(0, 800) });\n"
            "}\n"
            "const top = items.slice(0, Number(cfg.max_items) || 20);\n")
    if mode == "digest":
        keep += ("if (!top.length) return [];\n"
                 "return [{ json: { count: top.length,\n"
                 "  items_text: top.map((i, n) => `${n + 1}. ${i.title}\\n${i.snippet}\\n${i.link}`).join('\\n\\n'),\n"
                 "  links: top.map((i, n) => `${n + 1}. ${i.title}\\n   ${i.link}`).join('\\n') } }];")
    else:
        keep += "return top.map((i) => ({ json: i }));"
    k = n_code(w, "Keep new items", keep, x + 4 * DX, 0)
    w.chain(trig, st, lst, rss, k)
    if mode == "digest":
        a = ai_text(w, "AI: write the digest", spec["prompt"] + "\n\nItems ({{ $json.count }}):\n{{ $json.items_text }}",
                    {"headline": "Short subject line", "summary": "The digest text"}, x + 5 * DX, 0)
        send = w.add("Email the digest", "n8n-nodes-base.gmail", 2.2,
                     {"sendTo": "={{ $('Settings').first().json.config.owner_email }}",
                      "subject": "=" + spec.get("subject_prefix", "") + "{{ $json.output.headline }}", "emailType": "text",
                      "message": "={{ $json.output.summary }}\n\nSources:\n{{ $('Keep new items').first().json.links }}",
                      "options": {"appendAttribution": False}}, x + 6 * DX, 0)
        w.chain(k, a, send)
        out_step = "Connect Gmail and OpenAI on the nodes with warnings."
    elif mode == "alert":
        if spec.get("out") == "slack":
            send = n_slack(w, "Post to Slack", spec["text"], x + 5 * DX, 0)
            out_step = "Connect Slack on **Post to Slack** and invite the app to the channel."
        else:
            send = n_gmail_send(w, "Email me", "{cfg.owner_email}", spec["subject"], spec["text"], x + 5 * DX, 0)
            out_step = "Connect Gmail on **Email me**."
        w.link(k, send)
    else:  # per_item: AI per item -> sheet (+ optional email)
        a = ai_text(w, "AI: process the item", spec["prompt"] + "\n\nTitle: {{ $json.title }}\nLink: {{ $json.link }}\nText: {{ $json.snippet }}",
                    spec["schema"], x + 5 * DX, 0)
        row = n_code(w, "Build the row",
                     "return $input.all().map((item, i) => ({ json: { ...$('Keep new items').all()[i].json, ...(item.json.output || {}), saved_at: new Date().toISOString() } }));",
                     x + 6 * DX, 0)
        save = n_sheet(w, "Save to sheet", "append", x + 7 * DX, 0)
        w.chain(k, a, row, save)
        out_step = "Use a Google Sheet with a tab named **%s** and the headers in `sheet-headers.csv`, then connect Google Sheets and OpenAI." % spec["tab"]
    setup_notes(w, spec["summary"],
                ["Open **Settings** and list your RSS feed URLs (most blogs have `/feed` or `/rss`; a YouTube channel is `https://www.youtube.com/feeds/videos.xml?channel_id=...`)." + spec.get("extra", ""),
                 out_step, "Run it once by hand and look at **Keep new items**, then switch to **Active**."], y=-420)
    cols = spec.get("cols")
    return w, cols, needs_from(w)


# =================================================================== Telegram

def tg_send(w, name, chat_expr, text, x, y):
    return w.add(name, "n8n-nodes-base.telegram", 1.2,
                 {"chatId": chat_expr, "text": text, "additionalFields": {"appendAttribution": False}}, x, y)


def build_tg_faq(spec):
    w = WF(spec["slug"], spec["name"])
    cfg = {"business_name": "Your Business", "tone": "friendly and short", "phone_for_humans": "(555) 010-0000",
           "booking_link": "https://cal.com/your-business", "knowledge_sheet_url": SHEET_URL, "knowledge_tab": "Knowledge"}
    trig = w.add("Telegram message", "n8n-nodes-base.telegramTrigger", 1.2, {"updates": ["message"], "additionalFields": {}},
                 0, 0, webhookId=uid(w.slug, "tg"))
    st = n_settings(w, cfg, DX, 0)
    doc = {"__rl": True, "mode": "url", "value": "={{ $('Settings').first().json.config.knowledge_sheet_url }}"}
    sh = {"__rl": True, "mode": "name", "value": "={{ $('Settings').first().json.config.knowledge_tab }}"}
    faq = w.add("Load FAQ sheet", "n8n-nodes-base.googleSheets", 4.7,
                {"operation": "read", "documentId": doc, "sheetName": sh, "options": {}}, 2 * DX, 0, executeOnce=True, alwaysOutputData=True)
    prep = n_code(w, "Prepare the question",
                  "const msg = $('Telegram message').first().json.message || {};\n"
                  "const text = String(msg.text || '').trim();\n"
                  "if (!text) return [];\n"
                  "const lines = $input.all().map((i) => Object.entries(i.json).filter(([k, v]) => k !== 'row_number' && String(v ?? '').trim() !== '').map(([, v]) => String(v).trim()).join(': ')).filter(Boolean);\n"
                  "return [{ json: { chat_id: msg.chat.id, first_name: (msg.from && msg.from.first_name) || '', text: text.slice(0, 2000),\n"
                  "  is_start: text === '/start', knowledge: lines.join('\\n') || '(The FAQ sheet is empty.)' } }];", 3 * DX, 0)
    a = ai_text(w, "AI: answer from the FAQ",
                "You answer customer questions for {cfg.business_name} on Telegram. Tone: {cfg.tone}. Reply in 1-3 short sentences, plain text, in the customer's language.\n"
                "Use ONLY these facts:\n{{ $json.knowledge }}\n\nBooking link: {cfg.booking_link}\nPhone for a person: {cfg.phone_for_humans}\n"
                "If the answer is not in the facts, say you're not sure and give the phone number. Never invent prices or promises.\n"
                "If the message is /start, greet {{ $json.first_name || 'them' }} and say what you can help with.\n\nCustomer message: {{ $json.text }}",
                {"reply": "Hi! We're open 9am-5pm Monday to Friday."}, 4 * DX, 0)
    send = tg_send(w, "Reply on Telegram", "={{ $('Prepare the question').item.json.chat_id }}", "={{ $json.output.reply }}", 5 * DX, 0)
    w.chain(trig, st, faq, prep, a, send)
    setup_notes(w, spec["summary"],
                ["Create a bot with **@BotFather** in Telegram and copy its token into a Telegram credential in n8n (you paste it, nobody else).",
                 "Make a Google Sheet with a tab **Knowledge** and two headers: `topic`, `answer`. Add your real facts.",
                 "Open **Settings**: business name, phone, booking link, sheet URL.",
                 "Connect Telegram, Google Sheets and OpenAI, then switch to **Active** and message your bot."], y=-420)
    return w, ["topic", "answer"], needs_from(w)


def build_tg_alert(spec):
    """Something happens -> short Telegram message to you (or your team chat)."""
    w = WF(spec["slug"], spec["name"])
    cfg = {"telegram_chat_id": "123456789"}
    cfg.update(spec.get("cfg", {}))
    src = spec["source"]
    if src == "gmail":
        cfg["vip_senders"] = spec["vip"]
        trig = w.add("New email", "n8n-nodes-base.gmailTrigger", 1.3,
                     {"pollTimes": {"item": [{"mode": "everyMinute"}]}, "simple": False,
                      "filters": {"q": "in:inbox -from:me", "readStatus": "unread"}, "options": {}}, 0, 0)
        st = n_settings(w, cfg, DX, 0)
        pick = n_code(w, "Is it from a VIP?",
                      "const cfg = $('Settings').first().json.config;\n"
                      "const vips = (cfg.vip_senders || []).map((v) => String(v).toLowerCase().trim()).filter(Boolean);\n"
                      "return $('New email').all().filter((i) => {\n"
                      "  const from = String((i.json.from && i.json.from.value && i.json.from.value[0] && i.json.from.value[0].address) || '').toLowerCase();\n"
                      "  return vips.some((v) => v.startsWith('@') ? from.endsWith(v) : from === v);\n"
                      "}).map((i) => ({ json: {\n"
                      "  from: (i.json.from && i.json.from.text) || '', subject: i.json.subject || '(no subject)',\n"
                      "  snippet: String(i.json.text || i.json.snippet || '').replace(/\\s+/g, ' ').slice(0, 300) } }));", 2 * DX, 0)
        send = tg_send(w, "Telegram me", "={{ $('Settings').first().json.config.telegram_chat_id }}",
                       "=VIP email from {{ $json.from }}\n{{ $json.subject }}\n\n{{ $json.snippet }}", 3 * DX, 0)
        w.chain(trig, st, pick, send)
        first = "Open **Settings**: your Telegram chat ID and the VIP list (full addresses, or `@domain.com` for a whole company)."
        extra_need = "Connect Gmail and Telegram."
        cols = None
    elif src == "webhook":
        fields = spec["fields"]
        cfg.update({"sheet_url": SHEET_URL, "sheet_tab": spec["tab"]})
        trig = n_webhook(w, spec["path"], 0, 0)
        st = n_settings(w, cfg, DX, 0)
        cl = clean_fields(w, fields, 2 * DX, 0)
        save = n_sheet(w, "Save to sheet", "append", 3 * DX, -100)
        send = tg_send(w, "Telegram me", "={{ $('Settings').first().json.config.telegram_chat_id }}", ex(spec["text"], "Clean up details"), 3 * DX, 100)
        w.chain(trig, st, cl)
        w.link(cl, save); w.link(cl, send)
        first = "Open **Settings**: your Telegram chat ID, sheet URL. Send the form's POST to the **Webhook** URL."
        extra_need = "Make a sheet tab **%s** with the headers in `sheet-headers.csv`, then connect Google Sheets and Telegram." % spec["tab"]
        cols = ["received_at"] + fields
    else:  # schedule: dispatch today's jobs from a sheet to each worker
        cfg.update({"sheet_url": SHEET_URL, "sheet_tab": spec["tab"], "business_name": "Your Business"})
        trig = n_schedule(w, spec.get("when", "daily 6"), 0, 0)
        st = n_settings(w, cfg, DX, 0)
        read = n_sheet(w, "Read jobs", "read", 2 * DX, 0)
        grp = n_code(w, "Group today's jobs by worker",
                     "const today = new Date().toISOString().slice(0, 10);\n"
                     "const by = {};\n"
                     "for (const { json: r } of $input.all()) {\n"
                     "  if (String(r.date || '').slice(0, 10) !== today || !r.worker_chat_id) continue;\n"
                     "  (by[r.worker_chat_id] = by[r.worker_chat_id] || []).push(r);\n"
                     "}\n"
                     "return Object.entries(by).map(([chat, jobs]) => ({ json: { chat_id: chat, worker: jobs[0].worker || '',\n"
                     "  text: `Good morning ${jobs[0].worker || ''}! Your jobs today:\\n\\n` + jobs.sort((a, b) => String(a.time).localeCompare(String(b.time)))\n"
                     "    .map((j, i) => `${i + 1}. ${j.time || ''} ${j.client || ''}\\n   ${j.address || ''}\\n   ${j.notes || ''}`.trimEnd()).join('\\n\\n') } }));",
                     3 * DX, 0)
        send = tg_send(w, "Send each worker their list", "={{ $json.chat_id }}", "={{ $json.text }}", 4 * DX, 0)
        w.chain(trig, st, read, grp, send)
        first = "Make a sheet tab **%s** with the headers in `sheet-headers.csv`. Each worker messages your bot once; put their chat ID in `worker_chat_id`." % spec["tab"]
        extra_need = "Open **Settings**: sheet URL. Connect Google Sheets and Telegram."
        cols = ["date", "time", "worker", "worker_chat_id", "client", "address", "notes"]
    setup_notes(w, spec["summary"],
                ["Create a Telegram bot with **@BotFather** and add its token as a Telegram credential in n8n. Send your bot a message, then get your chat ID (for example from @userinfobot).",
                 first, extra_need, "Run it once with test data, then switch to **Active**."], y=-420)
    return w, cols, needs_from(w)


# =================================================================== Twilio SMS

def twilio_send(w, name, to_expr, msg_expr, x, y):
    return w.add(name, "n8n-nodes-base.twilio", 1,
                 {"from": "={{ $('Settings').first().json.config.twilio_from_number }}", "to": to_expr, "message": msg_expr,
                  "options": {}}, x, y, onError="continueRegularOutput")


def build_missed_call(spec):
    w = WF(spec["slug"], spec["name"])
    cfg = {"business_name": "Your Business", "owner_phone": "+15550000000", "owner_email": "you@example.com",
           "twilio_from_number": "+15550000001", "ring_seconds": 20,
           "dial_result_url": "PASTE_THE_PRODUCTION_URL_OF_THE_'Call_finished'_WEBHOOK",
           "text_back": "Hi, sorry we missed your call at [business]! How can we help? Reply here and we'll get back to you shortly.",
           "sheet_url": SHEET_URL, "sheet_tab": "Missed calls"}
    inc = w.add("Incoming call", "n8n-nodes-base.webhook", 2.1, {"httpMethod": "POST", "path": "incoming-call", "responseMode": "responseNode", "options": {}},
                0, 0, webhookId=uid(w.slug, "in"))
    st1 = n_settings(w, cfg, DX, 0)
    twiml1 = w.add("Ring your phone", "n8n-nodes-base.respondToWebhook", 1.4,
                   {"respondWith": "text",
                    "responseBody": "=<Response><Dial timeout=\"{{ $('Settings').first().json.config.ring_seconds }}\" action=\"{{ $('Settings').first().json.config.dial_result_url }}\" method=\"POST\">{{ $('Settings').first().json.config.owner_phone }}</Dial></Response>",
                    "options": {"responseHeaders": {"entries": [{"name": "Content-Type", "value": "text/xml"}]}}}, 2 * DX, 0)
    w.chain(inc, st1, twiml1)
    fin = w.add("Call finished", "n8n-nodes-base.webhook", 2.1, {"httpMethod": "POST", "path": "call-finished", "responseMode": "responseNode", "options": {}},
                0, 300, webhookId=uid(w.slug, "fin"))
    read = n_code(w, "Was it missed?",
                   "const b = $json.body || {};\n"
                   "const status = String(b.DialCallStatus || '').toLowerCase();\n"
                   "const missed = ['no-answer', 'busy', 'failed', 'canceled'].includes(status);\n"
                   "return [{ json: { caller: String(b.From || '').trim(), status, missed, called_at: new Date().toISOString() } }];", DX, 300)
    twiml2 = w.add("Answer Twilio", "n8n-nodes-base.respondToWebhook", 1.4,
                   {"respondWith": "text",
                    "responseBody": "={{ $json.missed ? '<Response><Say>Sorry we missed you. We will text you right away.</Say></Response>' : '<Response></Response>' }}",
                    "options": {"responseHeaders": {"entries": [{"name": "Content-Type", "value": "text/xml"}]}}}, 2 * DX, 300)
    iff = n_if(w, "Missed?", "={{ $('Was it missed?').item.json.missed && $('Was it missed?').item.json.caller !== '' }}", 3 * DX, 300)
    # this branch runs in its own execution, so it needs its own copy of the settings
    cfgjs = w.add("Settings for texts", "n8n-nodes-base.set", 3.4,
                  {"mode": "raw", "jsonOutput": json.dumps({"config": cfg}, indent=2), "includeOtherFields": True, "options": {}}, 4 * DX, 300)
    sms = w.add("Text the caller back", "n8n-nodes-base.twilio", 1,
                {"from": "={{ $('Settings for texts').first().json.config.twilio_from_number }}",
                 "to": "={{ $('Was it missed?').item.json.caller }}",
                 "message": "={{ $('Settings for texts').first().json.config.text_back.replace('[business]', $('Settings for texts').first().json.config.business_name) }}",
                 "options": {}}, 5 * DX, 100, onError="continueRegularOutput")
    row = n_code(w, "Log row", "const c = $('Was it missed?').first().json;\nreturn [{ json: { called_at: c.called_at, caller: c.caller, status: c.status, texted_back: 'yes' } }];", 5 * DX, 300)
    doc = {"__rl": True, "mode": "url", "value": "={{ $('Settings for texts').first().json.config.sheet_url }}"}
    sh = {"__rl": True, "mode": "name", "value": "={{ $('Settings for texts').first().json.config.sheet_tab }}"}
    save = w.add("Save to sheet", "n8n-nodes-base.googleSheets", 4.7,
                 {"operation": "append", "documentId": doc, "sheetName": sh,
                  "columns": {"mappingMode": "autoMapInputData", "value": {}, "matchingColumns": [], "schema": []},
                  "options": {"cellFormat": "RAW", "handlingExtraData": "ignoreIt"}}, 6 * DX, 300)
    mail = w.add("Email me", "n8n-nodes-base.gmail", 2.2,
                 {"sendTo": "={{ $('Settings for texts').first().json.config.owner_email }}",
                  "subject": "=Missed call from {{ $('Was it missed?').first().json.caller }} (texted back)",
                  "emailType": "text", "message": "=Missed call from {{ $('Was it missed?').first().json.caller }} at {{ $('Was it missed?').first().json.called_at }}. They got an automatic text. Call them back when you can.",
                  "options": {"appendAttribution": False}}, 6 * DX, 100)
    w.chain(fin, read, twiml2, iff)
    w.link(iff, cfgjs)
    w.link(cfgjs, sms); w.link(cfgjs, row)
    w.link(row, save); w.link(sms, mail)
    setup_notes(w, spec["summary"],
                ["Open **Settings** and **Settings for texts** (keep them the same): your phone, Twilio number, email, sheet URL. Make a sheet tab **Missed calls** with the headers in `sheet-headers.csv`.",
                 "Activate the workflow. Copy the production URL of **Call finished** into `dial_result_url` in **Settings**.",
                 "In Twilio, set your number's *A call comes in* webhook (POST) to the production URL of **Incoming call**.",
                 "Connect Twilio, Google Sheets and Gmail. Call your Twilio number and don't answer to test.",
                 "US numbers: texting needs A2P 10DLC registration in Twilio first."], y=-460)
    return w, ["called_at", "caller", "status", "texted_back"], needs_from(w)


def build_sms_schedule(spec):
    """Like archetype S, but sends an SMS with Twilio."""
    w = WF(spec["slug"], spec["name"])
    cfg = {"business_name": "Your Business", "twilio_from_number": "+15550000001", "sheet_url": SHEET_URL, "sheet_tab": spec["tab"]}
    cfg.update(spec.get("cfg", {}))
    trig = n_schedule(w, spec.get("when", "every 1 hours"), 0, 0)
    st = n_settings(w, cfg, DX, 0)
    read = n_sheet(w, "Read rows", "read", 2 * DX, 0)
    find = n_code(w, "Find rows to text", HELPERS + "return $input.all().filter((item) => {\n  const r = item.json;\n  return (%s);\n}).slice(0, 50);" % spec["filter"], 3 * DX, 0)
    sms = twilio_send(w, "Send the text", "={{ $json.phone }}", ex(spec["sms"]), 4 * DX, 0)
    col, val = spec["mark"]
    mk = n_code(w, "Mark rows as done",
                "const stamp = %s;\nreturn $('Find rows to text').all().map((item) => ({ json: { row_number: item.json.row_number, %s: stamp } }));" % (val, json.dumps(col)),
                5 * DX, 0)
    upd = n_sheet(w, "Update rows", "update", 6 * DX, 0, match=["row_number"])
    w.chain(trig, st, read, find, sms, mk, upd)
    setup_notes(w, spec["summary"],
                ["Make a sheet tab **%s** with the headers in `sheet-headers.csv`. Phone numbers in international format (+15551234567)." % spec["tab"],
                 "Open **Settings**: your business name, Twilio number, sheet URL.",
                 "Connect Twilio and Google Sheets. US numbers need A2P 10DLC registration in Twilio before texting.",
                 "Only text people who agreed to receive texts, and honour STOP replies. Run once with your own number, then switch to **Active**."], y=-420)
    return w, spec["cols"], needs_from(w)


# =================================================================== HubSpot / Airtable / Notion

def build_crm_intake(spec):
    """Form or webhook -> clean -> CRM (HubSpot or Airtable) -> welcome email -> owner alert."""
    w = WF(spec["slug"], spec["name"])
    crm = spec["crm"]
    fields = spec["fields"]
    cfg = {"business_name": "Your Business", "sender_name": "Your Name", "owner_email": "you@example.com"}
    if crm == "airtable":
        cfg["airtable_base_url"] = "https://airtable.com/appXXXXXXXXXXXXXX"
        cfg["airtable_table_url"] = "https://airtable.com/appXXXXXXXXXXXXXX/tblXXXXXXXXXXXXXX"
    cfg.update(spec.get("cfg", {}))
    if spec.get("trigger") == "form":
        trig = n_form(w, fields, spec.get("form_title", "Contact us"), 0, 0)
    else:
        trig = n_webhook(w, spec["path"], 0, 0)
    st = n_settings(w, cfg, DX, 0)
    cl = clean_fields(w, fields, 2 * DX, 0)
    if crm == "hubspot":
        first, _, last = "", "", ""
        add = {"firstName": "={{ $json.name.split(' ')[0] }}", "lastName": "={{ $json.name.split(' ').slice(1).join(' ') }}"}
        if "phone" in fields: add["phoneNumber"] = "={{ $json.phone }}"
        if "company" in fields: add["companyName"] = "={{ $json.company }}"
        c = w.add("Create or update HubSpot contact", "n8n-nodes-base.hubspot", 2.1,
                  {"authentication": "appToken", "resource": "contact", "operation": "upsert",
                   "email": "={{ $json.email }}", "additionalFields": add, "options": {}}, 3 * DX, 0)
        crm_step = "Create a HubSpot **private app** (Settings > Integrations > Private apps) with contacts read/write scope, and paste its token into a HubSpot App Token credential in n8n."
    else:
        c = w.add("Add to Airtable", "n8n-nodes-base.airtable", 2.1,
                  {"operation": "create",
                   "base": {"__rl": True, "mode": "url", "value": "={{ $('Settings').first().json.config.airtable_base_url }}"},
                   "table": {"__rl": True, "mode": "url", "value": "={{ $('Settings').first().json.config.airtable_table_url }}"},
                   "columns": {"mappingMode": "autoMapInputData", "value": {}, "matchingColumns": [], "schema": []},
                   "options": {"typecast": True}}, 3 * DX, 0)
        crm_step = "In Airtable, make a table with fields named exactly: " + ", ".join(["received_at"] + fields) + ". Create a personal access token (data.records:write, schema.bases:read) and add it as an Airtable credential."
    mail = n_gmail_send(w, "Welcome email", "{email}", spec["reply_subject"], spec["reply_body"], 4 * DX, -100, src="Clean up details")
    alert = n_gmail_send(w, "Tell the owner", "{cfg.owner_email}", spec["alert_subject"], spec["alert_body"], 4 * DX, 100, src="Clean up details")
    w.chain(trig, st, cl, c)
    w.link(c, mail); w.link(c, alert)
    setup_notes(w, spec["summary"],
                [crm_step, "Open **Settings**: business name, your name and email" + (", Airtable base and table URLs." if crm == "airtable" else "."),
                 "Connect Gmail on the two email nodes." + (" Share the form URL from the **Form** node." if spec.get("trigger") == "form" else " Send your form's POST to the **Webhook** URL."),
                 "Submit a test entry, check the record, then switch to **Active**."], y=-420)
    return w, None, needs_from(w)


def build_airtable_sync(spec):
    w = WF(spec["slug"], spec["name"])
    cfg = {"airtable_base_url": "https://airtable.com/appXXXXXXXXXXXXXX", "airtable_table_url": "https://airtable.com/appXXXXXXXXXXXXXX/tblXXXXXXXXXXXXXX",
           "sheet_url": SHEET_URL, "sheet_tab": "Airtable copy"}
    trig = n_schedule(w, "every 1 hours", 0, 0)
    st = n_settings(w, cfg, DX, 0)
    at = w.add("Get Airtable records", "n8n-nodes-base.airtable", 2.1,
               {"operation": "search",
                "base": {"__rl": True, "mode": "url", "value": "={{ $('Settings').first().json.config.airtable_base_url }}"},
                "table": {"__rl": True, "mode": "url", "value": "={{ $('Settings').first().json.config.airtable_table_url }}"},
                "returnAll": True, "options": {}}, 2 * DX, 0)
    fl = n_code(w, "Flatten for the sheet",
                "return $input.all().map(({ json: r }) => {\n"
                "  const out = { airtable_id: r.id, synced_at: new Date().toISOString() };\n"
                "  const fields = r.fields || r;\n"
                "  for (const [k, v] of Object.entries(fields)) {\n"
                "    if (k === 'id' || k === 'createdTime') continue;\n"
                "    out[k] = Array.isArray(v) ? v.map((x) => (x && typeof x === 'object' ? (x.name || x.url || JSON.stringify(x)) : x)).join(', ')\n"
                "      : v && typeof v === 'object' ? JSON.stringify(v) : v;\n"
                "  }\n"
                "  return { json: out };\n"
                "});", 3 * DX, 0)
    save = n_sheet(w, "Add or update sheet rows", "appendOrUpdate", 4 * DX, 0, match=["airtable_id"])
    w.chain(trig, st, at, fl, save)
    setup_notes(w, spec["summary"],
                ["Make a Google Sheet tab **Airtable copy** with headers `airtable_id`, `synced_at` and then your Airtable field names, spelt exactly the same.",
                 "Open **Settings**: Airtable base and table URLs, sheet URL.",
                 "Add an Airtable personal access token credential (data.records:read) and connect Google Sheets.",
                 "Run once: every record appears in the sheet, then each hour new records are added and changed ones updated (matched on airtable_id)."], y=-420)
    return w, ["airtable_id", "synced_at"], needs_from(w)


def notion_page(w, name, title_expr, body_expr, x, y):
    return w.add(name, "n8n-nodes-base.notion", 2.2,
                 {"resource": "databasePage", "operation": "create",
                  "databaseId": {"__rl": True, "mode": "url", "value": "={{ $('Settings').first().json.config.notion_database_url }}"},
                  "title": title_expr,
                  "propertiesUi": {"propertyValues": []},
                  "blockUi": {"blockValues": [{"textContent": body_expr}]},
                  "options": {}}, x, y)


def build_notion(spec):
    w = WF(spec["slug"], spec["name"])
    cfg = {"notion_database_url": "https://www.notion.so/your-workspace/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "owner_email": "you@example.com"}
    if spec["source"] == "gmail":
        trig = w.add("New email", "n8n-nodes-base.gmailTrigger", 1.3,
                     {"pollTimes": {"item": [{"mode": "everyMinute"}]}, "simple": False,
                      "filters": {"q": "in:inbox -from:me", "readStatus": "unread"}, "options": {}}, 0, 0)
        st = n_settings(w, cfg, DX, 0)
        rd = n_code(w, "Read the email",
                    "return $('New email').all().map((i) => ({ json: { from: (i.json.from && i.json.from.text) || '', subject: i.json.subject || '',\n"
                    "  body: String(i.json.text || i.json.snippet || '').slice(0, 4000) } }));", 2 * DX, 0)
        a = ai_text(w, "AI: is there a task?",
                    "Read this email and decide whether it asks the reader to do something.\n\nFrom: {{ $json.from }}\nSubject: {{ $json.subject }}\n\n{{ $json.body }}\n\n"
                    "Return is_task (true/false), task (a short imperative title, empty if no task), due (a date if one is stated, else empty) and details (one or two sentences of context).",
                    {"is_task": True, "task": "Send the signed contract to Acme", "due": "2026-11-20", "details": "Jane asked for the signed contract before the kickoff."}, 3 * DX, 0)
        iff = n_if(w, "Is it a task?", "={{ $json.output.is_task === true && $json.output.task !== '' }}", 4 * DX, 0)
        pg = notion_page(w, "Create Notion task", "={{ $json.output.task }}",
                         "={{ $json.output.details }}\nDue: {{ $json.output.due || 'not stated' }}\nFrom: {{ $('Read the email').item.json.from }} ({{ $('Read the email').item.json.subject }})",
                         5 * DX, -60)
        w.chain(trig, st, rd, a, iff)
        w.link(iff, pg)
        src_step = "Connect Gmail and OpenAI. Only emails that really ask you to do something become tasks."
    else:
        fields = ["meeting_title", "attendees", "notes"]
        trig = n_form(w, fields, "Meeting notes", 0, 0)
        st = n_settings(w, cfg, DX, 0)
        cl = clean_fields(w, fields, 2 * DX, 0)
        a = ai_text(w, "AI: summarise the meeting",
                    "Summarise this meeting. Do not invent owners or dates.\n\nTitle: {{ $json.meeting_title }}\nAttendees: {{ $json.attendees }}\nNotes:\n{{ $json.notes }}\n\n"
                    "Return summary (3 sentences), decisions (bullet list as text) and action_items (bullet list 'Owner: task (due)').",
                    {"summary": "...", "decisions": "- ...", "action_items": "- Sam: send the quote (Friday)"}, 3 * DX, 0)
        pg = notion_page(w, "Save to Notion", "={{ $('Clean up details').item.json.meeting_title }}",
                         "=Summary: {{ $json.output.summary }}\n\nDecisions:\n{{ $json.output.decisions }}\n\nAction items:\n{{ $json.output.action_items }}\n\nAttendees: {{ $('Clean up details').item.json.attendees }}",
                         4 * DX, 0)
        w.chain(trig, st, cl, a, pg)
        src_step = "Connect OpenAI. Open the form URL from the **Form** node and paste meeting notes or a transcript."
    setup_notes(w, spec["summary"],
                ["In Notion, create a database (a table) and an internal integration at notion.so/my-integrations. Share the database with the integration (... > Connections).",
                 "Add a Notion credential in n8n with the integration secret (you paste it). Open **Settings** and paste the database URL.",
                 src_step, "Test once, check the new page in Notion, then switch to **Active**."], y=-420)
    return w, None, needs_from(w)


# =================================================================== Google Drive

def build_drive_attachments(spec):
    w = WF(spec["slug"], spec["name"])
    cfg = {"drive_folder_id": "PASTE_FOLDER_ID_FROM_THE_FOLDER_URL", "only_from": [], "sheet_url": SHEET_URL, "sheet_tab": "Saved attachments"}
    trig = w.add("New email with attachment", "n8n-nodes-base.gmailTrigger", 1.3,
                 {"pollTimes": {"item": [{"mode": "everyMinute"}]}, "simple": False,
                  "filters": {"q": "has:attachment -from:me", "readStatus": "unread"}, "options": {"downloadAttachments": True}}, 0, 0)
    st = n_settings(w, cfg, DX, 0)
    split = n_code(w, "One item per attachment",
                   "const cfg = $('Settings').first().json.config;\n"
                   "const only = (cfg.only_from || []).map((s) => String(s).toLowerCase());\n"
                   "const out = [];\n"
                   "for (const item of $('New email with attachment').all()) {\n"
                   "  const from = String((item.json.from && item.json.from.value && item.json.from.value[0] && item.json.from.value[0].address) || '').toLowerCase();\n"
                   "  if (only.length && !only.some((o) => o.startsWith('@') ? from.endsWith(o) : from === o)) continue;\n"
                   "  const date = new Date(item.json.date || Date.now()).toISOString().slice(0, 10);\n"
                   "  for (const [key, bin] of Object.entries(item.binary || {})) {\n"
                   "    out.push({ json: { from, subject: item.json.subject || '', file_name: `${date} ${from.split('@')[0]} - ${bin.fileName || key}` },\n"
                   "      binary: { data: bin } });\n"
                   "  }\n"
                   "}\n"
                   "return out;", 2 * DX, 0)
    up = w.add("Upload to Google Drive", "n8n-nodes-base.googleDrive", 3,
               {"name": "={{ $json.file_name }}", "driveId": {"__rl": True, "mode": "list", "value": "My Drive"},
                "folderId": {"__rl": True, "mode": "id", "value": "={{ $('Settings').first().json.config.drive_folder_id }}"},
                "inputDataFieldName": "data", "options": {}}, 3 * DX, 0)
    row = n_code(w, "Log row",
                 "return $input.all().map((item, i) => { const src = $('One item per attachment').all()[i].json;\n"
                 "  return { json: { saved_at: new Date().toISOString(), from: src.from, subject: src.subject, file_name: src.file_name, drive_link: item.json.webViewLink || '' } }; });",
                 4 * DX, 0)
    save = n_sheet(w, "Save to sheet", "append", 5 * DX, 0)
    w.chain(trig, st, split, up, row, save)
    setup_notes(w, spec["summary"],
                ["Create a Drive folder and copy the ID from its URL (the part after /folders/) into **Settings**. Optional: `only_from` limits it to certain senders or `@domain.com`.",
                 "Make a sheet tab **Saved attachments** with the headers in `sheet-headers.csv` and put its URL in **Settings**.",
                 "Connect Gmail, Google Drive and Google Sheets.", "Send yourself an email with an attachment, then switch to **Active**."], y=-420)
    return w, ["saved_at", "from", "subject", "file_name", "drive_link"], needs_from(w)


def build_drive_new_file(spec):
    w = WF(spec["slug"], spec["name"])
    trig = w.add("New file in folder", "n8n-nodes-base.googleDriveTrigger", 1,
                 {"pollTimes": {"item": [{"mode": "everyMinute"}]}, "triggerOn": "specificFolder",
                  "folderToWatch": {"__rl": True, "mode": "url", "value": "https://drive.google.com/drive/folders/PASTE_FOLDER_ID"},
                  "event": "fileCreated", "options": {}}, 0, 0)
    st = n_settings(w, {"notify_emails": "you@example.com, teammate@example.com", "folder_name": "Client uploads"}, DX, 0)
    mail = w.add("Email the team", "n8n-nodes-base.gmail", 2.2,
                 {"sendTo": "={{ $('Settings').first().json.config.notify_emails }}",
                  "subject": "=New file in {{ $('Settings').first().json.config.folder_name }}: {{ $('New file in folder').item.json.name }}",
                  "emailType": "text",
                  "message": "=A new file was added to {{ $('Settings').first().json.config.folder_name }}.\n\nFile: {{ $('New file in folder').item.json.name }}\nOpen: {{ $('New file in folder').item.json.webViewLink }}",
                  "options": {"appendAttribution": False}}, 2 * DX, 0)
    w.chain(trig, st, mail)
    setup_notes(w, spec["summary"],
                ["Open **New file in folder** and paste the folder URL (or pick it from the list).",
                 "Open **Settings**: who gets the email and a friendly folder name.",
                 "Connect Google Drive and Gmail.", "Drop a test file in the folder, then switch to **Active**."], y=-420)
    return w, None, needs_from(w)


# =================================================================== Utilities

def build_error_alert(spec):
    w = WF(spec["slug"], spec["name"])
    trig = w.add("When any workflow fails", "n8n-nodes-base.errorTrigger", 1, {}, 0, 0)
    st = n_settings(w, {"alert_email": "you@example.com"}, DX, 0)
    mail = w.add("Email the error", "n8n-nodes-base.gmail", 2.2,
                 {"sendTo": "={{ $('Settings').first().json.config.alert_email }}",
                  "subject": "=Workflow failed: {{ $('When any workflow fails').item.json.workflow.name }}",
                  "emailType": "text",
                  "message": "=Workflow: {{ $('When any workflow fails').item.json.workflow.name }}\n"
                             "Failed node: {{ $('When any workflow fails').item.json.execution.lastNodeExecuted }}\n"
                             "Error: {{ $('When any workflow fails').item.json.execution.error.message }}\n"
                             "Time: {{ $now.toISO() }}\n\nOpen the failed run: {{ $('When any workflow fails').item.json.execution.url }}",
                  "options": {"appendAttribution": False}}, 2 * DX, 0)
    w.chain(trig, st, mail)
    setup_notes(w, spec["summary"],
                ["Open **Settings** and set the email for alerts. Connect Gmail.",
                 "Save this workflow. You do not need to activate it.",
                 "In each workflow you want watched: **Settings > Error workflow** and choose this one.",
                 "Test: make a workflow fail on purpose (for example a Code node with `throw new Error('test')`) and run it from a schedule or webhook. Manual runs do not trigger error workflows."], y=-420)
    return w, None, needs_from(w)


def build_dedupe(spec):
    w = WF(spec["slug"], spec["name"])
    cfg = {"sheet_url": SHEET_URL, "sheet_tab": "Contacts", "match_on": ["email"], "owner_email": "you@example.com"}
    trig = n_schedule(w, "weekly 1 7", 0, 0)
    st = n_settings(w, cfg, DX, 0)
    read = n_sheet(w, "Read rows", "read", 2 * DX, 0)
    find = n_code(w, "Find duplicates",
                  "const cfg = $('Settings').first().json.config;\n"
                  "const norm = (v) => String(v ?? '').toLowerCase().replace(/\\s+/g, ' ').trim().replace(/^\\+?0+/, '');\n"
                  "const groups = {};\n"
                  "for (const { json: r } of $input.all()) {\n"
                  "  const key = (cfg.match_on || ['email']).map((c) => norm(r[c])).join('|');\n"
                  "  if (!key.replace(/\\|/g, '')) continue;\n"
                  "  (groups[key] = groups[key] || []).push(r.row_number);\n"
                  "}\n"
                  "const dups = Object.entries(groups).filter(([, rows]) => rows.length > 1);\n"
                  "if (!dups.length) return [];\n"
                  "return [{ json: { count: dups.length, list: dups.map(([k, rows]) => `${k}  ->  rows ${rows.join(', ')}`).join('\\n') } }];",
                  3 * DX, 0)
    mail = w.add("Email the list", "n8n-nodes-base.gmail", 2.2,
                 {"sendTo": "={{ $('Settings').first().json.config.owner_email }}",
                  "subject": "={{ $json.count }} duplicate groups in {{ $('Settings').first().json.config.sheet_tab }}",
                  "emailType": "text",
                  "message": "=These rows look like duplicates (matched on {{ $('Settings').first().json.config.match_on.join(' + ') }}):\n\n{{ $json.list }}\n\nNothing was deleted. Merge or remove them by hand.",
                  "options": {"appendAttribution": False}}, 4 * DX, 0)
    w.chain(trig, st, read, find, mail)
    setup_notes(w, spec["summary"],
                ["Open **Settings**: sheet URL, tab name, the column(s) to match on (for example `email`, or `name` + `phone`), your email.",
                 "Connect Google Sheets and Gmail.", "Run once by hand. It only reports and never deletes rows.", "Switch to **Active** for a weekly check."], y=-420)
    return w, None, needs_from(w)


def build_csv_cleaner(spec):
    w = WF(spec["slug"], spec["name"])
    cfg = {"sheet_url": SHEET_URL, "sheet_tab": "Imported", "required_columns": ["email"]}
    trig = w.add("CSV upload form", "n8n-nodes-base.formTrigger", 2.3,
                 {"formTitle": "Upload a CSV", "formDescription": "The file is cleaned and added to the Google Sheet.",
                  "formFields": {"values": [{"fieldLabel": "CSV file", "fieldType": "file", "acceptFileTypes": ".csv", "multipleFiles": False, "requiredField": True}]},
                  "options": {"appendAttribution": False, "buttonLabel": "Upload"}}, 0, 0, webhookId=uid(w.slug, "form"))
    st = n_settings(w, cfg, DX, 0)
    ext = w.add("Read the CSV", "n8n-nodes-base.extractFromFile", 1, {"binaryPropertyName": "CSV_file", "options": {}}, 2 * DX, 0)
    clean = n_code(w, "Clean the rows",
                   "const cfg = $('Settings').first().json.config;\n"
                   "const key = (k) => String(k).trim().toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '');\n"
                   "const title = (s) => s.replace(/\\s+/g, ' ').trim().toLowerCase().replace(/(^|[\\s'-])\\p{L}/gu, (m) => m.toUpperCase());\n"
                   "const seen = new Set();\n"
                   "const out = [];\n"
                   "for (const { json: raw } of $input.all()) {\n"
                   "  const r = {};\n"
                   "  for (const [k, v] of Object.entries(raw)) r[key(k)] = String(v ?? '').replace(/\\s+/g, ' ').trim();\n"
                   "  if (r.email !== undefined) { r.email = r.email.toLowerCase(); if (!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(r.email)) r.email = ''; }\n"
                   "  for (const c of ['name', 'first_name', 'last_name', 'city']) if (r[c]) r[c] = title(r[c]);\n"
                   "  if (r.phone !== undefined) r.phone = r.phone.replace(/[^\\d+]/g, '');\n"
                   "  if ((cfg.required_columns || []).some((c) => !r[c])) continue;\n"
                   "  const id = JSON.stringify(r);\n"
                   "  if (seen.has(id)) continue;\n"
                   "  seen.add(id);\n"
                   "  out.push({ json: r });\n"
                   "}\n"
                   "return out;", 3 * DX, 0)
    save = n_sheet(w, "Add to sheet", "append", 4 * DX, 0)
    w.chain(trig, st, ext, clean, save)
    setup_notes(w, spec["summary"],
                ["Make a sheet tab **Imported** whose headers match your CSV columns in lower_snake_case (for example `First Name` becomes `first_name`).",
                 "Open **Settings**: sheet URL and the columns a row must have to be kept.",
                 "Connect Google Sheets. Open the form URL from **CSV upload form** and upload a test file.",
                 "Cleans: trims spaces, lower-cases emails and drops invalid ones, title-cases names, strips phone formatting, removes exact duplicates and rows missing required columns."], y=-420)
    return w, None, needs_from(w)


# =================================================================== specs

SPECS = [
 dict(type="X", build=build_rss, mode="digest", slug="competitor-blog-monitor-ai-digest", category=C_CONTENT,
      name="Competitor blog monitor with a weekly AI digest",
      summary="Every Monday reads your competitors' blog feeds and emails a short AI summary of what they published and what it means for you.",
      feeds=["https://example-competitor.com/feed", "https://another-competitor.com/rss"], when="weekly 1 8", hours_back=168,
      prompt="You are a marketing analyst. Summarise what these competitors published this week in 5 short bullet points, then add 2 ideas for content we could publish in response. Plain text.",
      subject_prefix="Competitor digest: "),
 dict(type="X", build=build_rss, mode="alert", out="slack", slug="google-alerts-rss-to-slack", category=C_CONTENT,
      name="Google Alerts and brand mentions (RSS) to Slack",
      summary="Posts every new Google Alert (or any RSS feed) to a Slack channel, so mentions of your brand never sit unread.",
      feeds=["https://www.google.com/alerts/feeds/YOUR_ID/YOUR_FEED"], when="every 1 hours", hours_back=1,
      text="New mention: {title}\n{link}", extra=" For Google Alerts choose **Deliver to: RSS feed** and copy the feed link."),
 dict(type="X", build=build_rss, mode="digest", slug="weekly-newsletter-drafter-from-rss", category=C_CONTENT,
      name="Weekly newsletter drafter from your favourite RSS feeds",
      summary="Collects this week's posts from the feeds you follow and emails you a ready-to-edit newsletter draft with an intro and short write-ups.",
      feeds=["https://example.com/feed"], when="weekly 4 9", hours_back=168, max_items=10,
      prompt="Write a friendly weekly newsletter draft for our readers from these items: a two-sentence intro, then for each item a bold-free headline line and two sentences on why it matters. End with a one-line sign-off. Plain text.",
      subject_prefix="Newsletter draft: "),
 dict(type="X", build=build_rss, mode="per_item", slug="youtube-video-to-blog-draft", category=C_CONTENT,
      name="New YouTube video to blog post draft and social posts",
      summary="When a YouTube channel publishes a video, AI writes a blog post draft, a LinkedIn post and a tweet from the title and description, saved to a sheet.",
      feeds=["https://www.youtube.com/feeds/videos.xml?channel_id=YOUR_CHANNEL_ID"], when="every 6 hours", hours_back=6, tab="Video content",
      cols=["title", "link", "published", "blog_title", "blog_draft", "linkedin_post", "tweet", "saved_at"],
      prompt="Turn this YouTube video into written content. Use only what the title and description say; do not invent facts. Return blog_title, blog_draft (300-500 words, plain text), linkedin_post (under 120 words) and tweet (under 260 characters).",
      schema={"blog_title": "...", "blog_draft": "...", "linkedin_post": "...", "tweet": "..."}),
 dict(type="X", build=build_rss, mode="digest", slug="industry-news-daily-digest", category=C_CONTENT,
      name="Daily industry news digest (AI summary of your news feeds)",
      summary="Every morning summarises the last 24 hours from your industry news feeds into one short email: top stories and why they matter.",
      feeds=["https://example-news-site.com/rss"], when="daily 7", hours_back=24, keywords=[],
      prompt="Summarise today's industry news for a busy small-business owner: the 3-5 most important stories in one or two sentences each, and one line on why it matters. Plain text.",
      subject_prefix="Today's news: "),
 dict(type="X", build=build_rss, mode="alert", out="email", slug="rss-keyword-job-alerts", category=C_SALES,
      name="Keyword alerts from any RSS feed (jobs, tenders, listings)",
      summary="Checks RSS feeds every 30 minutes and emails you each new item that contains your keywords, for job boards, tenders, property or deal feeds.",
      feeds=["https://example-jobs.com/feed"], when="every 30 minutes", hours_back=1, keywords=["n8n", "automation"],
      subject="New match: {title}", text="{title}\n\n{snippet}\n\n{link}",
      extra=" Put the words to look for in `keywords` (any one match counts)."),
 dict(type="X", build=build_tg_faq, slug="telegram-faq-bot-from-sheet", category=C_SUPPORT,
      name="Telegram FAQ bot that answers from your Google Sheet",
      summary="A Telegram bot that answers customer questions using only the facts in your Google Sheet, and gives your phone number when it doesn't know."),
 dict(type="X", build=build_tg_alert, source="gmail", vip=["boss@example.com", "@bigclient.com"], slug="gmail-vip-alert-to-telegram", category=C_GMAIL,
      name="VIP email alert to Telegram",
      summary="When an email arrives from someone on your VIP list (or a whole company domain), you get a Telegram message with the subject and first lines."),
 dict(type="X", build=build_tg_alert, source="schedule", tab="Jobs", slug="daily-job-dispatch-telegram", category=C_LOCAL,
      name="Daily job list to each cleaner or field worker on Telegram",
      summary="Every morning sends each worker their jobs for the day (time, client, address, notes) on Telegram, from one schedule sheet."),
 dict(type="X", build=build_tg_alert, source="webhook", path="new-lead-telegram", tab="Leads", fields=["name", "email", "phone", "message"],
      text="New lead: {name}\n{phone} {email}\n\n{message}", slug="new-lead-alert-to-telegram", category=C_SALES,
      name="New website lead to Google Sheet with instant Telegram alert",
      summary="Every form submission is saved to a sheet and pinged to your Telegram straight away, so you can call while the lead is hot."),
 dict(type="X", build=build_missed_call, slug="missed-call-text-back", category=C_LOCAL,
      name="Missed call text-back (Twilio): never lose a caller",
      summary="Calls to your Twilio number ring your phone. If you don't answer, the caller instantly gets a friendly text, the call is logged and you get an email."),
 dict(type="X", build=build_sms_schedule, slug="appointment-reminder-sms", category=C_LOCAL, tab="Appointments",
      name="Appointment reminder text 24 hours before (Twilio)",
      summary="Texts each client a reminder about 24 hours before their appointment, once, from your appointments sheet. Cuts no-shows.",
      cols=["name", "phone", "appointment_at", "service", "reminder_sent"], when="every 1 hours",
      filter="!has(r.reminder_sent) && has(r.phone) && daysUntil(r.appointment_at) !== null && daysUntil(r.appointment_at) > 0 && daysUntil(r.appointment_at) <= 1",
      sms="Hi {name}, a reminder of your {service} with {cfg.business_name} on {appointment_at}. Reply C to confirm or call us to change. Reply STOP to opt out.",
      mark=("reminder_sent", "new Date().toISOString()")),
 dict(type="X", build=build_sms_schedule, slug="review-request-sms", category=C_LOCAL, tab="Jobs",
      name="Google review request by text after a finished job (Twilio)",
      summary="A day after a job is marked done, texts the customer a thank-you with your review link. Once per customer.",
      cols=["name", "phone", "status", "completed_at", "review_sms_sent"], when="daily 11", cfg={"review_link": "https://g.page/r/YOUR_ID/review"},
      filter="String(r.status).toLowerCase() === 'done' && !has(r.review_sms_sent) && has(r.phone) && daysSince(r.completed_at) !== null && daysSince(r.completed_at) >= 1 && daysSince(r.completed_at) <= 14",
      sms="Hi {name}, thanks for choosing {cfg.business_name}! If you were happy, a quick review helps us a lot: {cfg.review_link} Reply STOP to opt out.",
      mark=("review_sms_sent", "new Date().toISOString()")),
 dict(type="X", build=build_crm_intake, crm="hubspot", trigger="webhook", path="lead-to-hubspot", fields=["name", "email", "phone", "company", "message"],
      slug="website-form-to-hubspot-contact", category=C_SALES,
      name="Website form to HubSpot contact with welcome email and owner alert",
      summary="Each website enquiry creates or updates a HubSpot contact, sends the lead a thank-you email and alerts you with the details.",
      reply_subject="Thanks for getting in touch, {name}", reply_body="Hi {name},\n\nThanks for your message. We'll get back to you within one business day.\n\n{cfg.sender_name}\n{cfg.business_name}",
      alert_subject="New HubSpot lead: {name} ({company})", alert_body="{name} | {email} | {phone}\nCompany: {company}\n\n{message}"),
 dict(type="X", build=build_crm_intake, crm="hubspot", trigger="webhook", path="calendly-to-hubspot", fields=["name", "email", "event_type", "start_time"],
      slug="calendly-booking-to-hubspot", category=C_SALES,
      name="Calendly booking to HubSpot contact with prep email",
      summary="When someone books on Calendly (or Cal.com), they are added to HubSpot, get a short prep email, and you get the booking details.",
      reply_subject="See you soon, {name}", reply_body="Hi {name},\n\nThanks for booking ({event_type}, {start_time}). To make the most of it, reply with anything you'd like to cover.\n\n{cfg.sender_name}",
      alert_subject="New booking: {name}, {start_time}", alert_body="{name} ({email}) booked {event_type} for {start_time}. Contact is in HubSpot."),
 dict(type="X", build=build_crm_intake, crm="airtable", trigger="form", form_title="Get in touch", fields=["name", "email", "phone", "message"],
      slug="form-to-airtable-with-welcome-email", category=C_SALES,
      name="Form submissions to Airtable with welcome email and owner alert",
      summary="A hosted form saves every submission as an Airtable record, emails the person a welcome message and alerts you.",
      reply_subject="Thanks, {name}!", reply_body="Hi {name},\n\nThanks for reaching out. We'll reply shortly.\n\n{cfg.sender_name}",
      alert_subject="New form entry: {name}", alert_body="{name} | {email} | {phone}\n\n{message}"),
 dict(type="X", build=build_airtable_sync, slug="airtable-to-google-sheets-sync", category=C_DEV,
      name="Airtable table to Google Sheets sync (hourly)",
      summary="Copies every record of an Airtable table into a Google Sheet each hour, adding new records and updating changed ones."),
 dict(type="X", build=build_notion, source="gmail", slug="email-to-notion-task-ai", category=C_GMAIL,
      name="Emails that ask you to do something become Notion tasks (AI)",
      summary="AI reads each new email; when it asks you to do something, a task with a due date and context is created in your Notion database."),
 dict(type="X", build=build_notion, source="form", slug="meeting-notes-to-notion-ai", category=C_OPS,
      name="Meeting notes to Notion page with AI summary and action items",
      summary="Paste meeting notes or a transcript into a form. AI writes the summary, decisions and action items and saves them as a Notion page."),
 dict(type="X", build=build_drive_attachments, slug="gmail-attachments-to-google-drive", category=C_GMAIL,
      name="Save Gmail attachments to Google Drive with a log sheet",
      summary="Every attachment you receive (optionally only from chosen senders) is saved to a Drive folder with a clear name and logged in a sheet."),
 dict(type="X", build=build_drive_new_file, slug="google-drive-new-file-alert", category=C_OPS,
      name="New file in a Google Drive folder: email alert to the team",
      summary="When a client or colleague drops a file in a shared Drive folder, your team gets an email with the file name and link."),
 dict(type="X", build=build_error_alert, slug="error-alert-for-all-workflows", category=C_DEV,
      name="Error alert email for all your workflows",
      summary="Set it once as the error workflow: whenever a production workflow fails, you get an email with the workflow, the failed node, the error and a link to the run."),
 dict(type="X", build=build_dedupe, slug="google-sheet-duplicate-finder", category=C_DEV,
      name="Duplicate finder for a Google Sheet (weekly report)",
      summary="Weekly check of a contacts or leads sheet for duplicate rows (by email, or any columns you choose) and an email listing them. Never deletes anything."),
 dict(type="X", build=build_csv_cleaner, slug="csv-upload-cleaner-to-google-sheets", category=C_DEV,
      name="CSV upload cleaner to Google Sheets",
      summary="Upload a CSV through a form: headers are normalised, emails checked, names tidied, duplicates and incomplete rows dropped, and the rest appended to your sheet."),
]
