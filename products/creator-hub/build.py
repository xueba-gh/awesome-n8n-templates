"""Build all workflows from specs/*.py into workflows/NNN-slug/ and validate."""
import glob, importlib, json, os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from arch import BUILDERS
from lib import headers_csv

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "workflows")


def readme(spec, w, cols, needs):
    steps = ""
    for n in w.nodes:
        if n["name"] == "Note: setup":
            steps = n["parameters"]["content"].split("\n", 1)[1]
    lines = [f"# {spec['name']}", "", spec["summary"], "", "## What you need", ""]
    lines += [f"- {n}" for n in needs] or ["- Nothing beyond n8n"]
    lines += ["", "## Setup", "", steps, ""]
    if cols:
        lines += ["## Google Sheet columns (row 1)", "", "`" + "`, `".join(cols) + "`", ""]
    if spec.get("notes"):
        lines += ["## Good to know", "", spec["notes"], ""]
    lines += ["## About this template", "",
              "Built and checked by a new n8n creator. It uses standard n8n nodes only, has no credentials inside, and every setting you need to change sits in the **Settings** node. Test with dummy data first.",
              "", "Need help installing or customising it? Message me via my n8n Creator profile.", ""]
    return "\n".join(lines)


def check(w, spec):
    errs = []
    d = w.json()
    names = [n["name"] for n in d["nodes"]]
    if len(names) != len(set(names)): errs.append("dup names")
    for a, kinds in d["connections"].items():
        if a not in names: errs.append(f"conn from missing {a}")
        for k, outs in kinds.items():
            for o in outs:
                for c in o:
                    if c["node"] not in names: errs.append(f"conn to missing {c['node']}")
    s = json.dumps(d)
    if "credentials" in s: errs.append("credentials key present")
    for n in d["nodes"]:
        for v in json.dumps(n["parameters"]).split("{{")[1:]:
            pass
        def walk(v):
            if isinstance(v, str):
                if n["type"].endswith(".code") or "jsonOutput" in n["parameters"] and v is n["parameters"].get("jsonOutput"): return
                if v.startswith("=") and v.count("{{") != v.count("}}"): errs.append(f"unbalanced braces in {n['name']}")
                if re.search(r"\{\w+\}", v) and v.startswith("="): errs.append(f"unresolved shorthand in {n['name']}: {re.findall(r'[{]\w+[}]', v)}")
            elif isinstance(v, dict):
                for x in v.values(): walk(x)
            elif isinstance(v, list):
                for x in v: walk(x)
        walk(n["parameters"])
        if n["type"].endswith(".code"):
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
                f.write("(async function(){\n" + n["parameters"]["jsCode"] + "\n})")
            r = subprocess.run(["node", "--check", f.name], capture_output=True, text=True)
            os.unlink(f.name)
            if r.returncode: errs.append(f"JS error in {n['name']}: {r.stderr.strip()[:200]}")
    return errs


def refs(txt):
    return set(re.findall(r"(?<![\w.])\{(\w+)\}", txt or "")) - {"cfg"}


def field_check(sp, cols):
    """every {field} used in templates must exist as a column/field."""
    errs = []
    t = sp["type"]
    if t == "X":
        return []
    allowed = set(cols or [])
    texts = []
    if t == "I":
        for k in ("reply", "notify"):
            if sp.get(k): texts += [v for v in sp[k].values() if isinstance(v, str) and v not in ("gmail", "slack")]
        if sp.get("reply"): allowed.add(sp["reply"].get("to", "email")); texts.append("{" + sp["reply"].get("to", "email") + "}")
    elif t == "S":
        texts += list(sp["mail"].values()); texts.append(sp["filter"])
        allowed |= set(re.findall(r"r\.(\w+)", sp["filter"]))
        for tx in [sp["filter"]]:
            for f in re.findall(r"r\.(\w+)", tx):
                if f not in cols: errs.append(f"filter uses column {f} not in cols")
    elif t == "G":
        texts += [sp.get("alert_subject"), sp.get("alert_body")]
    elif t == "E":
        texts.append(sp["prompt"])
    elif t == "M":
        texts += [sp["alert_subject"], sp["alert_body"]]; allowed |= {"url", "detail", "checked_at"}
    for tx in texts:
        for f in refs(tx):
            if f not in allowed and not (t == "G" and f in ("subject", "from_address", "from_name", "body")):
                errs.append(f"template uses {{{f}}} not in columns")
    return errs


def main():
    specs = []
    for f in sorted(glob.glob(os.path.join(ROOT, "specs", "s*.py"))):
        mod = importlib.import_module("specs." + os.path.basename(f)[:-3])
        specs += mod.SPECS
    import shutil
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT, exist_ok=True)
    rows, bad = [], 0
    for i, sp in enumerate(specs, 1):
        sp = dict(sp); sp["slug"] = f"{i:03d}-{sp['slug']}"
        w, cols, needs = BUILDERS[sp["type"]](sp)
        errs = check(w, sp) + field_check(sp, cols)
        if errs:
            bad += 1; print("ERR", sp["slug"], errs)
        d = os.path.join(OUT, sp["slug"]); os.makedirs(d, exist_ok=True)
        json.dump(w.json(), open(os.path.join(d, "workflow.json"), "w"), indent=2, ensure_ascii=False)
        open(os.path.join(d, "README.md"), "w").write(readme(sp, w, cols, needs))
        if cols: open(os.path.join(d, "sheet-headers.csv"), "w").write(headers_csv(cols))
        rows.append((i, sp["name"], sp["category"], sp["slug"], "; ".join(needs)))
    with open(os.path.join(ROOT, "CATALOG.csv"), "w") as f:
        f.write("id,name,category,folder,needs\n")
        for r in rows: f.write(",".join('"%s"' % str(x).replace('"', "'") for x in r) + "\n")
    print(len(specs), "workflows,", bad, "with errors")


if __name__ == "__main__":
    main()
