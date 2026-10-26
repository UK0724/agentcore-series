# Episode 5: Memory (Short-Term vs Long-Term)

Companion code for **Episode 5** of the **AWS AgentCore Complete Guide** series.

Models forget everything between requests. AgentCore Memory adds **short-term memory** (the turns of one session) and **long-term memory** (facts extracted after a session and retrieved in later ones), tagged by actor ID and session ID. This demo shows both kinds locally across three sessions.

Everything runs locally for free. Nothing is deployed to AWS and no AWS resources are created.

---

## Quick Start (Free Local Demo)

### 1. Prerequisites

- Python 3.10+
- A Google Gemini API key (free tier available at [Google AI Studio](https://aistudio.google.com/))

### 2. Setup Environment

```bash
cd episode-05
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

1. Memory demo page:
   ```bash
   python memory_demo.py
   ```

Open your browser to:
[http://localhost:3013](http://localhost:3013)

Session files and extracted facts are written to `memory/` while the demo runs. Delete that folder to start fresh.

---

## File Overview

- [`long_term.py`](./long_term.py) - A tiny long-term memory, to show the idea behind AgentCore Memory.
- [`memory_demo.py`](./memory_demo.py) - Short-term memory: Strands keeps each session's turns in files.
- [`page.html`](./page.html) - The demo page.
