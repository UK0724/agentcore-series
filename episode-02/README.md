# Episode 2: Harness (The Managed Agent Loop)

Welcome to **Episode 2** of the **AWS AgentCore Complete Guide** series!

In production, an agent loop is not enough by itself. You need compute, safe microVM sandboxes, tool connections, persistent memory, identity, and observability. This complete package is an **Agent Harness**.

AWS AgentCore Harness transforms the agent loop into declarative configuration (`harness.json`). It is powered under the hood by **Strands Agents**, an open-source framework.

This project lets you run the exact same Strands engine locally for free, showing how configuration maps to loop execution and streaming event cards.

---

## Architecture: How Managed Harness Works

```
┌────────────────────────────────────────────────────────┐
│               Declarative harness.json                 │
│         (Model, System Prompt, Tool Registry)          │
└───────────────────────────┬────────────────────────────┘
                            │ Read by Harness Engine
                            ▼
┌────────────────────────────────────────────────────────┐
│                   Managed Loop Engine                  │
│                     (Strands Agent)                    │
│                                                        │
│  1. [loop]       Sends prompt & tool definitions       │
│  2. [model]      Model emits stopReason: tool_use      │
│  3. [tool]       Harness executes tool & sends result  │
│  4. [answer]     Model emits stopReason: end_turn      │
└───────────────────────────┬────────────────────────────┘
                            │ Server-Sent Events (SSE)
                            ▼
┌────────────────────────────────────────────────────────┐
│              Live Visual Step Cards (Web UI)           │
│      Orange (Loop) → Purple (Model) → Green (Tool)     │
└────────────────────────────────────────────────────────┘
```

---

## Quick Start (Free Local Demo)

### 1. Prerequisites
- Python 3.10+
- A Google Gemini API key (free tier available at [Google AI Studio](https://aistudio.google.com/))

### 2. Setup Environment
```bash
cd episode-02
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure API Key
```bash
cp .env.example .env
# Edit .env and paste your GOOGLE_API_KEY
```

Or set it in your terminal:
```powershell
$env:GOOGLE_API_KEY="your_api_key_here"
```

### 4. Run the Agent Server
```bash
python agent.py
```

Open your browser to:
[http://localhost:3010](http://localhost:3010)

Click **Ask** to watch the agent loop stream each step as visual color-coded cards:
- **Card 1 (Orange)**: Loop sends system prompt and tool schema to the Gemini model.
- **Card 2 (Purple)**: Model requests `get_sprint_status` tool call for `sprint-42` (`tool_use`).
- **Card 3 (Green)**: Loop runs the tool against local fixture and returns data.
- **Card 4 (Blue)**: Model generates the final answer (`end_turn`).

---

## File Overview

- [`harness.json`](./harness.json) — Declarative harness configuration (model ID, system prompt, allowed tools).
- [`tools.py`](./tools.py) — Python tool decorated with `@tool` and schema docstring.
- [`agent.py`](./agent.py) — Reads `harness.json`, configures `Strands` agent, and streams SSE step cards.
- [`data/sprint.json`](./data/sprint.json) — Local mock sprint data.
- [`page/index.html`](./page/index.html) — Live UI visualizing every loop event.
