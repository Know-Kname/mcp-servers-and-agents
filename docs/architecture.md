# Architecture Guide

## Four Layers

### Layer 1: MCP Servers (the tools)
16 servers provide external capabilities. When the AI needs to search GitHub or fetch a web page, it calls an MCP server.

- **npx (4)**: filesystem, memory, sequential-thinking, perplexity
- **Docker (3)**: fetch, git, n8n
- **Custom Node (2)**: power-apps, sharepoint
- **Remote HTTP (7)**: github-official, context7, notion, fabric, foundry, vercel, figma

The remote tier is the one that grows — it is now nearly half the stack.
`github-official`, `notion`, `fabric`, and `context7` all moved off local
runtimes onto their vendors' hosted endpoints, and `foundry` was added the same
way. Each authenticates interactively (OAuth / Entra ID) rather than holding a
long-lived token, and each updates server-side — no image to pull, no credential
to rotate, no package resolution at launch.

That leaves exactly three secrets in the config — `PERPLEXITY_API_KEY`,
`CONTEXT7_API_KEY`, and the n8n pair — plus the Azure service-principal
credentials still used by `power-apps` and `sharepoint`.

**Context cost.** Every enabled server's tools occupy the model's context before
work starts, so breadth is not free. `github-official` alone can expose well over a
hundred tools if pointed at `/mcp/x/all`. It ships scoped to the default toolset,
with per-toolset and read-only endpoints documented in the
[server catalog](../servers/README.md) for when a session needs something narrower
or safer.

### Layer 2: Rules (the behavior)
14 rule files shape how the AI works. `master-router.mdc` is the central dispatcher. `research-workflow.mdc` enforces cost hierarchy:
1. Memory MCP (free)
2. Context7 (free)
3. WebSearch (free)
4. Perplexity (paid) -- only when free sources fail

### Layer 3: Agents (the specialists)
16 agents act as specialized personas. Selected automatically by the master-router based on your request.

### Layer 4: Skills (the playbooks)
31 step-by-step workflow instructions. Read on-demand when the task matches.

## Data Flow: Deployment
```
User: "Deploy to Vercel"
  -> master-router.mdc routes to auto-deploy skill
  -> auto-deploy/SKILL.md provides steps
  -> vercel MCP server executes commands
  -> Result returned
```

## Data Flow: Research
```
User: "How does React Server Components work?"
  -> research-workflow.mdc checks memory first (free)
  -> No prior research -> query context7 (free)
  -> Found answer -> save to memory for next time
```
