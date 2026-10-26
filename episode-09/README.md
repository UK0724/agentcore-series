# Episode 9: Code Interpreter (Exact Answers in a Sandbox)

Companion code for **Episode 9** of the **AWS AgentCore Complete Guide** series.

Models guess at exact maths. With AgentCore Code Interpreter the model **writes code**, a **sandbox runs it**, and only the output comes back. This demo runs a tiny sandbox service (a separate Python process per session, with a time limit) and an agent that answers a question about `data/sales.csv` with code.

Everything runs locally for free. Nothing is deployed to AWS and no AWS resources are created.

---

## Quick Start (Free Local Demo)

### 1. Prerequisites

- Python 3.10+
- A Google Gemini API key (free tier available at [Google AI Studio](https://aistudio.google.com/))

### 2. Setup Environment

```bash
cd episode-09
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

Start each piece in its own terminal, in this order (from the `episode-09` folder):

1. Sandbox service (port 4041):
   ```bash
   python sandbox/sandbox.py
   ```
2. Agent page:
   ```bash
   python agent/agent.py
   ```

Open your browser to:
[http://localhost:3017](http://localhost:3017)

---

## File Overview

- [`agent/agent.py`](./agent/agent.py) - An agent that answers with code: it writes Python, the sandbox runs it, and the agent reads the output. No guessing at maths.
- [`agent/index.html`](./agent/index.html) - The demo page.
- [`data/sales.csv`](./data/sales.csv) - Demo data.
- [`sandbox/sandbox.py`](./sandbox/sandbox.py) - A tiny code sandbox service, port 4041, like AgentCore Code Interpreter: each session gets its own empty folder, and code runs in a separate Python process with a time limit.
