# A recommendation: a model reads a failing trace and suggests a
# better system prompt, aimed at a goal (like AgentCore's target
# evaluator). It is only a suggestion: review and test it first.
from strands import Agent

from weather_agent import gemini

COACH = ("You improve system prompts for AI agents. Given the "
         "goal, the current prompt and a failing example, fix the "
         "cause of the failure. Reply with ONLY the new system "
         "prompt, in one or two sentences.")
GOAL = "Answers must be correct and use only the weather tool data."


def recommend(prompt, failure):
    coach = Agent(model=gemini(), system_prompt=COACH,
                  callback_handler=None)
    return str(coach(f"Goal: {GOAL}\nCurrent prompt: {prompt}\n"
                     f"Failing example: {failure}")).strip()
