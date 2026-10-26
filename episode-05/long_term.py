# A tiny long-term memory, to show the idea behind AgentCore Memory.
# After a session, we EXTRACT facts about the user and save them.
# In a new session, we RETRIEVE the facts that match the question.
import json
import re
from pathlib import Path

STORE = Path(__file__).parent / "memory" / "long_term.json"


def load():
    if STORE.exists():
        return json.loads(STORE.read_text())
    return {}


def save_records(actor_id, facts):
    records = load()
    mine = records.setdefault(actor_id, [])
    for fact in facts:
        if fact not in mine:
            mine.append(fact)
    STORE.parent.mkdir(exist_ok=True)
    STORE.write_text(json.dumps(records, indent=2))
    return mine


def stems(text):
    # "leads" and "lead" both become "lead" (first 4 letters).
    return {w[:4] for w in re.findall(r"[a-z0-9]+", text.lower())
            if len(w) > 2}


def retrieve(actor_id, question, top_k=3):
    # Keep facts sharing words with the question.
    # (AgentCore Memory uses real semantic search instead.)
    asked = stems(question)
    facts = load().get(actor_id, [])
    hits = [f for f in facts if asked & stems(f)]
    return sorted(hits, key=lambda f: -len(asked & stems(f)))[:top_k]
