"""Archetype builders. Each returns (WF, sheet_headers_or_None, needs:list[str])."""
import json
from lib import *

SHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
DX = 240


def base_cfg(spec, uses_sheet=True, slack=False):
    cfg = {}
    if uses_sheet:
        cfg["sheet_url"] = SHEET_URL
        cfg["sheet_tab"] = spec.get("tab", "Sheet1")
    cfg["owner_email"] = "you@example.com"
    cfg["business_name"] = "Your Business"
    cfg["sender_name"] = "Your Name"
    if slack:
        cfg["slack_channel_id"] = "C0123456789"
    cfg.update(spec.get("cfg", {}))
    return cfg


def needs_from(w):
    t = {n["type"] for n in w.nodes}
    out = []
    if "n8n-nodes-base.googleSheets" in t: out.append("Google Sheets")
    if any(x.startswith("n8n-nodes-base.gmail") for x in t): out.append("Gmail")
    if "n8n-nodes-base.slack" in t: out.append("Slack")
    if "@n8n/n8n-nodes-langchain.lmChatOpenAi" in t: out.append("OpenAI API key")
    for typ, label in (("n8n-nodes-base.telegram", "Telegram bot (from @BotFather)"), ("n8n-nodes-base.twilio", "Twilio account and phone number"),
                       ("n8n-nodes-base.hubspot", "HubSpot (private app token)"), ("n8n-nodes-base.airtable", "Airtable (personal access token)"),
                       ("n8n-nodes-base.notion", "Notion (internal integration shared with the database)"), ("n8n-nodes-base.googleDrive", "Google Drive")):
        if any(x.startswith(typ) for x in t): out.append(label)
    return out


# ------------------------------------------------------------------ I
def build_I(spec):
    w = WF(spec["slug"], spec["name"])
    fields = spec["fields"]
    ai = spec.get("ai")
    reply, notify = spec.get("reply"), spec.get("notify")
    slack = bool(notify and notify.get("via") == "slack")
    cfg = base_cfg(spec, True, slack)
    x, y = 0, 0
    if spec.get("trigger", "webhook") == "form":
        trig = n_form(w, fields, spec.get("form_title", spec["name"]), x, y)
        trig_note = "Fill in the built-in form (open the form URL from the **Form** node)."
    else:
        trig = n_webhook(w, spec["slug"].split("-", 1)[-1][:40], x, y)
        trig_note = spec.get("source_note", "Send a POST request with the fields below to the **Webhook** URL (any form tool, Zapier, Make, or your own site can do this).")
    st = n_settings(w, cfg, x + DX, y)
    js = (FLATTEN +
          "const FIELDS = %s;\n"
          "return $input.all().map((item) => {\n"
          "  const { config, headers, params, query, webhookUrl, executionMode, ...rest } = item.json;\n"
          "  const d = flatten(rest.body || rest);\n"
          "  const out = { received_at: new Date().toISOString() };\n"
          "  for (const f of FIELDS) out[f] = d[f] === undefined || d[f] === null ? '' : String(d[f]).trim();\n"
          "  return { json: out };\n"
          "});" % json.dumps(fields))
    prep = n_code(w, "Clean up details", js, x + 2 * DX, y)
    w.chain(trig, st, prep)
    last = prep
    cols = ["received_at"] + fields
    px = x + 3 * DX
    if ai:
        detail = "\n".join(f"- {title(f)}: {{{{ $json.{f} || 'not given' }}}}" for f in fields)
        prompt = ai["prompt"] + "\n\nDetails received:\n" + detail
        # prompt text already uses {{ }} for details; shorthand still allowed for {cfg.x}
        node = w.add("AI: " + ai.get("label", "analyse"), "@n8n/n8n-nodes-langchain.chainLlm", 1.7,
                     {"promptType": "define", "text": "=" + re.sub(r"\{cfg\.(\w+)\}", lambda m: "{{ $('Settings').first().json.config.%s }}" % m.group(1), prompt),
                      "hasOutputParser": True}, px, y)
        m = w.add("AI model", "@n8n/n8n-nodes-langchain.lmChatOpenAi", 1.3,
                  {"model": {"__rl": True, "mode": "list", "value": "gpt-5-mini", "cachedResultName": "gpt-5-mini"},
                   "responsesApiEnabled": False, "options": {}}, px, y + 220)
        p = w.add("AI output format", "@n8n/n8n-nodes-langchain.outputParserStructured", 1.3,
                  {"jsonSchemaExample": json.dumps(ai["schema"], indent=2, ensure_ascii=False)}, px + 200, y + 220)
        w.link(m, node, "ai_languageModel")
        w.link(p, node, "ai_outputParser")
        comb = n_code(w, "Add AI results",
                      "return $input.all().map((item, i) => ({ json: { ...$('Clean up details').all()[i].json, ...item.json.output } }));",
                      px + DX, y)
        w.chain(last, node, comb)
        last = comb
        px += 2 * DX
        cols += list(ai["schema"].keys())
    save = n_sheet(w, "Save to sheet", "append", px, y)
    w.link(last, save)
    prev = save
    px += DX
    if reply:
        r = n_gmail_send(w, "Reply to them", "{" + reply.get("to", "email") + "}", reply["subject"], reply["body"], px, y, src=last)
        w.link(prev, r)
        prev = r
        px += DX
    if notify:
        if notify.get("when"):
            cond = re.sub(r"\{(\w+)\}", lambda m: "$('%s').item.json.%s" % (last, m.group(1)), notify["when"])
            iff = n_if(w, "Worth alerting?", "={{ " + cond + " }}", px, y)
            w.link(prev, iff)
            prev = iff
            px += DX
        if notify["via"] == "slack":
            nn = n_slack(w, "Alert Slack", notify["text"], px, y, src=last)
        else:
            nn = n_gmail_send(w, "Email me", "{cfg.owner_email}", notify["subject"], notify["text"], px, y, src=last)
        w.link(prev, nn, out=0)
    setup_notes(w, spec["summary"],
                ["Make a Google Sheet with a tab named **%s** and paste the header row from `sheet-headers.csv` (first row)." % cfg["sheet_tab"],
                 "Open **Settings** and fill in your sheet URL, email and names.",
                 "Connect your accounts on every node with a warning (Google Sheets" + (", Gmail" if (reply or (notify and notify['via'] == 'gmail')) else "") + (", Slack" if slack else "") + (", OpenAI" if ai else "") + ").",
                 trig_note,
                 "Click **Execute workflow**, send a test, then switch the workflow to **Active**."],
                y=-400)
    return w, cols, needs_from(w)


# ------------------------------------------------------------------ S
def build_S(spec):
    w = WF(spec["slug"], spec["name"])
    cfg = base_cfg(spec, True, False)
    x, y = 0, 0
    trig = n_schedule(w, spec.get("when", "daily 9"), x, y)
    st = n_settings(w, cfg, x + DX, y)
    read = n_sheet(w, "Read rows", "read", x + 2 * DX, y)
    helpers = ("const daysSince = (v) => { const t = Date.parse(v); return isNaN(t) ? null : (Date.now() - t) / 86400000; };\n"
               "const daysUntil = (v) => { const t = Date.parse(v); return isNaN(t) ? null : (t - Date.now()) / 86400000; };\n"
               "const has = (v) => v !== undefined && v !== null && String(v).trim() !== '';\n"
               "const cfg = $('Settings').first().json.config;\n")
    find = n_code(w, "Find rows to act on",
                  helpers + "return $input.all().filter((item) => {\n  const r = item.json;\n  return (%s);\n}).slice(0, %d);" % (spec["filter"], spec.get("limit", 50)),
                  x + 3 * DX, y)
    mail = spec["mail"]
    send = n_gmail_send(w, "Send email", mail.get("to", "{email}"), mail["subject"], mail["body"], x + 4 * DX, y)
    w.chain(trig, st, read, find, send)
    cols = list(spec["cols"])
    if spec.get("mark"):
        col, val = spec["mark"]
        if col not in cols: cols.append(col)
        mk = n_code(w, "Mark rows as done",
                    "const stamp = %s;\nreturn $('Find rows to act on').all().map((item) => ({ json: { row_number: item.json.row_number, %s: stamp } }));" % (val, json.dumps(col)),
                    x + 5 * DX, y)
        upd = n_sheet(w, "Update rows", "update", x + 6 * DX, y, match=["row_number"])
        w.chain(send, mk, upd)
    setup_notes(w, spec["summary"],
                ["Use a Google Sheet with a tab named **%s** and these headers in row 1: see `sheet-headers.csv`." % cfg["sheet_tab"],
                 "Open **Settings** and fill in your sheet URL, your email and names.",
                 "Connect Google Sheets and Gmail on the nodes with warnings.",
                 "Check the rule in **Find rows to act on** (it shows exactly which rows get an email) and the wording in **Send email**.",
                 "Run it once by hand with a test row, then switch the workflow to **Active**."],
                y=-400)
    return w, cols, needs_from(w)


# ------------------------------------------------------------------ D
def build_D(spec):
    w = WF(spec["slug"], spec["name"])
    cfg = base_cfg(spec, True, False)
    x, y = 0, 0
    trig = n_schedule(w, spec.get("when", "weekly 1 8"), x, y)
    st = n_settings(w, cfg, x + DX, y)
    read = n_sheet(w, "Read rows", "read", x + 2 * DX, y)
    summ = n_code(w, "Prepare the rows",
                  "const cfg = $('Settings').first().json.config;\n"
                  "const rows = $input.all().map((i) => i.json).filter((r) => (%s)).slice(0, 150);\n"
                  "const text = rows.map((r) => Object.entries(r).filter(([k]) => k !== 'row_number').map(([k, v]) => k + ': ' + v).join(' | ')).join('\\n');\n"
                  "return [{ json: { count: rows.length, rows_text: text || 'No rows.' } }];" % spec.get("filter", "true"),
                  x + 3 * DX, y)
    prompt = spec["prompt"] + "\n\nNumber of rows: {{ $json.count }}\nRows:\n{{ $json.rows_text }}"
    ai = w.add("AI: write the summary", "@n8n/n8n-nodes-langchain.chainLlm", 1.7,
               {"promptType": "define", "text": "=" + re.sub(r"\{cfg\.(\w+)\}", lambda m: "{{ $('Settings').first().json.config.%s }}" % m.group(1), prompt),
                "hasOutputParser": True}, x + 4 * DX, y)
    m = w.add("AI model", "@n8n/n8n-nodes-langchain.lmChatOpenAi", 1.3,
              {"model": {"__rl": True, "mode": "list", "value": "gpt-5-mini", "cachedResultName": "gpt-5-mini"},
               "responsesApiEnabled": False, "options": {}}, x + 4 * DX, y + 220)
    p = w.add("AI output format", "@n8n/n8n-nodes-langchain.outputParserStructured", 1.3,
              {"jsonSchemaExample": json.dumps({"headline": "Short subject line", "summary": "Two or three sentences.", "actions": "- First action\n- Second action"}, indent=2)},
              x + 4 * DX + 200, y + 220)
    w.link(m, ai, "ai_languageModel"); w.link(p, ai, "ai_outputParser")
    send = w.add("Email the summary", "n8n-nodes-base.gmail", 2.2,
                 {"sendTo": "={{ $('Settings').first().json.config.owner_email }}",
                  "subject": "=" + spec.get("subject_prefix", "") + "{{ $json.output.headline }}",
                  "emailType": "text",
                  "message": "={{ $json.output.summary }}\n\nWhat to do next:\n{{ $json.output.actions }}\n\n(Based on {{ $('Prepare the rows').first().json.count }} rows from your sheet.)",
                  "options": {"appendAttribution": False}}, x + 5 * DX, y)
    w.chain(trig, st, read, summ, ai, send)
    setup_notes(w, spec["summary"],
                ["Use a Google Sheet with a tab named **%s** and these headers in row 1 (see `sheet-headers.csv`)." % cfg["sheet_tab"],
                 "Open **Settings**: sheet URL and the email that should receive the summary.",
                 "Connect Google Sheets, Gmail and OpenAI on the nodes with warnings.",
                 "Run once by hand to see the email, then switch the workflow to **Active** (it runs on the schedule in the first node)."],
                y=-400)
    return w, list(spec["cols"]), needs_from(w)


# ------------------------------------------------------------------ G
def build_G(spec):
    w = WF(spec["slug"], spec["name"])
    cfg = base_cfg(spec, True, False)
    x, y = 0, 0
    trig = w.add("New email", "n8n-nodes-base.gmailTrigger", 1.3,
                 {"pollTimes": {"item": [{"mode": "everyMinute"}]}, "simple": False,
                  "filters": {"q": spec.get("query", "in:inbox -from:me"), "readStatus": "unread"}, "options": {}}, x, y)
    st = n_settings(w, cfg, x + DX, y)
    prep = n_code(w, "Read the email",
                  "return $input.all().map((i) => {\n"
                  "  const j = i.json;\n"
                  "  const from = (j.from && j.from.value && j.from.value[0]) ? j.from.value[0] : {};\n"
                  "  return { json: {\n"
                  "    message_id: j.id, thread_id: j.threadId,\n"
                  "    from_address: from.address || String(j.from || ''), from_name: from.name || '',\n"
                  "    subject: j.subject || '', body: String(j.text || j.snippet || '').slice(0, 4000),\n"
                  "    received_at: new Date().toISOString(),\n"
                  "  } };\n"
                  "});", x + 2 * DX, y)
    prompt = spec["prompt"] + "\n\nEmail:\nFrom: {{ $json.from_name }} <{{ $json.from_address }}>\nSubject: {{ $json.subject }}\n\n{{ $json.body }}"
    ai = w.add("AI: read the email", "@n8n/n8n-nodes-langchain.chainLlm", 1.7,
               {"promptType": "define", "text": "=" + re.sub(r"\{cfg\.(\w+)\}", lambda m: "{{ $('Settings').first().json.config.%s }}" % m.group(1), prompt),
                "hasOutputParser": True}, x + 3 * DX, y)
    m = w.add("AI model", "@n8n/n8n-nodes-langchain.lmChatOpenAi", 1.3,
              {"model": {"__rl": True, "mode": "list", "value": "gpt-5-mini", "cachedResultName": "gpt-5-mini"},
               "responsesApiEnabled": False, "options": {}}, x + 3 * DX, y + 260)
    p = w.add("AI output format", "@n8n/n8n-nodes-langchain.outputParserStructured", 1.3,
              {"jsonSchemaExample": json.dumps(spec["schema"], indent=2, ensure_ascii=False)}, x + 3 * DX + 200, y + 260)
    w.link(m, ai, "ai_languageModel"); w.link(p, ai, "ai_outputParser")
    comb = n_code(w, "Combine",
                  "return $input.all().map((item, i) => ({ json: { ...$('Read the email').all()[i].json, ...item.json.output } }));",
                  x + 4 * DX, y)
    w.chain(trig, st, prep, ai, comb)
    cols = ["received_at", "from_address", "subject", "message_id"] + list(spec["schema"].keys())
    log = n_sheet(w, "Log to sheet", "append", x + 5 * DX, y + 160)
    w.link(comb, log)
    alert_js = spec.get("alert_when")
    if alert_js:
        flag = n_code(w, "Needs an alert?",
                      "return $input.all().map((i) => { const r = i.json; return { json: { ...r, alert: Boolean(%s) } }; });" % alert_js,
                      x + 5 * DX, y - 160)
        iff = n_if(w, "Alert?", "={{ $json.alert }}", x + 6 * DX, y - 160)
        a = n_gmail_send(w, "Email me an alert", "{cfg.owner_email}", spec["alert_subject"], spec["alert_body"], x + 7 * DX, y - 240)
        w.link(comb, flag); w.link(flag, iff); w.link(iff, a, out=0)
    if spec.get("draft"):
        d_if = n_if(w, "Reply needed?", "={{ $json.needs_reply }}", x + 5 * DX, y + 340)
        dr = w.add("Save reply as draft", "n8n-nodes-base.gmail", 2.2,
                   {"resource": "draft", "operation": "create", "subject": "=Re: {{ $json.subject }}",
                    "emailType": "text", "message": "={{ $json.%s }}" % spec["draft"],
                    "options": {"threadId": "={{ $json.thread_id }}", "sendTo": "={{ $json.from_address }}"}},
                   x + 6 * DX, y + 340)
        w.link(comb, d_if); w.link(d_if, dr, out=0)
    setup_notes(w, spec["summary"],
                ["Make a Google Sheet with a tab named **%s** and paste the header row from `sheet-headers.csv`." % cfg["sheet_tab"],
                 "Open **Settings**: sheet URL and your email.",
                 "Connect Gmail (trigger and any Gmail node), Google Sheets and OpenAI on the nodes with warnings.",
                 "The trigger checks unread mail matching `%s` every minute. Change that search in **New email** to match your inbox." % spec.get("query", "in:inbox -from:me"),
                 "Send yourself a test from another address, check the result, then switch to **Active**. Nothing is ever sent to customers: replies are saved as drafts." if spec.get("draft") else "Send yourself a test from another address, check the result, then switch to **Active**."],
                y=-560)
    return w, cols, needs_from(w)


# ------------------------------------------------------------------ M
def build_M(spec):
    w = WF(spec["slug"], spec["name"])
    kind = spec["kind"]
    cfg = {"owner_email": "you@example.com", "urls": spec.get("urls", ["https://example.com"])}
    cfg.update(spec.get("cfg", {}))
    x, y = 0, 0
    trig = n_schedule(w, spec.get("when", "every 5 minutes"), x, y)
    st = n_settings(w, cfg, x + DX, y)
    lst = n_code(w, "List what to check",
                 "return $('Settings').first().json.config.urls.map((url) => ({ json: { url } }));", x + 2 * DX, y)
    http = w.add("Fetch the page", "n8n-nodes-base.httpRequest", 4.2,
                 {"url": "={{ $json.url }}",
                  "options": {"timeout": 20000, "response": {"response": {"fullResponse": True, "neverError": True, "responseFormat": "text"}}}},
                 x + 3 * DX, y, onError="continueRegularOutput")
    ev = {
        "uptime": ("const code = Number($json.statusCode || 0);\n"
                   "const problem = !(code >= 200 && code < 400);\n"
                   "const detail = problem ? 'Status ' + (code || 'no answer') : 'OK';"),
        "keyword": ("const body = String($json.body || $json.data || '');\n"
                    "const kw = String(cfg.keyword || '').toLowerCase();\n"
                    "const found = body.toLowerCase().includes(kw);\n"
                    "const problem = cfg.alert_when_found ? found : !found;\n"
                    "const detail = found ? 'Found \"' + cfg.keyword + '\" on the page' : 'Did not find \"' + cfg.keyword + '\" on the page';"),
        "price": ("const body = String($json.body || $json.data || '');\n"
                  "const m = body.match(new RegExp(cfg.price_regex));\n"
                  "const price = m ? parseFloat(String(m[1]).replace(/,/g, '')) : null;\n"
                  "const problem = price !== null && price <= Number(cfg.target_price);\n"
                  "const detail = price === null ? 'Could not read the price' : 'Price is ' + price + ' (target ' + cfg.target_price + ')';"),
    }[kind]
    if kind == "keyword":
        cfg.setdefault("keyword", spec.get("keyword", "In stock")); cfg.setdefault("alert_when_found", spec.get("alert_when_found", False))
    if kind == "price":
        cfg.setdefault("price_regex", spec.get("price_regex", "\\$\\s?([0-9][0-9,]*\\.?[0-9]*)")); cfg.setdefault("target_price", spec.get("target_price", 100))
    # settings node was created with older cfg; rebuild its params
    for n in w.nodes:
        if n["name"] == "Settings":
            n["parameters"]["jsonOutput"] = json.dumps({"config": cfg}, indent=2)
    evn = n_code(w, "Judge the result",
                 "const cfg = $('Settings').first().json.config;\n"
                 "return $input.all().map((item, i) => {\n"
                 "  const $json = item.json;\n"
                 "  const url = $('List what to check').all()[i].json.url;\n"
                 "  " + ev.replace("\n", "\n  ") + "\n"
                 "  return { json: { url, problem, detail, checked_at: new Date().toISOString() } };\n"
                 "});", x + 4 * DX, y)
    iff = n_if(w, "Problem found?", "={{ $json.problem }}", x + 5 * DX, y)
    al = n_gmail_send(w, "Email me the alert", "{cfg.owner_email}", spec["alert_subject"], spec["alert_body"], x + 6 * DX, y - 100)
    w.chain(trig, st, lst, http, evn, iff)
    w.link(iff, al, out=0)
    setup_notes(w, spec["summary"],
                ["Open **Settings** and list the addresses to check (and your email)." + spec.get("extra_setting", ""),
                 "Connect Gmail on **Email me the alert**.",
                 "Run it once by hand, look at **Judge the result** to see what it found, then switch to **Active**.",
                 "It only emails you when something is wrong, so a quiet inbox means all is well."],
                y=-420)
    return w, None, needs_from(w)


# ------------------------------------------------------------------ E
def build_E(spec):
    w = WF(spec["slug"], spec["name"])
    cfg = base_cfg(spec, True, False)
    cfg["rows_per_run"] = spec.get("limit", 20)
    x, y = 0, 0
    trig = n_schedule(w, spec.get("when", "every 6 hours"), x, y)
    st = n_settings(w, cfg, x + DX, y)
    read = n_sheet(w, "Read rows", "read", x + 2 * DX, y)
    need = spec["need"]  # input columns that must be filled
    fill = list(spec["schema"].keys())
    find = n_code(w, "Find rows to fill in",
                  "const cfg = $('Settings').first().json.config;\n"
                  "const has = (v) => v !== undefined && v !== null && String(v).trim() !== '';\n"
                  "return $input.all().filter((i) => %s && !has(i.json[%s])).slice(0, Number(cfg.rows_per_run));" %
                  (" && ".join("has(i.json.%s)" % c for c in need), json.dumps(fill[0])), x + 3 * DX, y)
    ai = w.add("AI: fill in the row", "@n8n/n8n-nodes-langchain.chainLlm", 1.7,
               {"promptType": "define", "text": ex(spec["prompt"]), "hasOutputParser": True}, x + 4 * DX, y)
    m = w.add("AI model", "@n8n/n8n-nodes-langchain.lmChatOpenAi", 1.3,
              {"model": {"__rl": True, "mode": "list", "value": "gpt-5-mini", "cachedResultName": "gpt-5-mini"},
               "responsesApiEnabled": False, "options": {}}, x + 4 * DX, y + 220)
    p = w.add("AI output format", "@n8n/n8n-nodes-langchain.outputParserStructured", 1.3,
              {"jsonSchemaExample": json.dumps(spec["schema"], indent=2, ensure_ascii=False)}, x + 4 * DX + 200, y + 220)
    w.link(m, ai, "ai_languageModel"); w.link(p, ai, "ai_outputParser")
    comb = n_code(w, "Match results to rows",
                  "return $input.all().map((item, i) => ({ json: { row_number: $('Find rows to fill in').all()[i].json.row_number, ...item.json.output } }));",
                  x + 5 * DX, y)
    upd = n_sheet(w, "Write back to the sheet", "update", x + 6 * DX, y, match=["row_number"])
    w.chain(trig, st, read, find, ai, comb, upd)
    cols = list(spec["cols"])
    for c in fill:
        if c not in cols: cols.append(c)
    setup_notes(w, spec["summary"],
                ["Use a Google Sheet with a tab named **%s** and these headers in row 1 (see `sheet-headers.csv`)." % cfg["sheet_tab"],
                 "Fill the input columns (%s). Leave %s empty: the AI fills it." % (", ".join(need), ", ".join(fill)),
                 "Open **Settings**: sheet URL and how many rows to process per run.",
                 "Connect Google Sheets and OpenAI on the nodes with warnings.",
                 "Run once by hand, check the results, then switch to **Active**. It only touches rows where %s is empty." % fill[0]],
                y=-400)
    return w, cols, needs_from(w)


BUILDERS = {"I": build_I, "S": build_S, "D": build_D, "G": build_G, "M": build_M, "E": build_E,
            "X": lambda spec: spec["build"](spec)}
