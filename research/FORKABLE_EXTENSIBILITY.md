# Forkable Extensibility

Status: open research note  
Date: 2026-09-27

This note preserves an observation that may be worth investigating. It is not a specification, architectural commitment, workflow requirement, or claim that a general solution has been discovered.

## Observation

World Lab has become a relatively domain-agnostic place from which a human/model collaboration can extend a working system.

Its useful inheritance is not only source code. The repository increasingly carries several different forms of context:

- an executable realization;
- a durable semantic surface describing what the system currently is and what owns what;
- embedded semantic material useful to the current realization;
- change records preserving why important boundaries were earned;
- Git history preserving exact implementation lineage.

Together these may allow a fork to inherit more of the accumulated understanding of a system than source code alone provides.

## Working hypothesis

A fork may be able to inherit enough semantic context for a human/model team to substantially change a system without first reconstructing all of its architectural reasoning from implementation.

As divergent forks perform executable work, they may earn new semantic or architectural knowledge of their own.

Some of those discoveries may be useful to other descendants or to the parent lineage even when the implementations themselves should not be merged.

The interesting possibility is therefore not merely forkable code, but **forkable semantic inheritance**:

```text
fork
→ inherit implementation + semantic context
→ pursue a different goal
→ encounter executable evidence
→ earn local semantic knowledge
→ preserve that knowledge
→ compare with other descendants
→ selectively return useful discoveries
```

This is only a hypothesis.

## Why World Lab may be a useful substrate

World Lab does not currently require descendants to share one application domain or one universal simulation.

Its present architecture already favors:

- independent behavioral ownership;
- a quiet common substrate;
- identity earned through executable evidence;
- interaction only where composition earns it;
- semantic state separated from disposable rendering;
- explicit preservation of important architectural changes.

A meaningful fork could therefore diverge substantially rather than merely producing another visual variant of the same application.

That divergence is useful to the research question. If semantic inheritance remains useful when descendants become materially different systems, the result would be stronger than demonstrating reuse among closely related variants.

A fork need not remain recognizable as World Lab for the experiment to be informative.

## Questions to leave open

- What information does a fork actually need in order to extend a system coherently?
- Which knowledge belongs in the current semantic surface, which belongs in change archaeology, and which should remain implementation-local?
- Can a fork return a useful semantic discovery without returning its implementation?
- What evidence is sufficient to promote a local discovery into knowledge worth sharing across lineages?
- How should discoveries from many divergent forks be compared?
- Can models recognize equivalent architectural discoveries expressed through very different implementations?
- What would a semantic merge mean if no source-code merge is desirable?
- How should conflicting discoveries be represented without prematurely selecting a universal answer?
- How does a lineage avoid accumulating an instruction landfill as knowledge returns from descendants?
- What should remain local because it is contingent on one fork's domain or history?
- Can semantic inheritance make transient or regenerated implementations safer to replace?
- Can it let an inexperienced builder make deeper changes without first understanding the entire inherited architecture?
- Does the process still work when a fork changes domain enough that the parent's original vocabulary is no longer useful?
- What useful information is lost when semantic knowledge crosses from one lineage to another?

## Possible future probe

A simple future experiment would be to fork World Lab, give the fork a materially different goal, and allow a human/model team to evolve it independently.

After the fork has accumulated real executable evidence, inspect what it learned.

Then ask whether any discovery can be returned to the parent as useful semantic knowledge **without importing the fork's implementation**.

A successful result would not prove a general paradigm. It would provide one concrete specimen worth studying.

## Relationship to current repository surfaces

This note deliberately does not alter current World Lab authority.

- `SEMANTIC_SURFACE.md` describes durable present-tense semantic truth.
- Embedded semantic material helps the current executable realization understand itself.
- `/changes` preserves the intent, evidence, and outcome of changes that actually occurred.
- `/research` preserves questions and observations that appear worth remembering before they have earned promotion into the system.

If this research produces executable evidence, its conclusions should earn their destination rather than being promoted in advance.
