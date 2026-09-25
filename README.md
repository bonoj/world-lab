# World Lab

A laboratory for rapidly probing systems across different world substrates.

## Continuous collaboration setup

This repository is configured so that a human can work with ChatGPT conversationally while ChatGPT updates the executable artifact in GitHub and GitHub Pages publishes the accepted `main` branch automatically.

The normal loop is:

```text
human intent
→ model inspects the artifact
→ model clarifies only what matters
→ model edits and validates
→ verified candidate
→ accepted candidate fast-forwards main
→ GitHub Pages publishes automatically
→ human refreshes the stable URL and plays
→ repeat
```

The infrastructure must adapt to the artifact. Connector limits are not a reason to split, minify, refactor, or otherwise redesign a coherent executable merely to make transport easier.

## Live site

World Lab is published at:

https://bonoj.github.io/world-lab/

This is a project Pages site, so `/world-lab/` is part of the URL.

Repository:

- `bonoj/world-lab`
- default branch: `main`
- Pages source: `main` / root
- executable entry point: `/index.html`

## GitHub / ChatGPT write access

World Lab uses the ChatGPT Codex Connector installed on the GitHub account with access to this repository. Read access alone does not prove write access; the original setup was verified with a harmless repository write before publishing real work.

The first end-to-end Pages deployment was confirmed from a phone on September 24, 2026.

## Artifact transport

### Why there is a receiver

Small UTF-8 repository writes are straightforward through the connector. Large self-contained executables and opaque/binary artifacts need a transport that does not make connector request size or representation constraints part of the artifact architecture.

The first roughly 1 MB World Lab publication succeeded by obtaining essentially the complete HTML as text and supplying that string to GitHub's Git-object APIs:

```text
artifact text
→ create_blob
→ create_tree
→ create_commit
→ update_ref
```

That did **not** prove a dedicated conversation-file → Git-blob adapter.

When World Lab grew to roughly 7 MB, a one-shot connector call was no longer a reliable transport seam. The repository therefore gained a GitHub Actions receiver that reconstructs artifacts from small connector-safe chunks and verifies the result before creating a candidate commit.

### Universal opaque-artifact transport

The current receiver is:

```text
scripts/world_lab_transport_receiver.py
```

The workflow is:

```text
.github/workflows/world-lab-transport.yml
```

The receiver supports both the historical v1 single-artifact manifest and the current **v2 multi-artifact manifest**.

A v2 manifest can transport one or more opaque artifacts to arbitrary safe repository paths:

```json
{
  "version": 2,
  "base_commit": "<40-hex commit>",
  "candidate_branch": "world-lab-publish-candidate-example",
  "artifacts": [
    {
      "destination": "index.html",
      "encoding": "utf-8",
      "compression": "none",
      "chunks": ["html/payload.000", "html/payload.001"],
      "expected_bytes": 123456,
      "expected_git_blob_sha": "<40-hex Git blob SHA>"
    },
    {
      "destination": "assets/example.bin",
      "encoding": "base64",
      "compression": "none",
      "chunks": ["binary/payload.000"],
      "expected_bytes": 789,
      "expected_git_blob_sha": "<40-hex Git blob SHA>"
    }
  ]
}
```

Supported representations are:

- `utf-8` + `none`
- `base64` + `none`
- `base64` + `gzip`

Chunks must be contiguous ordered `payload.NNN` files within one artifact directory. Binary data is carried as base64 text; the receiver reconstructs the original bytes on the GitHub runner.

### Verification and safety contract

For every artifact the receiver:

1. validates destination and chunk paths;
2. reconstructs the exact bytes;
3. verifies `expected_bytes`;
4. computes the canonical Git blob SHA over `blob <length>\0<bytes>`;
5. refuses publication if the SHA differs;
6. creates a detached worktree from the manifest's exact `base_commit`;
7. writes only the declared destinations;
8. independently checks each destination with `git hash-object`;
9. creates one clean candidate commit whose parent must equal the declared base;
10. pushes only the declared candidate branch.

The receiver **never updates `main`**. Promotion to `main` is a separate explicit fast-forward after the candidate has been inspected and verified.

This makes interrupted conversations recoverable: persisted GitHub chunks and manifests are checkpoints. Conversation continuity is not part of publication correctness.

### Proven large-release path

The approximately 7 MB Six Cities World Lab release proved the receiver end-to-end. A first run failed safely on a one-byte mismatch. After the missing final newline was restored, reconstruction succeeded, the resulting `index.html` Git blob matched the expected SHA exactly, and the verified candidate was fast-forwarded to `main`.

That failure is part of the proof: byte-count and blob-identity gates stopped an inexact artifact from being published.

### Binary ingress boundary

The universal receiver can reconstruct binary artifacts exactly **once their bytes have been represented as connector-safe base64 chunks**.

A separate experiment with GitHub issue image attachments established a current ingress limitation: issue attachments are exposed as `github.com/user-attachments/assets/...`, while the available connector operations do not currently provide a proven path from those attachment bytes directly into a Git blob or the receiver's base64 chunk strings.

That is an **ingress limitation, not a receiver limitation**.

For binary files already on the human's device, direct GitHub upload is therefore a valid practical ingress path. Do not redesign or revert the universal receiver because of this boundary. If a future connector exposes file/stream-aware Git writes, that ingress path can be replaced without changing the receiver's verification model.

## GitHub Pages

GitHub Pages publishes `main` / root automatically. No Pages-specific build system is required for the self-contained World Lab executable.

The publication path is:

```text
verified candidate
→ fast-forward main
→ GitHub Pages
→ https://bonoj.github.io/world-lab/
```

Pages publication is asynchronous and is not the low-latency development runtime.

## Collaboration rule

Repository access removes file-handling friction; it does not remove human authorship.

Inference can reduce communication cost. It should not silently replace human intention. Ordinary implementation details can be resolved by the model, while consequential semantic changes remain explicit.

## Why this exists

The infrastructure should disappear underneath the collaboration. A person extending World Lab should mostly experience:

- a conversation;
- the living executable toy.

Git, deployment, file transfer, reconstruction, hashing, and version bookkeeping are implementation machinery rather than the interaction model.

---

This README records mechanisms that were actually exercised. Where a transport path is unproven, it is labeled as such rather than presented as established behavior.
