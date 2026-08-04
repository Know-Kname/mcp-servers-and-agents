---
name: vercel-deploy
description: Vercel-specific deployment practice - environment variables per environment, build settings, preview versus production behaviour, and the failure modes that look like code bugs. Use when deploying to Vercel or diagnosing a Vercel build.
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

# Vercel deployment

## Environment variables are per-environment

The most common Vercel failure: a variable set for Production but not Preview,
so previews break in ways that look like code bugs. Set each variable for every
environment that needs it — Production, Preview, Development — and confirm it
in the dashboard rather than assuming inheritance.

Build-time versus runtime matters too. Anything a client bundle reads must be
prefixed (`VITE_`, `NEXT_PUBLIC_`) **and present at build time**. Setting it
after the build changes nothing until you redeploy.

## Changing a variable does not redeploy

Vercel does not rebuild on an environment-variable change. The old value stays
baked into the deployed bundle until you trigger a new deployment. If a config
change "didn't take effect", this is usually why.

## Build settings

- Node version: pin via `.nvmrc` or `engines` so local and CI agree.
- The build must **fail** on type errors. A build that warns and ships defeats
  the point of the check.
- `.vercelignore` keeps the upload small; verify nothing needed is excluded.
- `vercel.json` rewrites and headers apply in preview too — test them there.

## Preview versus production

Previews are real deployments against real services. A preview pointed at a
production database can write to it. Confirm which backend each environment
targets before treating previews as safe to experiment in.

## Verify after deploying

- Load the actual deployed URL. A green build is not a working app.
- Check runtime logs — errors that only appear under production config land
  there, not in the build output.
- Confirm the change is live; cached builds are common and quiet.

## Diagnosing a failed build

1. Read the build log from the top. The first error is the real one; later
   errors are usually consequences.
2. Reproduce locally with the same Node version and a clean install
   (`rm -rf node_modules && npm ci`). Most "works locally" failures are a
   stale lockfile or a dependency that was never actually installed.
3. Missing env var at build time reads as an undefined-variable crash, not as
   a config error. Check that before debugging the code.
