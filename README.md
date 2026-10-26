# AWS AgentCore Complete Guide

Companion repository for the **AWS AgentCore Complete Guide** video series on **LearnVerse**.

This repository contains free, reproducible code examples, local test harnesses, and architecture diagrams exploring every core service of **AWS AgentCore**.

---

## Series Episodes

| Episode | Title | Description | Code |
| :---: | :--- | :--- | :---: |
| **01** | **What is an Agent? The Tool Foundation** | Demystifying AI Agents (Model + Tools + Loop), full 13-service inventory of AgentCore, and a zero-cost local Python tool server. | [📁 episode-01](./episode-01) |
| **02** | **Harness (The Managed Agent Loop)** | Why the loop alone is not enough, microVM sandboxes, 5 tool types, streamed events, and a local Strands Agents demo streaming live step cards. | [📁 episode-02](./episode-02) |
| **03** | **Runtime** | Host your own agent code: the `/invocations` + `/ping` contract on port 8080, one microVM per session, and the `BedrockAgentCoreApp` SDK. | [📁 episode-03](./episode-03) |
| **04** | **Gateway & MCP** | Turn REST APIs into MCP tools behind one `/mcp` front door: targets, `target___tool` names, inbound and outbound auth. | [📁 episode-04](./episode-04) |
| **05** | **Memory** | Short-term memory (turns of one session) vs long-term memory (facts extracted and recalled across sessions). | [📁 episode-05](./episode-05) |
| **06** | **Identity** | No secrets in agent code: inbound identity, a token vault for short-lived tokens, and user consent first. | [📁 episode-06](./episode-06) |
| **07** | **Policy** | Rules the agent cannot break: every tool call checked at the gateway against Cedar rules, with default deny. | [📁 episode-07](./episode-07) |
| **08** | **Browser** | Isolated browser sessions for sites with no API: actions in, screenshots out. | [📁 episode-08](./episode-08) |
| **09** | **Code Interpreter** | Exact answers from code: the model writes Python, a sandbox runs it, only the output comes back. | [📁 episode-09](./episode-09) |
| **10** | **Agent Registry** | One catalog for agents, MCP servers and skills, with a draft, pending, approved flow. | [📁 episode-10](./episode-10) |
| **11** | **Payments** | Tiny payments with hard limits: HTTP 402, pay, retry, inside a spending cap. Pretend cents only. | [📁 episode-11](./episode-11) |
| **12** | **Observability** | A flight recorder for your agent: sessions, traces and spans in OpenTelemetry. | [📁 episode-12](./episode-12) |
| **13** | **Evaluations** | Grade your agent with test cases, a rubric and an LLM judge. | [📁 episode-13](./episode-13) |
| **14** | **Optimization** | Recommend a better prompt, save it as a config bundle, A/B test it, keep the winner. | [📁 episode-14](./episode-14) |
| **15** | **Web Search** | Fresh facts with sources: a search tool on the gateway with domain filters and citations. | [📁 episode-15](./episode-15) |

---

## Design Philosophy

- **Zero Unnecessary Cloud Costs**: All practical concepts are taught with genuine documentation and 100% free, local reproduction harnesses before cloud deployment.
- **Mental Models First**: Visual step cards, architecture diagrams, and plain-language definitions precede raw code.
- **Multilingual Education**: Video tutorials include complete, studio-calibrated multi-audio tracks in English, Telugu (తెలుగు), and Tamil (தமிழ்).

---

## Technologies Used

- **Frameworks**: [Strands Agents](https://github.com/strands-agents/strands), Python 3.10+, Next.js
- **Model Providers**: Google Gemini (`gemini-flash-lite-latest`), Amazon Bedrock
- **Protocols**: SSE (Server-Sent Events), REST, MCP (Model Context Protocol)

---

## License

MIT License. Free for educational and commercial use.
