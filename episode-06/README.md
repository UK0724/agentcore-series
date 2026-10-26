# Episode 6: Identity (No Secrets in Your Agent)

Companion code for **Episode 6** of the **AWS AgentCore Complete Guide** series.

AgentCore Identity answers two questions: **who is calling** the agent (inbound), and **which keys** the agent may use (outbound, from a token vault). Private data needs the user's consent first. This demo uses a tiny stand-in for Identity, a pretend calendar API, and an agent whose code contains no secrets.

Everything runs locally for free. Nothing is deployed to AWS and no AWS resources are created.

---

## Quick Start (Free Local Demo)

### 1. Prerequisites

- Python 3.10+
- A Google Gemini API key (free tier available at [Google AI Studio](https://aistudio.google.com/))

### 2. Setup Environment

```bash
cd episode-06
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

Start each piece in its own terminal, in this order (from the `episode-06` folder):

1. Pretend calendar API (port 4011):
   ```bash
   python calendar_api.py
   ```
2. Agent page:
   ```bash
   python agent.py
   ```

Open your browser to:
[http://localhost:3014](http://localhost:3014)

`calendar-demo-secret-not-real-0001` in `calendar_api.py` is a demo value, not a real secret.

---

## File Overview

- [`agent.py`](./agent.py) - The agent: it checks who is calling, and its calendar tool gets a short-lived token from the vault. No secret in this file.
- [`calendar_api.py`](./calendar_api.py) - A pretend calendar service (like Google Calendar), port 4011.
- [`identity.py`](./identity.py) - A tiny stand-in for AgentCore Identity, to show the ideas
- [`page.html`](./page.html) - The demo page.
