# AWS AgentCore Complete Guide

Companion repository for the **AWS AgentCore Complete Guide** video series on **LearnVerse**.

This repository contains free, reproducible code examples, local test harnesses, and architecture diagrams exploring every core service of **AWS AgentCore**.

---

## Series Episodes

| Episode | Title | Description | Code |
| :---: | :--- | :--- | :---: |
| **01** | **What is an Agent? The Tool Foundation** | Demystifying AI Agents (Model + Tools + Loop), full 13-service inventory of AgentCore, and a zero-cost local Python tool server. | [📁 episode-01](./episode-01) |
| **02** | **Harness (The Managed Agent Loop)** | Why the loop alone is not enough, microVM sandboxes, 5 tool types, streamed events, and a local Strands Agents demo streaming live step cards. | [📁 episode-02](./episode-02) |
| **03** | **Runtime** | Custom agent runtime code, bring-your-own-framework, and microVM deployment. *(Coming next)* | Coming soon |
| **04** | **Gateway & MCP** | Remote tool routing and Model Context Protocol servers. | Planned |
| **05** | **Memory** | Short-term and long-term agent memory persistence across sessions. | Planned |
| **06** | **Identity** | Agent authentication, session tokens, and security boundaries. | Planned |

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
