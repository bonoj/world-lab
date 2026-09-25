#!/usr/bin/env python3
"""World Lab opaque-artifact transport receiver.

Reconstructs one or more opaque artifacts from connector-safe chunks, verifies
every byte/blob identity, and creates a clean candidate commit based directly
on the manifest's declared base commit. It never updates main.

Manifest v2:
{
  "version": 2,
  "base_commit": "<40 hex sha>",
  "candidate_branch": "world-lab-publish-candidate-...",
  "artifacts": [
    {
      "destination": "assets/portals/foundry.png",
      "encoding": "base64",
      "compression": "none",
      "chunks": ["foundry/payload.000", ...],
      "expected_bytes": 123,
      "expected_git_blob_sha": "<40 hex sha>"
    }
  ]
}

Version 1 single-artifact manifests remain supported for historical releases.
"""
from __future__ import annotations
import base64, gzip, hashlib, json, os, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TRANSPORT = ROOT / "transport"
MANIFEST = TRANSPORT / "manifest.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
SAFE_BRANCH = re.compile(r"^[A-Za-z0-9._/-]+$")
SAFE_CHUNK = re.compile(r"^(?:[A-Za-z0-9._-]+/)*payload\.[0-9]{3}$")

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

def safe_destination(raw: object) -> str:
    value = str(raw)
    p = pathlib.PurePosixPath(value)
    if not value or p.is_absolute() or ".." in p.parts or value.startswith(".git/"):
        fail(f"unsafe destination: {value}")
    return value

def validate_artifact(a: object, label: str) -> dict:
    if not isinstance(a, dict):
        fail(f"{label} must be an object")
    required = {"destination","encoding","compression","chunks","expected_bytes","expected_git_blob_sha"}
    missing = sorted(required - set(a))
    if missing:
        fail(f"{label} missing keys: " + ", ".join(missing))
    a = dict(a)
    a["destination"] = safe_destination(a["destination"])
    if (a["encoding"], a["compression"]) not in {
        ("base64","none"), ("base64","gzip"), ("utf-8","none")
    }:
        fail(f"{label}: unsupported encoding/compression")
    if not isinstance(a["expected_bytes"], int) or a["expected_bytes"] < 0:
        fail(f"{label}: invalid expected_bytes")
    if not HEX40.fullmatch(str(a["expected_git_blob_sha"])):
        fail(f"{label}: invalid expected_git_blob_sha")
    chunks = a["chunks"]
    if not isinstance(chunks, list) or not chunks or len(set(chunks)) != len(chunks):
        fail(f"{label}: chunks must be a non-empty unique list")
    for name in chunks:
        if not isinstance(name, str) or not SAFE_CHUNK.fullmatch(name) or ".." in pathlib.PurePosixPath(name).parts:
            fail(f"{label}: unsafe chunk name: {name}")
    parent = str(pathlib.PurePosixPath(chunks[0]).parent)
    prefix = "" if parent == "." else parent + "/"
    expected = [f"{prefix}payload.{i:03d}" for i in range(len(chunks))]
    if chunks != expected:
        fail(f"{label}: chunks must be contiguous ordered payload.NNN names in one directory")
    return a

def reconstruct(a: dict) -> tuple[bytes,str]:
    parts = []
    for name in a["chunks"]:
        p = TRANSPORT / pathlib.PurePosixPath(name)
        if not p.is_file():
            fail(f"{a['destination']}: missing chunk: {name}")
        parts.append(p.read_bytes())
    if a["encoding"] == "utf-8":
        artifact = b"".join(parts)
    else:
        try:
            packed = base64.b64decode(b"".join(parts), validate=True)
        except Exception as e:
            fail(f"{a['destination']}: base64 decode failed: {e}")
        if a["compression"] == "gzip":
            try:
                artifact = gzip.decompress(packed)
            except Exception as e:
                fail(f"{a['destination']}: gzip decompression failed: {e}")
        else:
            artifact = packed
    if len(artifact) != a["expected_bytes"]:
        fail(f"{a['destination']}: byte count mismatch: got {len(artifact)}, expected {a['expected_bytes']}")
    blob = hashlib.sha1(f"blob {len(artifact)}\0".encode("ascii") + artifact).hexdigest()
    if blob != a["expected_git_blob_sha"]:
        fail(f"{a['destination']}: Git blob SHA mismatch: got {blob}, expected {a['expected_git_blob_sha']}")
    return artifact, blob

if not MANIFEST.is_file():
    fail("transport/manifest.json is missing")
try:
    m = json.loads(MANIFEST.read_text("utf-8"))
except Exception as e:
    fail(f"invalid manifest JSON: {e}")

if m.get("version") == 1:
    required = {"version","base_commit","destination","encoding","compression","chunks","expected_bytes","expected_git_blob_sha","candidate_branch"}
    missing = sorted(required - set(m))
    if missing: fail("manifest missing keys: " + ", ".join(missing))
    artifacts = [validate_artifact({k:m[k] for k in ("destination","encoding","compression","chunks","expected_bytes","expected_git_blob_sha")}, "artifact[0]")]
elif m.get("version") == 2:
    required = {"version","base_commit","candidate_branch","artifacts"}
    missing = sorted(required - set(m))
    if missing: fail("manifest missing keys: " + ", ".join(missing))
    if not isinstance(m["artifacts"], list) or not m["artifacts"]:
        fail("artifacts must be a non-empty list")
    artifacts = [validate_artifact(a, f"artifact[{i}]") for i,a in enumerate(m["artifacts"])]
    destinations = [a["destination"] for a in artifacts]
    if len(set(destinations)) != len(destinations):
        fail("duplicate artifact destinations")
else:
    fail("unsupported manifest version")

if not HEX40.fullmatch(str(m["base_commit"])):
    fail("invalid base_commit")
if not SAFE_BRANCH.fullmatch(str(m["candidate_branch"])) or ".." in str(m["candidate_branch"]):
    fail("invalid candidate_branch")
if m["candidate_branch"] in {"main","master"}:
    fail("candidate_branch may not be main/master")

reconstructed = [(a, *reconstruct(a)) for a in artifacts]
run("git","cat-file","-e",f"{m['base_commit']}^{{commit}}")

work = pathlib.Path(os.environ.get("RUNNER_TEMP","/tmp")) / "world-lab-publish"
if work.exists():
    run("git","worktree","remove","--force",str(work))
run("git","worktree","add","--detach",str(work),m["base_commit"])
try:
    for a,data,blob in reconstructed:
        dest = work / a["destination"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        if run("git","hash-object",str(dest),cwd=work) != blob:
            fail(f"{a['destination']}: git hash-object disagrees after write")
    run("git","config","user.name","github-actions[bot]",cwd=work)
    run("git","config","user.email","41898282+github-actions[bot]@users.noreply.github.com",cwd=work)
    for a,_,_ in reconstructed:
        run("git","add","--",a["destination"],cwd=work)
    run("git","commit","-m","Publish verified World Lab artifacts",cwd=work)
    candidate=run("git","rev-parse","HEAD",cwd=work)
    parent=run("git","rev-parse","HEAD^",cwd=work)
    if parent != m["base_commit"]:
        fail("candidate parent is not declared base_commit")
    run("git","push","origin",f"HEAD:refs/heads/{m['candidate_branch']}",cwd=work)
    summary=" ".join(f"{a['destination']}={blob}:{len(data)}" for a,data,blob in reconstructed)
    print(f"TRANSPORT OK: candidate={candidate} {summary}")
finally:
    run("git","worktree","remove","--force",str(work))
