# World Lab

A laboratory for rapidly probing systems across different world substrates.

## Continuous collaboration setup

This repository is being configured so that a human can work with ChatGPT conversationally while ChatGPT updates the executable artifact in GitHub and GitHub publishes the result automatically. The intended loop is:

```text
human intent
→ model inspects the artifact
→ model clarifies only what matters
→ model states the proposed delta
→ human confirms
→ model edits and validates the repository
→ GitHub deploys automatically
→ human refreshes the stable URL and plays
→ repeat
```

The human should not need to manually download, rename, save, upload, or move artifact files between iterations.

## GitHub / ChatGPT write access

### 1. Create or choose the repository

World Lab currently uses:

- repository: `bonoj/world-lab`
- default branch: `main`
- visibility: public

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

That proved this path:

```text
phone
→ ChatGPT conversation
→ GitHub connector
→ repository commit
```

Do not assume the setup works merely because ChatGPT can read the repository. Verify an actual write.

## Continuous deployment

**Status: not configured yet.**

The next step is to publish the executable World Lab automatically with GitHub Pages so every accepted repository update becomes available at a stable browser URL.

Once the deployment path is working and verified from the phone, this section will be replaced with the exact setup we used rather than speculative instructions.

Target path:

```text
phone
→ conversation
→ confirmed artifact mutation
→ GitHub commit
→ automatic GitHub Pages deployment
→ stable World Lab URL
→ refresh and inspect
```

## Collaboration rule

Repository access removes file-handling friction; it does not remove human authorship.

The working interaction remains:

1. Human expresses intent.
2. Model inspects current artifact and context.
3. Model resolves consequential ambiguity with the smallest useful clarification.
4. Model states the concrete proposed change.
5. Human confirms.
6. Model edits, validates, and commits.
7. Deployment produces executable evidence.
8. Human inspects that evidence and continues the conversation.

Inference can reduce communication cost. It should not silently replace human intention.

## Why this exists

The infrastructure should disappear underneath the collaboration. A person extending their World Lab should mostly experience two things:

- a conversation;
- the living executable toy.

Git, deployment, file transfer, and version bookkeeping are implementation machinery, not the interaction model.

---

This README is intentionally being written from a setup that has been performed and tested on a phone. Unverified deployment instructions are left explicitly unfinished until the deployment seam itself has been proven.
