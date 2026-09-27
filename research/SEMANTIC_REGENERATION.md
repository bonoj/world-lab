# Semantic Regeneration

Status: open research note  
Date: 2026-09-27

This note preserves a recurring research question. It is not a claim that implementation can currently be discarded safely, nor a specification for a regeneration system.

## Observation

Across several executable experiments, implementation has increasingly behaved as one realization of a more durable semantic object.

Useful continuity has come from preserving things such as:

- what exists;
- what owns what;
- which relationships are authoritative;
- which invariants have been earned;
- what evidence caused an architectural boundary to exist;
- which implementation details are merely current representation.

This raises the possibility that some implementations may eventually become substantially more transient or regenerable without making the system itself transient.

## Working hypothesis

If a repository preserves enough durable semantic truth and executable evidence, a model may be able to regenerate, replace, or substantially restructure an implementation while retaining the system's earned identity.

The interesting loop is not source generation by itself:

```text
experience
→ semantic interpretation
→ implementation / regeneration
→ executable evidence
→ revised semantic interpretation
```

The semantic description would not be a complete substitute for executable evidence. Regeneration would remain a hypothesis until the resulting system was experienced and validated.

## Questions to leave open

- What semantic information is sufficient to regenerate a coherent realization?
- Which implementation details are actually semantic constraints in disguise?
- How can a regenerated artifact demonstrate that it preserved meaning rather than merely matching visible output?
- Which invariants should be tested mechanically and which require human experience?
- How much implementation archaeology is useful to a successor realization?
- When should old implementation be treated as evidence, reference, or disposable residue?
- Can radically different architectures realize the same semantic surface?
- How should a semantic surface change when regeneration exposes assumptions that were never documented?
- Can regeneration preserve emergent behavior without freezing accidental implementation?
- At what point does a regenerated system become a new descendant rather than the same system?
- How should provenance connect semantic claims to the executable evidence that earned them?

## Possible future probe

Take a bounded executable system with a mature semantic surface and change record.

Give a fresh model the durable semantic material and only the minimum implementation evidence deliberately chosen for the experiment. Ask it to produce a new realization.

Compare the resulting behavior with the original through executable probes and human inspection.

The useful result would not be visual similarity. It would be evidence about which semantic information survived architectural translation and which important truths had existed only implicitly in the old implementation.

## Relationship to current repository surfaces

This question is broader than World Lab's current architecture. World Lab is simply one place where the distinction between semantic authority and disposable representation has become visible.

No current World Lab implementation is declared disposable by this note.
