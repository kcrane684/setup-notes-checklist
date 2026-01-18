import json
import re
import sys
from typing import Dict, List

def split_list(text: str) -> List[str]:
    parts = [p.strip() for p in re.split(r"[;,]", text) if p.strip()]
    return parts

def extract_tools(text: str) -> List[str]:
    m = re.search(r"(?im)^\s*tools?\s*:\s*(.+)$", text)
    if not m:
        return []
    return split_list(m.group(1))

def extract_job_name(text: str) -> str:
    m = re.search(r"(?i)\bjob\s*([A-Za-z0-9\-]+)\b", text)
    if not m:
        return ""
    return f"Job {m.group(1)}"

def extract_material(text: str) -> str:
    m = re.search(r"(?im)^\s*material\s*[:\-]?\s*(.+)$", text)
    if m:
        return m.group(1).strip()
    m2 = re.search(r"(?i)\bmaterial\b\s+([^\n\.]+)", text)
    return m2.group(1).strip() if m2 else ""

def extract_sentences(text: str) -> List[str]:
    raw = re.split(r"[.\n]+", text)
    return [s.strip() for s in raw if s.strip()]

def classify_items(sentences: List[str]) -> Dict[str, List[str]]:
    setup_steps, inspection, risk_points = [], [], []

    for s in sentences:
        low = s.lower()

        if any(k in low for k in ["inspect", "check", "verify", "gage", "gauge", "tolerance", "+/-", "±"]):
            inspection.append(s)
            continue

        if any(k in low for k in ["watch", "risk", "chips", "burr", "crash", "tight", "careful", "coolant"]):
            risk_points.append(s)
            continue

        if any(k in low for k in ["set", "load", "install", "offset", "zero", "z0", "x0", "touch off", "bar", "collet", "puller"]):
            setup_steps.append(s)
            continue

    return {"setup_steps": setup_steps, "inspection": inspection, "risk_points": risk_points}

def generate_checklist(notes: str) -> Dict:
    def dedupe(items: List[str]) -> List[str]:
        seen, out = set(), []
        for i in items:
            key = i.strip().lower()
            if key and key not in seen:
                seen.add(key)
                out.append(i.strip())
        return out

    tools = dedupe(extract_tools(notes))
    job_name = extract_job_name(notes)
    material = extract_material(notes)

    buckets = classify_items(extract_sentences(notes))

    result = {
        "job_name": job_name,
        "material": material,
        "tools": tools,
        "setup_steps": dedupe(buckets["setup_steps"]),
        "inspection": dedupe(buckets["inspection"]),
        "risk_points": dedupe(buckets["risk_points"]),
    }

    return {k: v for k, v in result.items() if v not in ("", [], None)}

def main():
    if len(sys.argv) >= 2:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            notes = f.read()
    else:
        print("Paste your setup notes. Press Ctrl+D (or Ctrl+Z then Enter on Windows) when done:\n")
        notes = sys.stdin.read()

    print(json.dumps(generate_checklist(notes), indent=2))

if __name__ == "__main__":
    main()
