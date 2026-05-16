# Agent Prompts

Starter system prompts for the five agents in the Governed Intent Development pipeline. Each file is self-contained and usable directly as a system prompt.

| Agent | File | Workflow stage |
|---|---|---|
| Intent Elicitation Agent | [elicitation-agent.md](elicitation-agent.md) | Stage 2 — after authoring |
| Intent Review Agent | [review-agent.md](review-agent.md) | Stage 3 — after elicitation |
| Compliance Agent | [compliance-agent.md](compliance-agent.md) | Stage 7 — after code generation |
| Security Agent | [security-agent.md](security-agent.md) | Stage 8 — after compliance check |
| Intent Maintenance Agent | [maintenance-agent.md](maintenance-agent.md) | Pre-change gate — before any revision |

See [workflow/workflow.md](../workflow/workflow.md) for where each agent fits in the full lifecycle.
