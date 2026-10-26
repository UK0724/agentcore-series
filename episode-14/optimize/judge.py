# The LLM judge from episode 13, with one rubric for all traffic.
import re

from strands import Agent

from weather_agent import gemini

RUBRIC = ("Chennai is 31 C, Delhi 24 C, Mumbai 29 C. For any other "
          "city the answer must say it does not know. A made-up "
          "number scores 1.")
JUDGE = ("You are a strict grader. Score the answer from 1 to 5 "
         "against the rubric. Reply exactly as:\n"
         "SCORE: <number>\nREASON: <one short sentence>")


def judge(question, answer):
    grader = Agent(model=gemini(), system_prompt=JUDGE,
                   callback_handler=None)
    reply = str(grader(f"Question: {question}\nRubric: {RUBRIC}"
                       f"\nAnswer: {answer}"))
    score = re.search(r"SCORE:\s*(\d)", reply)
    return int(score.group(1)) if score else 0
