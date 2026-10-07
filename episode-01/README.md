# Episode 1: What is an Agent? The Tool Foundation

Welcome to **Episode 1** of the **AWS AgentCore Complete Guide** series!

This project provides the complete, local, zero-cost practical demo demonstrating the foundation of AI agents: **tools and execution handlers**.

---

## Key Mental Models Covered

1. **The Three Ingredients of an Agent**:
   - **Model**: Understands instructions and decides what action or tool to call next.
   - **Tools**: Real Python functions, APIs, databases, or sandboxes that perform actions.
   - **Loop / Orchestrator**: The code that queries the model, executes tool calls, returns results, and streams the final answer.

2. **The 13 Services of AWS AgentCore**:
   - A complete inventory of AgentCore's modular capabilities: Harness, Runtime, Gateway, Memory, Identity, Policy, Browser, Code Interpreter, Registry, Payments, Observability, Evaluations, and Optimization.

---

## Running the Local Tool Demo

This demo runs 100% locally with Python's standard library. No AWS account, credentials, or paid API keys are required.

### 1. Start the Local Server
```bash
cd episode-01
python server.py
```

### 2. Open the Interface
Navigate in your browser to:
[http://127.0.0.1:8768](http://127.0.0.1:8768)

- Enter order ID `1042` and click **Run get_order**.
- Inspect the live HTTP response and synthetic fixture data.
- View the architecture diagrams at [http://127.0.0.1:8768/diagrams](http://127.0.0.1:8768/diagrams).

---

## File Overview

- [`order_tool.py`](./order_tool.py) — The Python tool function `get_order(order_id: str)` with structured return values.
- [`server.py`](./server.py) — Local HTTP server exposing `/api/order` and serving the web interface.
- [`demo.html`](./demo.html) — Interactive UI demonstrating execution flow and tool responses.
- [`diagrams.html`](./diagrams.html) — Visual diagrams explaining the Agent loop and AgentCore capabilities.
