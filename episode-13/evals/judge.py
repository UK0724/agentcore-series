# LLM-as-a-judge: another model grades each answer against a
# rubric, like AgentCore's built-in evaluators do.
import re
import sys
from pathlib import Path

from strands import Agent

sys.path.append(str(Path(__file__).parent.parent / "agent"))
from weather_agent import gemini  # noqa: E402

JUDGE = ("You are a strict grader. Score the answer from 1 to 5 "
         "against the rubric. Reply exactly as:\n"
         "SCORE: <number>\nREASON: <one short sentence>")


def judge(question, answer, rubric):
    grader = Agent(model=gemini(), system_prompt=JUDGE,
                   callback_handler=None)
    reply = str(grader(f"Question: {question}\nRubric: {rubric}"
                       f"\nAnswer: {answer}"))
    score = re.search(r"SCORE:\s*(\d)", reply)
    reason = re.search(r"REASON:\s*(.+)", reply)
    return (int(score.group(1)) if score else 0,
            reason.group(1).strip() if reason else reply)
