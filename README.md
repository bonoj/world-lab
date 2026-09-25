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

World Lab remains a single self-contained HTML artifact. The ordinary small-file write path is not allowed to dictate the artifact architecture.

The first successful large-artifact publication used the raw Git object path:

```text
uploaded World Lab HTML
→ Git blob
→ Git tree
→ Git commit
→ update main ref
```

That historical solution is preserved in the repository history; the first full executable commit was:

```text
a38714fb342baa0ed956e359c74c1358fd94858a
```

As World Lab grew to 6,977,815 bytes, a single connector request stopped being a reliable transport. The replacement is an interruption-safe, multi-turn transport protocol. It treats the accepted artifact as opaque release bytes and moves transport state into GitHub rather than relying on one ChatGPT turn or conversation context.

The proven large-file path is now:

```text
accepted artifact
→ compute exact byte count + expected Git blob SHA
→ split transport representation into numbered connector-safe chunks
→ persist chunks + manifest on a world-lab-transport-* branch
→ GitHub Actions reconstructs the bytes
→ receiver verifies byte count + exact Git blob SHA
→ receiver creates a clean candidate commit based directly on declared main
→ ChatGPT independently verifies candidate parent + index.html blob SHA
→ fast-forward main with force disabled
→ GitHub Pages publishes automatically
```

The receiver lives on the transport branch in:

```text
scripts/world_lab_transport_receiver.py
.github/workflows/world-lab-transport.yml
```

The manifest is the durable checkpoint and publication contract. It records at least:

```text
base_commit
destination
encoding
compression
ordered payload.NNN chunk names
expected_bytes
expected_git_blob_sha
candidate_branch
```

#### Multi-turn / interruption recovery

Transport progress must be recoverable from GitHub alone.

A resumed or completely new conversation should:

1. Inspect the transport branch and manifest.
2. Enumerate the already-persisted `payload.NNN` chunks.
3. Continue with the first missing chunk rather than retransmitting completed work.
4. Trigger reconstruction only when the declared chunk set is complete.
5. Treat receiver failure as a hard stop; never compensate by weakening byte/SHA checks.
6. Verify the generated candidate independently before touching `main`.
7. Confirm `main` has not moved away from the manifest's `base_commit`; if it has, stop and deliberately rebase/reissue the release rather than force-pushing.
8. Move `main` only by non-force fast-forward to the verified candidate.

No conversational memory is required for correctness. GitHub is the checkpoint store.

#### Verified failure behavior

The first real multi-turn publication intentionally demonstrated the safety property: reconstruction found the staged artifact was one byte short (`6,977,814` vs. `6,977,815`) and refused to publish it. After the missing final byte was restored, reconstruction succeeded and produced the exact expected blob:

```text
cb4412192eba404dac637856246a4e7acc922a5b
```

The verified clean publication commit was:

```text
ad66993de9d810f7f317ae521ddffed6d5c76791
```

Its parent was the previously captured `main`, and `main:index.html` was fetched again after the fast-forward and independently confirmed to have the same expected blob SHA.

The current receiver accepts both `base64 + gzip` and `utf-8 + none` transport manifests. Chunk size is a transport implementation detail and may be reduced whenever connector limits require it; the artifact itself does not need to be split, minified, refactored, or redesigned.

This matters because a connector limitation is not a reason to change the semantic architecture of an otherwise coherent executable artifact.

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
