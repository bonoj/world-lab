# World Lab

A laboratory for rapidly probing systems across different world substrates.

## Continuous collaboration setup

This repository is configured so that a human can work with ChatGPT conversationally while ChatGPT updates the executable artifact in GitHub and GitHub Pages publishes the accepted `main` branch automatically.

The proven loop is:

```text
human intent
→ model inspects the artifact
→ model clarifies only what matters
→ model states the proposed delta
→ human confirms
→ model edits and validates the artifact
→ model commits the accepted head to main
→ GitHub Pages publishes automatically
→ human refreshes the stable URL and plays
→ repeat
```

The human does not need to manually rename, save, upload, or move artifact files to publish an accepted build.

For rapid development, a locally downloaded/opened artifact can still be used for immediate inspection. GitHub Pages is the continuously published head, not the low-latency development runtime.

## Live site

World Lab is published at:

https://bonoj.github.io/world-lab/

This is a **project Pages site**, so `/world-lab/` is part of the URL. The bare `bonoj.github.io` address is a different site namespace.

The first end-to-end Pages deployment was confirmed from the phone at **11:04 PM on September 24, 2026 (America/New_York)**.

## GitHub / ChatGPT write access

### 1. Create or choose the repository

World Lab currently uses:

- repository: `bonoj/world-lab`
- default branch: `main`
- visibility: public
- executable entry point: `/index.html`

A separate repository can be used for another person's World Lab.

### 2. Connect GitHub to ChatGPT

Authorize the **ChatGPT Codex Connector** for the GitHub account from ChatGPT.

GitHub may show this authorization under:

```text
GitHub
→ Settings
→ Applications
→ Authorized GitHub Apps
→ ChatGPT Codex Connector
```

Authorization alone is not sufficient for repository writes.

### 3. Install the ChatGPT Codex Connector on the GitHub account

Official installation page:

https://github.com/apps/chatgpt-codex-connector/installations/new

Install it on the GitHub account that owns the repository.

For least privilege, choose:

```text
Only select repositories
→ select the World Lab repository
```

This installation step matters. In our first attempt the connector was authorized but **not installed on the account**. Reads were possible, but repository-content writes failed with:

```text
403 Resource not accessible by integration
```

After installing the connector on `bonoj` with access to `world-lab`, the same conversational write succeeded.

### 4. Verify the write seam before doing real work

Ask ChatGPT to create a harmless probe file in the repository.

Our verified probe:

- file: `chatgpt-write-probe.txt`
- commit: `fb531b8945a27eb02c6211d4fd1ec97a23d76a39`

That proved:

```text
phone
→ ChatGPT conversation
→ GitHub connector
→ repository commit
```

Do not assume the setup works merely because ChatGPT can read the repository. Verify an actual write.

### 5. Verify large executable transport

The current World Lab is a self-contained HTML artifact of roughly 1 MB. The ordinary small-file write path was not allowed to dictate the artifact architecture.

The successful transport path was:

```text
uploaded World Lab HTML
→ Git blob
→ Git tree
→ Git commit
→ update main ref
```

The first full executable commit was:

```text
a38714fb342baa0ed956e359c74c1358fd94858a
```

After that commit, `index.html` was fetched back from `main`, downloaded on the phone, opened in the browser, and confirmed working before Pages was enabled.

This matters because a connector limitation is not a reason to split or redesign an otherwise coherent executable artifact.

## Continuous deployment with GitHub Pages

**Status: configured and verified.**

No custom GitHub Actions workflow or build system is required for the current self-contained HTML artifact.

Repository configuration:

```text
Repository
→ Settings
→ Pages
→ Build and deployment
→ Source: Deploy from a branch
→ Branch: main
→ Folder: /(root)
→ Save
```

GitHub then reports:

```text
Your GitHub Pages site is currently being built from the main branch.
```

Because `index.html` lives at the repository root, accepted commits to `main` become the next published World Lab automatically.

The deployment path has now been verified end-to-end:

```text
phone
→ conversation
→ confirmed artifact mutation
→ GitHub commit to main
→ automatic GitHub Pages publication
→ https://bonoj.github.io/world-lab/
→ refresh and inspect
```

Pages publication is asynchronous and should not be treated as the rapid development loop. We have not yet measured steady-state commit-to-live latency; that should be measured during ordinary future changes rather than guessed from initial provisioning.

## Collaboration rule

Repository access removes file-handling friction; it does not remove human authorship.

The working interaction remains:

1. Human expresses intent.
2. Model inspects current artifact and context.
3. Model resolves consequential ambiguity with the smallest useful clarification.
4. Model states the concrete proposed change.
5. Human confirms.
6. Model edits and validates.
7. Model commits the accepted head to `main`.
8. GitHub Pages publishes it.
9. Human inspects the executable evidence and continues the conversation.

Inference can reduce communication cost. It should not silently replace human intention.

## Why this exists

The infrastructure should disappear underneath the collaboration. A person extending their World Lab should mostly experience two things:

- a conversation;
- the living executable toy.

Git, deployment, file transfer, and version bookkeeping are implementation machinery, not the interaction model.

A minimal user experience can therefore be two browser tabs:

```text
Tab 1: talk to ChatGPT about the world
Tab 2: refresh the published World Lab and play
```

---

This README records a setup that was actually performed and tested from a phone. Where behavior has not yet been measured—such as steady-state Pages deployment latency—it is left explicitly unclaimed rather than replaced with speculative instructions.
