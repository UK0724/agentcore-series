# Episode 12: Observability (See Every Step)

Companion code for **Episode 12** of the **AWS AgentCore Complete Guide** series.

From outside you only see an agent's answer. AgentCore Observability records every step as **OpenTelemetry** spans (session, trace, span) into CloudWatch, so you can find the slow step. This demo turns on Strands tracing, keeps the spans in memory and draws them locally.

Everything runs locally for free. Nothing is deployed to AWS and no AWS resources are created.

---

## Quick Start (Free Local Demo)

### 1. Prerequisites

- Python 3.10+
- A Google Gemini API key (free tier available at [Google AI Studio](https://aistudio.google.com/))

### 2. Setup Environment

```bash
cd episode-12
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

1. Agent page with trace view:
   ```bash
   python agent/agent.py
   ```

Open your browser to:
[http://localhost:3020](http://localhost:3020)

---

## File Overview

- [`agent/agent.py`](./agent/agent.py) - An agent with tracing turned on. Every step becomes an OpenTelemetry span, the same format AgentCore Observability uses. Here we keep the spans in memory and draw them locally.
- [`agent/index.html`](./agent/index.html) - The demo page.
- [`agent/tools.py`](./agent/tools.py) - Two small tools, so the trace has something to show.
