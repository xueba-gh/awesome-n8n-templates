"""Builds n8n workflow JSON from compact specs. Six archetypes:
  I  intake / event hook  (webhook or form -> clean -> optional AI -> sheet -> emails/alerts)
  S  scheduled reminder   (schedule -> read sheet -> filter -> email -> mark row)
  D  digest               (schedule -> read sheet -> AI summary -> email)
  G  gmail + AI           (Gmail trigger -> AI -> alert / draft -> log)
  M  monitor              (schedule -> HTTP check -> alert if bad)
  E  enrich rows          (schedule/manual -> read sheet -> rows missing X -> AI -> write back)
No credentials are ever written into the JSON.
"""
import json, re, uuid, os

NS = uuid.UUID("6f1c2a7e-9d34-4b8e-a1c5-3e2d7f9b0a11")


def uid(*parts):
    return str(uuid.uuid5(NS, "|".join(parts)))


def sx(s, src=None):
    """Shorthand -> n8n expression text. {cfg.x} -> Settings config, {field} -> $json.field
    (or $('src').item.json.field when src is given)."""
    if s is None:
        return s
    s = re.sub(r"\{cfg\.(\w+)\}", lambda m: "{{ $('Settings').first().json.config.%s }}" % m.group(1), s)
    if src:
        s = re.sub(r"\{(\w+)\}", lambda m: "{{ $('%s').item.json.%s }}" % (src, m.group(1)), s)
    else:
        s = re.sub(r"\{(\w+)\}", lambda m: "{{ $json.%s }}" % m.group(1), s)
    return s


def ex(s, src=None):
    return "=" + sx(s, src)


def title(s):
    return s.replace("_", " ").strip().capitalize()


class WF:
    def __init__(self, slug, name):
        self.slug, self.name = slug, name
        self.nodes, self.conns = [], {}
        self.names = set()

    def add(self, name, type_, tv, params, x, y, **extra):
        assert name not in self.names, f"duplicate node name {name} in {self.slug}"
        self.names.add(name)
        n = {"parameters": params, "id": uid(self.slug, name), "name": name, "type": type_,
             "typeVersion": tv, "position": [x, y]}
        n.update(extra)
        self.nodes.append(n)
        return name

    def link(self, a, b, kind="main", out=0):
        self.conns.setdefault(a, {}).setdefault(kind, [])
        lst = self.conns[a][kind]
        while len(lst) <= out:
            lst.append([])
        lst[out].append({"node": b, "type": kind, "index": 0})

    def chain(self, *names):
        for a, b in zip(names, names[1:]):
            self.link(a, b)

    def sticky(self, name, content, x, y, w=420, h=240, color=4):
        self.add(name, "n8n-nodes-base.stickyNote", 1,
                 {"content": content, "height": h, "width": w, "color": color}, x, y)

    def json(self):
        return {"name": self.name, "nodes": self.nodes, "connections": self.conns, "pinData": {},
                "settings": {"executionOrder": "v1"}, "meta": {"templateCredsSetupCompleted": False},
                "tags": []}


# ---------- node builders ----------

def n_settings(w, cfg, x, y):
    return w.add("Settings", "n8n-nodes-base.set", 3.4,
                 {"mode": "raw", "jsonOutput": json.dumps({"config": cfg}, indent=2, ensure_ascii=False),
                  "includeOtherFields": True, "options": {}}, x, y)


def n_webhook(w, path, x, y):
    return w.add("Webhook", "n8n-nodes-base.webhook", 2.1,
                 {"httpMethod": "POST", "path": path, "responseMode": "onReceived",
                  "options": {"responseData": "{\"ok\":true}"}}, x, y,
                 webhookId=uid(w.slug, "webhook"))


def n_form(w, fields, ftitle, x, y):
    vals = []
    for f in fields:
        v = {"fieldLabel": title(f), "requiredField": f in ("name", "email")}
        if f == "email":
            v["fieldType"] = "email"
        elif f in ("message", "notes", "description", "details", "feedback", "reason", "summary"):
            v["fieldType"] = "textarea"
        vals.append(v)
    return w.add("Form", "n8n-nodes-base.formTrigger", 2.3,
                 {"formTitle": ftitle, "formDescription": "Fill in the form and we'll be in touch.",
                  "formFields": {"values": vals},
                  "options": {"appendAttribution": False, "buttonLabel": "Send"}}, x, y,
                 webhookId=uid(w.slug, "form"))


def n_schedule(w, when, x, y):
    """when: 'every N minutes' | 'every N hours' | 'daily H' | 'weekly D H' (D=0..6, 0=Sunday)."""
    m = re.match(r"every (\d+) minutes", when)
    if m:
        rule = {"interval": [{"field": "minutes", "minutesInterval": int(m.group(1))}]}
    elif (m := re.match(r"every (\d+) hours", when)):
        rule = {"interval": [{"field": "hours", "hoursInterval": int(m.group(1))}]}
    elif (m := re.match(r"daily (\d+)", when)):
        rule = {"interval": [{"field": "days", "daysInterval": 1, "triggerAtHour": int(m.group(1))}]}
    elif (m := re.match(r"weekly (\d) (\d+)", when)):
        rule = {"interval": [{"field": "weeks", "weeksInterval": 1, "triggerAtDay": [int(m.group(1))],
                              "triggerAtHour": int(m.group(2))}]}
    else:
        raise ValueError(when)
    return w.add("Schedule", "n8n-nodes-base.scheduleTrigger", 1.2, {"rule": rule}, x, y)


def n_code(w, name, js, x, y):
    return w.add(name, "n8n-nodes-base.code", 2, {"jsCode": js}, x, y)


def n_if(w, name, left_expr, x, y):
    return w.add(name, "n8n-nodes-base.if", 2.2,
                 {"conditions": {"options": {"caseSensitive": True, "leftValue": "", "typeValidation": "loose", "version": 2},
                                 "conditions": [{"id": uid(w.slug, name, "c"), "leftValue": left_expr,
                                                 "operator": {"type": "boolean", "operation": "true", "singleValue": True},
                                                 "rightValue": ""}], "combinator": "and"},
                  "looseTypeValidation": True, "options": {}}, x, y)


def sheet_ref():
    return ({"__rl": True, "mode": "url", "value": "={{ $('Settings').first().json.config.sheet_url }}"},
            {"__rl": True, "mode": "name", "value": "={{ $('Settings').first().json.config.sheet_tab }}"})


def n_sheet(w, name, op, x, y, match=None, tab_key="sheet_tab"):
    doc, sheet = sheet_ref()
    sheet["value"] = "={{ $('Settings').first().json.config.%s }}" % tab_key
    p = {"operation": op, "documentId": doc, "sheetName": sheet}
    if op in ("append", "update"):
        p["columns"] = {"mappingMode": "autoMapInputData", "value": {}, "matchingColumns": match or [], "schema": []}
        p["options"] = {"cellFormat": "RAW", "handlingExtraData": "ignoreIt"}
    else:
        p["options"] = {}
    kw = {"alwaysOutputData": True} if op == "read" else {}
    return w.add(name, "n8n-nodes-base.googleSheets", 4.7, p, x, y, **kw)


def n_gmail_send(w, name, to, subject, body, x, y, src=None):
    return w.add(name, "n8n-nodes-base.gmail", 2.2,
                 {"sendTo": ex(to, src), "subject": ex(subject, src), "emailType": "text", "message": ex(body, src),
                  "options": {"appendAttribution": False}}, x, y)


def n_slack(w, name, text, x, y, src=None):
    return w.add(name, "n8n-nodes-base.slack", 2.3,
                 {"select": "channel",
                  "channelId": {"__rl": True, "mode": "id",
                                "value": "={{ $('Settings').first().json.config.slack_channel_id }}"},
                  "text": ex(text, src), "otherOptions": {}}, x, y)


def n_ai(w, name, prompt, schema, x, y):
    """AI chain + OpenAI model + structured output parser. Returns the chain node name."""
    ai = w.add(name, "@n8n/n8n-nodes-langchain.chainLlm", 1.7,
               {"promptType": "define", "text": ex(prompt), "hasOutputParser": True}, x, y)
    m = w.add(name + " model", "@n8n/n8n-nodes-langchain.lmChatOpenAi", 1.3,
              {"model": {"__rl": True, "mode": "list", "value": "gpt-5-mini", "cachedResultName": "gpt-5-mini"},
               "responsesApiEnabled": False, "options": {}}, x, y + 220)
    p = w.add(name + " format", "@n8n/n8n-nodes-langchain.outputParserStructured", 1.3,
              {"jsonSchemaExample": json.dumps(schema, indent=2, ensure_ascii=False)}, x + 200, y + 220)
    w.link(m, ai, "ai_languageModel")
    w.link(p, ai, "ai_outputParser")
    return ai


FLATTEN = ("const key = (k) => String(k).toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '');\n"
           "function flatten(o, into = {}) {\n"
           "  for (const [k, v] of Object.entries(o || {})) {\n"
           "    if (v && typeof v === 'object' && !Array.isArray(v)) flatten(v, into);\n"
           "    else if (!(key(k) in into)) into[key(k)] = v;\n"
           "  }\n  return into;\n}\n")


def js_str(s):
    return json.dumps(s, ensure_ascii=False)


def setup_notes(w, summary, steps, x=-60, y=-420, extra=""):
    w.sticky("Note: what this does", "## " + w.name + "\n" + summary, x, y, 420, 300, 4)
    body = "## Setup (about 10 minutes)\n" + "\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1))
    if extra:
        body += "\n\n" + extra
    w.sticky("Note: setup", body, x + 460, y, 480, 300, 7)


def headers_csv(cols):
    return ",".join(cols) + "\n"
