"""Builds the FREE cut-down Creator Hub versions of the three paid products.

Each free version is derived from the paid workflow JSON: nodes are removed, a few
are rewired and adjusted, and the sticky notes are rewritten to explain what the
full version adds. Node configs that are kept are the tested ones from the paid files.

Run:  python3 build_free.py
Set SETUP_URL below once the Fiverr/Upwork listing exists, then rebuild.
"""
import json, os, copy, shutil, uuid

HERE = os.path.dirname(os.path.abspath(__file__))
PRODUCTS = os.path.abspath(os.path.join(HERE, "..", ".."))

# Where people can buy the done-for-you setup. Empty = point them to the creator profile.
SETUP_URL = ""

NS = uuid.UUID("0b8f3c52-7a61-4d0e-9e2b-5c4a1f6d8e20")


def uid(*p):
    return str(uuid.uuid5(NS, "|".join(p)))


def upsell_line():
    if SETUP_URL:
        return f"**Want it installed for you?** Done-for-you setup on your own accounts: {SETUP_URL}"
    return "**Want it installed for you?** I set up the full version on your own accounts. Message me through my n8n Creator profile."


def load(rel):
    with open(os.path.join(PRODUCTS, rel)) as f:
        return json.load(f)


def subset(w, keep, rewire, name):
    """Keep only nodes in `keep` (+ stickies added later), drop connections that touch
    removed nodes, then apply `rewire`: {src: [[targets of output 0], [output 1], ...]}."""
    nodes = [copy.deepcopy(n) for n in w["nodes"] if n["name"] in keep]
    missing = set(keep) - {n["name"] for n in nodes}
    assert not missing, missing
    conns = {}
    for a, kinds in w["connections"].items():
        if a not in keep:
            continue
        for kind, outs in kinds.items():
            new_outs = [[c for c in o if c["node"] in keep] for o in outs]
            conns.setdefault(a, {})[kind] = new_outs
    for a, outs in rewire.items():
        conns.setdefault(a, {})["main"] = [[{"node": t, "type": "main", "index": 0} for t in o] for o in outs]
    # drop empty main lists at the end
    for a in list(conns):
        for kind in list(conns[a]):
            outs = conns[a][kind]
            while outs and not outs[-1]:
                outs.pop()
            if not outs:
                del conns[a][kind]
        if not conns[a]:
            del conns[a]
    for n in nodes:  # fresh ids so the free copy never collides with the paid one
        n["id"] = uid(name, n["name"])
        if "webhookId" in n:
            n["webhookId"] = uid(name, n["name"], "hook")
    return {"name": name, "nodes": nodes, "connections": conns, "pinData": {},
            "settings": {"executionOrder": "v1"}, "meta": {"templateCredsSetupCompleted": False}, "tags": []}


def node(w, name):
    for n in w["nodes"]:
        if n["name"] == name:
            return n
    raise KeyError(name)


def set_cfg(w, cfg):
    node(w, "Settings")["parameters"]["jsonOutput"] = json.dumps({"config": cfg}, indent=2, ensure_ascii=False)


def sticky(w, name, content, x, y, wd, h, color):
    w["nodes"].append({"parameters": {"content": content, "height": h, "width": wd, "color": color},
                       "id": uid(w["name"], name), "name": name, "type": "n8n-nodes-base.stickyNote",
                       "typeVersion": 1, "position": [x, y]})


def move(w, name, x, y):
    node(w, name)["position"] = [x, y]


def check(w):
    names = {n["name"] for n in w["nodes"]}
    for a, kinds in w["connections"].items():
        assert a in names, a
        for outs in kinds.values():
            for o in outs:
                for c in o:
                    assert c["node"] in names, c
    blob = json.dumps(w)
    for n in w["nodes"]:
        assert "credentials" not in n, n["name"]
    # every $('Node') reference must exist
    import re
    for ref in set(re.findall(r"\$\('([^']+)'\)", blob)):
        assert ref in names, f"{w['name']}: missing referenced node {ref}"
    # every non-sticky node must be connected
    linked = set(w["connections"])
    for kinds in w["connections"].values():
        for outs in kinds.values():
            for o in outs:
                linked |= {c["node"] for c in o}
    for n in w["nodes"]:
        if n["type"] != "n8n-nodes-base.stickyNote":
            assert n["name"] in linked, f"{w['name']}: orphan {n['name']}"


# ---------------------------------------------------------------- 1. Speed-to-Lead Lite

def speed_to_lead():
    src = load("01-speed-to-lead/speed-to-lead.workflow.json")
    keep = ["New lead (webhook)", "New lead (built-in form)", "Settings", "Clean up lead details",
            "Has email or phone?", "Ignore: no contact details", "AI: score lead & write replies",
            "OpenAI model", "Lead reply format", "Build lead record", "Reply: has email?",
            "Reply: email the lead", "Save lead to sheet", "Hot lead?", "Email owner: hot lead"]
    w = subset(src, keep, {
        "New lead (webhook)": [["Settings"]],
        "New lead (built-in form)": [["Settings"]],
        "Settings": [["Clean up lead details"]],
        "Has email or phone?": [["AI: score lead & write replies"], ["Ignore: no contact details"]],
        "Build lead record": [["Reply: has email?", "Save lead to sheet", "Hot lead?"]],
    }, "Speed-to-Lead Lite: instant AI email reply, lead score and Google Sheets log")
    set_cfg(w, {
        "business_name": "Acme Plumbing",
        "business_type": "local plumbing company",
        "services": "Emergency repairs, leak detection, water heaters, bathroom and kitchen plumbing",
        "service_area": "Springfield and 25 miles around",
        "sender_name": "Sam at Acme Plumbing",
        "tone": "friendly, short and professional",
        "booking_link": "https://cal.com/your-business/15min",
        "owner_email": "owner@example.com",
        "default_country_code": "+1",
        "leads_sheet_url": "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit",
        "leads_sheet_tab": "Leads",
        "hot_lead_score": 8,
    })
    # email only: drop the text-message part of the prompt and schema
    ai = node(w, "AI: score lead & write replies")["parameters"]
    ai["text"] = ai["text"].replace(
        "   - sms_message: a text message under 300 characters. Use their first name if known. Thank them, show you understood their need in a few words, and invite them to book with the booking link. Sign with the sender name.\n   - email_subject and email_body: a short plain-text email with the same message, a bit more detail, the booking link on its own line, and the sender name as signature.",
        "   - email_subject and email_body: a short plain-text email. Use their first name if known. Thank them, show you understood their need in a few words, put the booking link on its own line, and sign with the sender name.")
    ai["text"] = ai["text"].replace("3. Write the first replies:", "3. Write the first reply:")
    assert "sms_message" not in ai["text"]
    node(w, "Lead reply format")["parameters"]["jsonSchemaExample"] = json.dumps({
        "score": 8, "summary": "Needs a burst pipe fixed today, ready to book.",
        "email_subject": "Your enquiry with Acme Plumbing", "email_body": "Hi Jane,\n\nThanks for getting in touch..."}, indent=2)
    code = node(w, "Build lead record")["parameters"]
    code["jsCode"] = code["jsCode"].replace("  sms_message: ai.sms_message || '',\n", "")
    code["jsCode"] = code["jsCode"].replace("  followups_sent: 0,\n  last_contact_at: new Date().toISOString(),\n  notes: '',\n",
                                            "  notes: '',\n")
    hot = node(w, "Email owner: hot lead")["parameters"]
    hot["message"] = hot["message"].replace("They have already received an automatic reply with your booking link.",
                                            "They have already received an automatic email with your booking link.")
    # layout
    for nm, x, y in [("New lead (webhook)", 0, 0), ("New lead (built-in form)", 0, 200), ("Settings", 240, 100),
                     ("Clean up lead details", 460, 100), ("Has email or phone?", 680, 100),
                     ("Ignore: no contact details", 920, 260), ("AI: score lead & write replies", 920, 60),
                     ("OpenAI model", 860, 300), ("Lead reply format", 1000, 300), ("Build lead record", 1260, 60),
                     ("Reply: has email?", 1500, -140), ("Reply: email the lead", 1740, -140),
                     ("Save lead to sheet", 1500, 60), ("Hot lead?", 1500, 260), ("Email owner: hot lead", 1740, 260)]:
        move(w, nm, x, y)
    cols = "received_at, lead_id, name, email, phone, source, message, score, temperature, summary, status, notes"
    sticky(w, "Note: start here",
           "## Speed-to-Lead Lite\nEvery new lead from your website form gets a personal AI-written email with your booking link within a minute. "
           "AI scores the lead 1-10, it is logged to Google Sheets, and you get an email when a hot lead comes in.\n\n"
           "**Setup (about 10 minutes)**\n"
           f"1. Make a Google Sheet with a tab `Leads` and these headers in row 1: {cols}\n"
           "2. Open **Settings**: business details, booking link, your email, sheet URL.\n"
           "3. Connect credentials: OpenAI, Google Sheets, Gmail (open each node once so the credential attaches).\n"
           "4. Point your website form at the **New lead (webhook)** URL, or share the built-in form's URL.\n"
           "5. Activate.", -560, -260, 500, 460, 4)
    sticky(w, "Note: full version",
           "### Full version adds\n- Text / WhatsApp reply (Twilio) as well as email\n- Follow-ups after 24h and 72h if the lead goes quiet\n"
           "- Stops follow-ups when they book (Cal.com / Calendly) or text back, and forwards replies to you\n"
           "- Duplicate check (returning leads alert you instead of a second reply)\n- Text alert to your phone on hot leads\n\n" + upsell_line(),
           1960, -160, 440, 360, 6)
    return w, "speed-to-lead-lite", "01-speed-to-lead/leads-sheet-template.csv", cols


# ---------------------------------------------------------------- 2. Support Chatbot Lite

def chatbot():
    src = load("02-ai-support-chatbot/ai-support-chatbot.workflow.json")
    keep = ["Website chat", "Settings", "Read the message", "Load FAQ sheet", "Prepare FAQ", "AI assistant",
            "OpenAI model", "Conversation memory", "Reply on website"]
    w = subset(src, keep, {"AI assistant": [["Reply on website"]]},
               "AI FAQ Chatbot Lite: website chat that answers from your Google Sheet")
    set_cfg(w, {
        "business_name": "Acme Dental",
        "assistant_name": "Ava",
        "what_we_do": "Family dental clinic: check-ups, cleaning, whitening, fillings, emergency appointments",
        "tone": "warm, clear and concise",
        "booking_link": "https://cal.com/your-business",
        "phone_for_humans": "(555) 010-0000",
        "knowledge_sheet_url": "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit",
        "knowledge_tab": "Knowledge",
    })
    rm = node(w, "Read the message")["parameters"]
    rm["jsCode"] = ("// Website chat message -> { channel, session_id, text }\n"
                    "const j = $input.first().json;\n"
                    "if (j.action && j.action !== 'sendMessage') return []; // the chat widget asking to reload an old session\n"
                    "return [{ json: { channel: 'website', session_id: 'web-' + j.sessionId, text: String(j.chatInput || '').slice(0, 2000), customer_name: '' } }];")
    sysm = node(w, "AI assistant")["parameters"]["options"]
    head, _, _ = sysm["systemMessage"].partition("HANDING OVER TO A HUMAN")
    sysm["systemMessage"] = head.rstrip() + ("\n\nIF THEY WANT A PERSON\nWhen the customer asks for a person, a call back, or a quote you can't give, "
                                             "give them the phone number above and the booking link.")
    sysm["systemMessage"] = sysm["systemMessage"].replace(
        "If the answer is not there, say you're not sure and offer to have a person get back to them.",
        "If the answer is not there, say you're not sure and give the phone number for a human.")
    node(w, "AI assistant")["parameters"]["options"]["maxIterations"] = 3
    for nm, x, y in [("Website chat", 0, 100), ("Settings", 220, 100), ("Read the message", 440, 100),
                     ("Load FAQ sheet", 660, 100), ("Prepare FAQ", 880, 100), ("AI assistant", 1120, 100),
                     ("OpenAI model", 1060, 340), ("Conversation memory", 1220, 340), ("Reply on website", 1440, 100)]:
        move(w, nm, x, y)
    sticky(w, "Note: start here",
           "## AI FAQ Chatbot Lite\nA chat page for your website that answers customer questions using only the facts in your Google Sheet, "
           "and remembers the last 12 messages of the conversation. Edit the sheet and the bot changes instantly.\n\n"
           "**Setup (about 10 minutes)**\n"
           "1. Make a Google Sheet with a tab `Knowledge` and two headers: topic, answer. Add your real hours, prices, services and policies.\n"
           "2. Open **Settings**: business name, booking link, phone number, sheet URL.\n"
           "3. Connect credentials: OpenAI, Google Sheets.\n"
           "4. Activate, open **Website chat** and copy the chat URL. Link to it from your site, or embed it.", -560, -220, 500, 420, 4)
    sticky(w, "Note: full version",
           "### Full version adds\n- WhatsApp channel (text and voice-note handling)\n- Hand-over to a human: collects name and phone/email, "
           "logs the request in a `Conversations` tab and emails you\n- Website chat-bubble embed snippet\n\n" + upsell_line(),
           1660, -60, 420, 300, 6)
    return w, "faq-chatbot-lite", "02-ai-support-chatbot/knowledge-base-template.csv", "topic, answer"


# ---------------------------------------------------------------- 3. Inbox Assistant Lite

def inbox():
    src = load("03-ai-inbox-assistant/ai-inbox-assistant.workflow.json")
    keep = ["New email", "Settings", "Prepare email", "One email at a time", "AI: triage email", "OpenAI model",
            "Triage format", "Triage result", "Get Gmail labels", "Find label", "Label exists?", "Create label",
            "Use new label", "Add label to email", "Log row", "Log to sheet", "Done"]
    w = subset(src, keep, {"Add label to email": [["Log row"]]},
               "Gmail AI Labeler Lite: auto-label, summarise and log every new email")
    set_cfg(w, {
        "your_name": "Sam Taylor",
        "your_role_and_business": "owner of Acme Plumbing, a local plumbing company",
        "label_prefix": "AI/",
        "log_sheet_url": "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit",
        "log_tab": "Inbox log",
    })
    ai = node(w, "AI: triage email")["parameters"]
    t = ai["text"]
    t = t.replace("Facts you may use in replies: {{ $('Settings').first().json.config.facts_for_replies }}\n", "")
    t = t[: t.index("- reply_draft:")].rstrip() + "\n"
    ai["text"] = t
    assert "reply_draft" not in t and "facts_for_replies" not in t and "signature" not in t, t
    node(w, "Triage format")["parameters"]["jsonSchemaExample"] = json.dumps({
        "category": "sales_lead", "urgency": "high", "needs_reply": True,
        "summary": "Wants a quote for a new water heater this week."}, indent=2)
    tr = node(w, "Triage result")["parameters"]
    tr["jsCode"] = (tr["jsCode"]
                    .replace("const needsReply = Boolean(ai.needs_reply) && !email.is_no_reply && String(ai.reply_draft || '').trim() !== '';",
                             "const needsReply = Boolean(ai.needs_reply) && !email.is_no_reply;")
                    .replace("  reply_subject: subject,\n  reply_draft: needsReply ? ai.reply_draft : '',\n  alert: category === 'sales_lead' || ai.urgency === 'high',\n", "")
                    .replace("const subject = /^re:/i.test(email.subject) ? email.subject : 'Re: ' + email.subject;\n", ""))
    assert "reply_draft" not in tr["jsCode"] and "alert" not in tr["jsCode"], tr["jsCode"]
    lr = node(w, "Log row")["parameters"]["assignments"]["assignments"]
    node(w, "Log row")["parameters"]["assignments"]["assignments"] = [a for a in lr if a["name"] != "draft_created"]
    for nm, x, y in [("Create label", 2060, 260), ("Use new label", 2280, 260), ("Log row", 2720, 100), ("Log to sheet", 2940, 100)]:
        move(w, nm, x, y)
    cols = "processed_at, from, subject, category, urgency, needs_reply, summary, message_id"
    sticky(w, "Note: start here",
           "## Gmail AI Labeler Lite\nEvery new email is read by AI, sorted into a label (AI/Sales lead, AI/Customer support, AI/Billing, AI/Newsletter...), "
           "summarised in one line and logged to a Google Sheet with its urgency and whether it needs a reply. It never sends or deletes email.\n\n"
           "**Setup (about 10 minutes)**\n"
           f"1. Make a Google Sheet with a tab `Inbox log` and these headers: {cols}\n"
           "2. Open **Settings**: your name and business, sheet URL.\n"
           "3. Connect credentials: Gmail, OpenAI, Google Sheets.\n"
           "4. Activate. Labels are created automatically the first time they're needed.", -560, -300, 500, 440, 4)
    sticky(w, "Note: full version",
           "### Full version adds\n- Reply drafts saved in Gmail Drafts, in your tone and with your facts, for you to check and send\n"
           "- Instant alert email for sales leads and urgent mail\n- Loop protection for its own alerts\n\n" + upsell_line(),
           3160, -100, 420, 280, 6)
    return w, "gmail-ai-labeler-lite", None, cols


README = """# {title}

{summary}

**Free template.** {upsell_plain}

## What it does
{what}

## What you need
{needs}

## Setup
{setup}

## Full version
{full}
"""

META = {
    "speed-to-lead-lite": dict(
        summary="Reply to every website lead within a minute with a personal AI-written email, score the lead, log it to Google Sheets and get an alert for hot leads.",
        what="- Catches leads from your website form (webhook) or a built-in n8n form\n- Cleans up names, emails and phone numbers from any form tool\n- AI scores the lead 1 to 10 and writes a short personal email with your booking link\n- Sends the email, saves the lead to Google Sheets, and emails you when the score is 8 or higher",
        needs="n8n, an OpenAI API key, a Google account (Sheets and Gmail).",
        full="- Text or WhatsApp reply via Twilio\n- Automatic follow-ups after 24 and 72 hours\n- Stops when the lead books (Cal.com / Calendly) or texts back\n- Duplicate-lead check and text alerts to your phone"),
    "faq-chatbot-lite": dict(
        summary="A website chatbot that answers customer questions only from the facts in your Google Sheet, with conversation memory.",
        what="- Hosted chat page you can link to or embed\n- Loads your FAQ sheet fresh on every message, so edits apply instantly\n- Answers in 1 to 3 sentences, in the customer's language, and never invents prices or promises\n- Gives your phone number and booking link when it doesn't know or the customer wants a person",
        needs="n8n, an OpenAI API key, a Google account (Sheets).",
        full="- WhatsApp channel\n- Hand-over to a human: collects contact details, logs the request and emails you\n- Chat-bubble embed snippet for your website"),
    "gmail-ai-labeler-lite": dict(
        summary="Auto-label every new Gmail email with AI, summarise it in one line and log it to Google Sheets.",
        what="- Reads each new email (Gmail trigger)\n- AI picks a category (sales lead, support, billing, scheduling, newsletter, notification, spam...), urgency and whether it needs a reply\n- Applies a Gmail label like AI/Sales lead, creating it the first time\n- Logs sender, subject, category, urgency and summary to a Google Sheet\n- Never sends or deletes email",
        needs="n8n, an OpenAI API key, a Google account (Gmail and Sheets).",
        full="- Reply drafts saved in Gmail for you to approve\n- Instant alerts for sales leads and urgent emails"),
}


def main():
    out_root = HERE
    built = []
    for fn in (speed_to_lead, chatbot, inbox):
        w, slug, sheet_src, cols = fn()
        check(w)
        d = os.path.join(out_root, slug)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "workflow.json"), "w") as f:
            json.dump(w, f, indent=2, ensure_ascii=False)
        with open(os.path.join(d, "sheet-headers.csv"), "w") as f:
            f.write(",".join(c.strip() for c in cols.split(",")) + "\n")
        notes = {n["name"]: n["parameters"]["content"] for n in w["nodes"] if n["type"].endswith("stickyNote")}
        setup = notes["Note: start here"].split("**Setup (about 10 minutes)**\n", 1)[1]
        m = META[slug]
        upsell_plain = upsell_line().replace("**", "")
        with open(os.path.join(d, "README.md"), "w") as f:
            f.write(README.format(title=w["name"], summary=m["summary"], upsell_plain=upsell_plain, what=m["what"],
                                  needs=m["needs"], setup=setup, full=m["full"] + "\n\n" + upsell_plain))
        built.append((slug, len(w["nodes"])))
    for s, n in built:
        print(f"{s}: {n} nodes")


if __name__ == "__main__":
    main()
