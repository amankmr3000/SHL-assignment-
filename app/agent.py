import re
from typing import Any, Dict, List
from .models import Message
from .retriever import Retriever

ROLE_SIGNALS = {
    "java","python","developer","engineer","software","swe","sales","finance","graduate",
    "admin","assistant","contact","customer","leadership","manager","executive","rust",
    "network","healthcare","nurse","accounting","data","front","backend","full-stack",
    "full stack","sql","aws","excel","word","safety","coding","cognitive","personality",
    "situational","spring","docker","analyst","call center","support"
}

VAGUE_WORDS = {"assessment","test","hire","hiring","recruit","candidate","role","solution"}
OFF_TOPIC = {"weather","cricket","football","stock","dating","joke","resume","salary","roadmap","movie"}

def norm(s: str) -> str:
    return re.sub(r"\s+", " ", str(s).lower()).strip()

def all_user(messages: List[Message]) -> str:
    return "\n".join(m.content for m in messages if m.role == "user")

def latest_user(messages: List[Message]) -> str:
    return next((m.content for m in reversed(messages) if m.role == "user"), "")

def refuse(t: str) -> bool:
    s = norm(t)
    if any(x in s for x in ["ignore previous", "system prompt", "developer message", "prompt injection", "reveal prompt"]):
        return True
    if any(x in s for x in ["legal advice", "lawsuit", "law 144", "regulatory compliance", "fire an employee", "terminate employee"]):
        return True
    if any(x in s for x in OFF_TOPIC) and not any(x in s for x in ["assessment", "shl", "test"]):
        return True
    return False

def vague(ctx: str) -> bool:
    s = norm(ctx)
    toks = set(re.findall(r"[a-z0-9#+.-]+", s))
    return bool(toks & VAGUE_WORDS) and not any(x in s for x in ROLE_SIGNALS) and len(toks) < 22

def compare(t: str) -> bool:
    s = norm(t)
    return any(x in s for x in ["compare", "difference", " vs ", "versus", "different from"])

def wants_personality(ctx: str) -> bool:
    s = norm(ctx)
    return any(x in s for x in ["personality", "behavior", "behaviour", "opq", "leadership", "culture fit"])

def include_personality(ctx: str) -> bool:
    s = norm(ctx)
    return not any(x in s for x in ["without personality", "skip personality", "remove personality", "drop personality", "remove opq", "drop opq", "skip opq", "no personality"])

def wants_cognitive(ctx: str) -> bool:
    s = norm(ctx)
    return any(x in s for x in ["cognitive", "ability", "aptitude", "reasoning", "numerical", "verbal", "logical", "g+"] )

def wants_shorter(ctx: str) -> bool:
    s = norm(ctx)
    return any(x in s for x in ["shorter", "short test", "less time", "quick", "under 20", "under 30", "fast"])

def seniority(ctx: str) -> str:
    s = norm(ctx)
    if any(x in s for x in ["intern", "entry", "entry-level", "junior", "graduate", "fresh"]):
        return "junior"
    if any(x in s for x in ["senior", "lead", "principal", "architect", "manager", "executive", "director"]):
        return "senior"
    if any(x in s for x in ["mid", "middle", "3 years", "4 years", "5 years"]):
        return "mid"
    return ""

def exclusions(ctx: str) -> List[str]:
    s, ex = norm(ctx), []
    if any(x in s for x in ["remove opq", "drop opq", "skip opq", "without personality", "no personality"]):
        ex += ["opq", "occupational personality"]
    if any(x in s for x in ["remove verify", "drop verify"]):
        ex += ["verify"]
    if any(x in s for x in ["remove coding", "no coding"]):
        ex += ["automata", "coding", "programming"]
    return ex

def payload(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    total = max(len(items), 1)
    for i, x in enumerate(items[:10]):
        conf = max(55, 99 - i * 5)
        out.append({
            "name": x["name"],
            "url": x["url"],
            "test_type": x.get("test_type", "K"),
            "confidence": conf
        })
    return out

def find_exact(catalog: List[Dict[str, Any]], name: str):
    for x in catalog:
        if x["name"].lower() == name.lower():
            return x
    return None

def family_name(item: Dict[str, Any]) -> str:
    n = item["name"].lower()
    if "sql" in n:
        return "sql"
    if "java" in n:
        return "java"
    if "opq" in n or "personality" in n:
        return "personality"
    if "verify" in n:
        return "verify"
    if "microsoft excel" in n or n.startswith("excel"):
        return "excel"
    if "microsoft word" in n or n.startswith("word"):
        return "word"
    if "automata" in n:
        return "automata"
    return re.sub(r"\(.*?\)", "", n).strip()

def diversify(items: List[Dict[str, Any]], max_items: int = 10) -> List[Dict[str, Any]]:
    out, seen_url, seen_family = [], set(), set()

    for it in items:
        u = it["url"]
        fam = family_name(it)
        if u in seen_url:
            continue
        if fam in seen_family and len(out) < 8:
            continue
        seen_url.add(u)
        seen_family.add(fam)
        out.append(it)
        if len(out) >= max_items:
            return out

    for it in items:
        if it["url"] not in seen_url:
            out.append(it)
            seen_url.add(it["url"])
        if len(out) >= max_items:
            break

    return out[:max_items]

def role_pack(ctx: str) -> List[str]:
    s = norm(ctx)
    level = seniority(ctx)
    wanted = []

    if "java" in s or "backend" in s or "spring" in s:
        wanted += [
            "Core Java (Advanced Level) (New)" if level != "junior" else "Core Java (Entry Level) (New)",
            "Spring (New)",
            "Amazon Web Services (AWS) Development (New)",
            "Docker (New)",
            "Automata (New)",
            "SQL (New)",
        ]

    if "full stack" in s or "full-stack" in s or "frontend" in s or "front end" in s:
        wanted += ["Automata Front End", "Angular 6 (New)", "JavaScript (New)", "HTML/CSS (New)"]

    if "rust" in s or "systems" in s or "linux" in s or "network" in s:
        wanted += ["Automata (New)", "Linux Programming (New)", "Networking (New)", "Verify - General Ability Screen", "Occupational Personality Questionnaire OPQ32r"]

    if "finance" in s or "accounting" in s or "analyst" in s:
        wanted += ["Verify - Numerical Ability", "Financial Accounting (New)", "Basic Statistics (New)", "Graduate Scenarios"]

    if "contact" in s or "call center" in s or "customer service" in s or "support" in s:
        wanted += ["Contact Center Call Simulation (New)", "Customer Service (New)", "SVAR - Spoken English (U.S.)", "Conversational Multichat Simulation"]

    if "admin" in s or "assistant" in s:
        wanted += ["Microsoft Excel 365 (New)", "Microsoft Word 365 (New)", "Business Communication (adaptive)", "Administrative Professional - Short Form"]

    if "leadership" in s or "manager" in s or "executive" in s:
        wanted += ["Occupational Personality Questionnaire OPQ32r", "OPQ Leadership Report", "OPQ Universal Competency Report"]

    if wants_cognitive(ctx) or any(x in s for x in ["add cognitive", "add reasoning", "add aptitude"]):
        wanted += ["Verify - G+", "Verify - Numerical Ability", "Verify - Verbal Ability", "Verify - Inductive Reasoning (2014)", "Verify - Deductive Reasoning"]

    if include_personality(ctx) and (wants_personality(ctx) or "manager" in s or "leadership" in s or "executive" in s or "include personality" in s):
        wanted += ["Occupational Personality Questionnaire OPQ32r"]

    seen, clean = set(), []
    for x in wanted:
        if x not in seen:
            clean.append(x)
            seen.add(x)
    return clean

def promote(ctx: str, items: List[Dict[str, Any]], retriever: Retriever) -> List[Dict[str, Any]]:
    top = []

    for name in role_pack(ctx):
        x = find_exact(retriever.catalog, name)
        if x and x not in top:
            top.append(x)

    rest = [x for x in items if x not in top]
    return diversify(top + rest, 10)

def cmp_answer(text: str, retriever: Retriever) -> Dict[str, Any]:
    s = norm(text)
    picked = []

    aliases = {
        "opq32r": "Occupational Personality Questionnaire OPQ32r",
        "opq": "Occupational Personality Questionnaire OPQ32r",
        "verify numerical": "Verify - Numerical Ability",
        "numerical": "Verify - Numerical Ability",
        "gsa": "Global Skills Assessment",
        "global skills": "Global Skills Assessment",
        "verify g": "Verify - General Ability Screen",
    }

    for key, val in aliases.items():
        if key in s:
            x = find_exact(retriever.catalog, val)
            if x and x not in picked:
                picked.append(x)

    if len(picked) < 2:
        picked = diversify(retriever.find(text, 5), 5)

    if len(picked) < 2:
        return {"reply":"Please give the exact SHL assessment names you want me to compare.","recommendations":[],"end_of_conversation":False}

    a, b = picked[0], picked[1]
    reply = (
        f"{a['name']} is mainly categorized as {', '.join(a.get('keys') or []) or 'an SHL assessment'} and measures: {a.get('description','')[:180]} "
        f"{b['name']} is mainly categorized as {', '.join(b.get('keys') or []) or 'an SHL assessment'} and measures: {b.get('description','')[:180]} "
        "Choose based on which construct matters more for the role."
    )

    return {"reply":reply,"recommendations":payload([a,b]),"end_of_conversation":False}

def reason_for(item: Dict[str, Any], ctx: str) -> str:
    q = norm(ctx)
    n = item["name"].lower()

    if "java" in n:
        return "matches the Java/backend skill requirement"
    if "spring" in n:
        return "matches the Spring Boot/framework requirement"
    if "aws" in n or "amazon web services" in n:
        return "covers cloud/backend deployment skills"
    if "docker" in n:
        return "covers containerization skills"
    if "automata" in n:
        return "adds hands-on coding or simulation-based assessment"
    if "sql" in n:
        return "covers database/querying skills"
    if "opq" in n or item.get("test_type") == "P":
        return "adds personality/workplace behaviour insight"
    if "verify" in n:
        return "adds cognitive/ability screening"
    if "excel" in n:
        return "covers spreadsheet productivity skills"
    if "word" in n:
        return "covers document productivity skills"
    if "customer" in n or "contact" in n:
        return "matches customer support/contact-center responsibilities"
    if "financial" in n or "accounting" in n:
        return "matches finance/accounting domain knowledge"

    keys = ", ".join(item.get("keys") or [])
    return f"matches the requested role using catalog category: {keys or 'SHL assessment'}"

def explain_reply(prefix: str, items: List[Dict[str, Any]], ctx: str) -> str:
    lines = [prefix, "", "Why these assessments:"]
    for it in items[:7]:
        lines.append(f"- {it['name']}: {reason_for(it, ctx)}.")
    return "\n".join(lines)

def answer(messages: List[Message], retriever: Retriever) -> Dict[str, Any]:
    latest = latest_user(messages)
    ctx = all_user(messages)

    if not messages:
        return {"reply":"Tell me the role, seniority, and skills you want to assess, and I will recommend SHL assessments.","recommendations":[],"end_of_conversation":False}

    if refuse(latest):
        return {"reply":"I can only help with SHL assessment selection and comparison using the SHL catalog. I can’t help with off-topic, legal, or prompt-injection requests.","recommendations":[],"end_of_conversation":False}

    if compare(latest):
        return cmp_answer(latest, retriever)

    if vague(ctx):
        return {"reply":"Happy to help. What role is this for, what seniority level, and do you want technical skills, cognitive ability, personality/behavior, situational judgement, or a mix?","recommendations":[],"end_of_conversation":False}

    if wants_shorter(latest):
        ctx += "\nPrefer shorter assessments where possible."

    items = retriever.search(ctx, 40, include_personality(ctx), exclusions(ctx))
    items = promote(ctx, items, retriever)

    if not include_personality(ctx):
        items = [x for x in items if "opq" not in x["name"].lower() and x.get("test_type") != "P"]

    bad_terms = ["customer service", "contact center", "phone simulation", "data entry"]
    if any(x in norm(ctx) for x in ["java", "backend", "spring", "docker", "aws"]):
        items = [x for x in items if not any(b in x["name"].lower() for b in bad_terms)]

    items = diversify(items, 10)

    if not items:
        return {"reply":"I need a little more detail to recommend from the SHL catalog. Please share role, seniority, main skills, and assessment type needed.","recommendations":[],"end_of_conversation":False}

    prefix = "Updated the shortlist based on your latest constraint." if any(x in norm(latest) for x in ["actually","remove","drop","instead","replace","add","shorter"]) else "Based on the conversation, here is a grounded SHL shortlist from the catalog."

    if "rust" in norm(ctx):
        prefix = "The catalog may not contain a Rust-specific test, so I selected the closest coding, Linux/networking, cognitive, and personality options from SHL's catalog."

    reply = explain_reply(prefix, items, ctx)
    return {"reply":reply,"recommendations":payload(items),"end_of_conversation":False}
