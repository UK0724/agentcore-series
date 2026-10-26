# Our own agent code, wrapped for AgentCore Runtime.
# The loop is ours (Strands); Runtime only needs two HTTP endpoints.
import os

from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent
from strands.models.gemini import GeminiModel

from tools import get_sprint_status

app = BedrockAgentCoreApp()  # serves POST /invocations and GET /ping


def build_agent():
    model = GeminiModel(
        client_args={"api_key": os.environ["GOOGLE_API_KEY"]},
        model_id="gemini-flash-lite-latest",
    )
    return Agent(
        model=model,
        system_prompt="You are a sprint assistant. Use your tools. "
        "Answer in one sentence.",
        tools=[get_sprint_status],
        callback_handler=None,
    )


@app.entrypoint
def invoke(payload, context):
    # Runtime sends the user's JSON as the payload, and the session ID in the context.
    result = build_agent()(payload["prompt"])
    return {"response": str(result).strip(), "session": context.session_id}


if __name__ == "__main__":
    app.run()  # port 8080, the same as on AgentCore Runtime
