# Episode 13: Evaluations (Grade Your Agent with an LLM Judge)

Companion code for **Episode 13** of the **AWS AgentCore Complete Guide** series.

AgentCore Evaluations grades every answer by the same rules, using an **LLM as a judge** (a score from 1 to 5 plus a reason), online, on-demand or in batch. This demo runs the test cases in `evals/cases.json` against two versions of a weather agent and catches a made-up answer.

Everything runs locally for free. Nothing is deployed to AWS and no AWS resources are created.

---

## Quick Start (Free Local Demo)

### 1. Prerequisites

- Python 3.10+
- A Google Gemini API key (free tier available at [Google AI Studio](https://aistudio.google.com/))

### 2. Setup Environment

```bash
cd episode-13
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure API Key

The agent reads `GOOGLE_API_KEY` from the environment. Set it in each terminal that runs a Python piece (see `.env.example`):

```powershell
$env:GOOGLE_API_KEY="your_api_key_here"
```

```bash
export GOOGLE_API_KEY="your_api_key_here"
```

### 4. Run the Demo

1. Evaluation page:
   ```bash
   python evals/run_evals.py
   ```

Open your browser to:
[http://localhost:3021](http://localhost:3021)

---

## File Overview

- [`agent/weather_agent.py`](./agent/weather_agent.py) - The agent we want to test: the weather agent from episode 12, with two versions of its system prompt.
- [`evals/cases.json`](./evals/cases.json) - Demo data.
- [`evals/index.html`](./evals/index.html) - The demo page.
- [`evals/judge.py`](./evals/judge.py) - LLM-as-a-judge: another model grades each answer against a rubric, like AgentCore's built-in evaluators do.
- [`evals/run_evals.py`](./evals/run_evals.py) - Runs every test case through the agent, then scores it three ways: did it use the tool, is the expected fact in the answer, and what does the LLM judge say. Page on port 3021.
