# An A/B test: each session is routed to variant A or B. The
# routing is sticky: the same session ID always gets the same
# variant. Then the judge scores every answer.
import hashlib

from judge import judge
from weather_agent import make_agent

TRAFFIC = ["How hot is Chennai?", "How hot is Paris?",
           "Is Delhi colder than Mumbai?", "Weather in Tokyo?",
           "Temperature in Mumbai?", "How warm is London?",
           "Hottest of Chennai, Delhi, Mumbai?", "Berlin today?",
           "How hot is Sydney?", "Is Mumbai warmer than Delhi?"]


def variant_for(session_id):  # sticky: same ID, same variant
    digest = hashlib.sha256(session_id.encode()).digest()
    return "A" if digest[0] % 2 == 0 else "B"


def run_session(session_id, question, prompts):
    variant = variant_for(session_id)
    answer = str(make_agent(prompts[variant])(question)).strip()
    return {"session": session_id, "variant": variant,
            "question": question, "answer": answer,
            "score": judge(question, answer)}
