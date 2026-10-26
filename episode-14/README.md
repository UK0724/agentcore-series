# Episode 14: Optimization (A/B Test Your Agent's Prompt)

Companion code for **Episode 14** of the **AWS AgentCore Complete Guide** series.

AgentCore Optimization recommends a better prompt from traces, saves it as a **configuration bundle**, **A/B tests** it on real traffic with sticky routing, and keeps the winner. This demo runs all three steps locally on one page.

Everything runs locally for free. Nothing is deployed to AWS and no AWS resources are created.

---

## Quick Start (Free Local Demo)

### 1. Prerequisites

- Python 3.10+
- A Google Gemini API key (free tier available at [Google AI Studio](https://aistudio.google.com/))

### 2. Setup Environment

```bash
cd episode-14
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

1. Optimization page:
   ```bash
   python optimize/server.py
   ```

Open your browser to:
[http://localhost:3022](http://localhost:3022)

---

## File Overview

- [`agent/weather_agent.py`](./agent/weather_agent.py) - The weather agent again. Its system prompt now comes from a config bundle, so we can swap versions without code changes.
- [`optimize/ab_test.py`](./optimize/ab_test.py) - An A/B test: each session is routed to variant A or B. The routing is sticky: the same session ID always gets the same variant. Then the judge scores every answer.
- [`optimize/bundles.json`](./optimize/bundles.json) - Demo data.
- [`optimize/index.html`](./optimize/index.html) - The demo page.
- [`optimize/judge.py`](./optimize/judge.py) - The LLM judge from episode 13, with one rubric for all traffic.
- [`optimize/recommend.py`](./optimize/recommend.py) - A recommendation: a model reads a failing trace and suggests a better system prompt, aimed at a goal (like AgentCore's target evaluator). It is only a suggestion: review and test it first.
- [`optimize/server.py`](./optimize/server.py) - The optimization loop on one page, port 3022
