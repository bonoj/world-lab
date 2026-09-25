#!/usr/bin/env python3
"""World Lab transport receiver.

Reconstructs an opaque release artifact from transport chunks, verifies it, and
creates a clean candidate commit based directly on the manifest's base commit.
It never updates main.

Manifest schema:
{
  "version": 1,
  "base_commit": "<40 hex sha>",
  "destination": "index.html",
  "encoding": "base64",
  "compression": "gzip",
  "chunks": ["payload.000", "payload.001", ...],
  "expected_bytes": 6977815,
  "expected_git_blob_sha": "<40 hex sha>",
  "candidate_branch": "world-lab-publish-candidate-..."
}
"""
from __future__ import annotations
import base64, gzip, hashlib, json, os, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TRANSPORT = ROOT / "transport"
MANIFEST = TRANSPORT / "manifest.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
SAFE_BRANCH = re.compile(r"^[A-Za-z0-9._/-]+$")

def fail(message: str) -> None:
    print(f"TRANSPORT ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)

def run(*args: str, cwd: pathlib.Path | None = None) -> str:
    p = subprocess.run(args, cwd=cwd or ROOT, text=True, capture_output=True)
    if p.returncode:
        print(p.stdout, end="")
        print(p.stderr, end="", file=sys.stderr)
        fail("command failed: " + " ".join(args))
    return p.stdout.strip()

if not MANIFEST.is_file():
    fail("transport/manifest.json is missing")

try:
    m = json.loads(MANIFEST.read_text("utf-8"))
except Exception as e:
    fail(f"invalid manifest JSON: {e}")

required = {
    "version", "base_commit", "destination", "encoding", "compression",
    "chunks", "expected_bytes", "expected_git_blob_sha", "candidate_branch"
}
missing = sorted(required - set(m))
if missing:
    fail("manifest missing keys: " + ", ".join(missing))
if m["version"] != 1:
    fail("unsupported manifest version")
if not HEX40.fullmatch(str(m["base_commit"])):
    fail("invalid base_commit")
if not HEX40.fullmatch(str(m["expected_git_blob_sha"])):
    fail("invalid expected_git_blob_sha")
if m["destination"] != "index.html":
    fail("destination must be index.html")
if m["encoding"] != "base64" or m["compression"] != "gzip":
    fail("receiver currently requires base64 + gzip")
if not isinstance(m["expected_bytes"], int) or m["expected_bytes"] < 0:
    fail("invalid expected_bytes")
if not isinstance(m["chunks"], list) or not m["chunks"]:
    fail("chunks must be a non-empty list")
if len(set(m["chunks"])) != len(m["chunks"]):
    fail("duplicate chunk names")
expected_names = [f"payload.{i:03d}" for i in range(len(m["chunks"]))]
if m["chunks"] != expected_names:
    fail("chunks must be contiguous ordered payload.NNN names")
if not SAFE_BRANCH.fullmatch(str(m["candidate_branch"])) or ".." in m["candidate_branch"]:
    fail("invalid candidate_branch")
if m["candidate_branch"] in {"main", "master"}:
    fail("candidate_branch may not be main/master")

encoded_parts = []
for name in m["chunks"]:
    p = TRANSPORT / name
    if not p.is_file():
        fail(f"missing chunk: {name}")
    encoded_parts.append(p.read_text("ascii").strip())

try:
    packed = base64.b64decode("".join(encoded_parts), validate=True)
except Exception as e:
    fail(f"base64 decode failed: {e}")
try:
    artifact = gzip.decompress(packed)
except Exception as e:
    fail(f"gzip decompression failed: {e}")

if len(artifact) != m["expected_bytes"]:
    fail(f"byte count mismatch: got {len(artifact)}, expected {m['expected_bytes']}")

blob_header = f"blob {len(artifact)}\0".encode("ascii")
actual_blob = hashlib.sha1(blob_header + artifact).hexdigest()
if actual_blob != m["expected_git_blob_sha"]:
    fail(f"Git blob SHA mismatch: got {actual_blob}, expected {m['expected_git_blob_sha']}")

# Ensure the declared base commit exists before constructing anything.
run("git", "cat-file", "-e", f"{m['base_commit']}^{{commit}}")

work = pathlib.Path(os.environ.get("RUNNER_TEMP", "/tmp")) / "world-lab-publish"
if work.exists():
    run("git", "worktree", "remove", "--force", str(work))
run("git", "worktree", "add", "--detach", str(work), m["base_commit"])
try:
    dest = work / m["destination"]
    dest.write_bytes(artifact)
    if run("git", "hash-object", str(dest), cwd=work) != m["expected_git_blob_sha"]:
        fail("git hash-object disagrees after writing destination")

    run("git", "config", "user.name", "github-actions[bot]", cwd=work)
    run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com", cwd=work)
    run("git", "add", "--", m["destination"], cwd=work)
    run("git", "commit", "-m", "Publish verified World Lab release", cwd=work)
    candidate = run("git", "rev-parse", "HEAD", cwd=work)
    parent = run("git", "rev-parse", "HEAD^", cwd=work)
    if parent != m["base_commit"]:
        fail("candidate parent is not declared base_commit")
    run("git", "push", "origin", f"HEAD:refs/heads/{m['candidate_branch']}", cwd=work)
    print(f"TRANSPORT OK: candidate={candidate} blob={actual_blob} bytes={len(artifact)}")
finally:
    run("git", "worktree", "remove", "--force", str(work))
