# Current Working Model

Status: provisional research synthesis  
Date: 2026-09-27

This note preserves our current understanding of the development practice that has emerged across World Lab and its related experiments.

It is not a manifesto, a claim of novelty, a universal software-development method, or current World Lab semantic authority.

It should be revised when our practice changes materially or executable evidence makes this description false.

## Current orientation

The implementation is not only a product to be specified and produced.

It can also be a shared research apparatus through which a human and a model discover what the system should become.

A recurring loop has been:

```text
human consequential intent
→ deliberately bounded but incomplete hypothesis
→ model implementation with ordinary engineering autonomy
→ executable experience
→ human/model inspection
→ evidence
→ semantic interpretation
→ architectural or vocabulary promotion where earned
→ durable preservation
→ next hypothesis
```

The important property is that some of the semantic truth does not exist before implementation.

The executable can reveal:

- distinctions that were not previously visible;
- vocabulary that becomes useful only after behavior exists;
- ownership boundaries exposed by composition or failure;
- invariants earned through repeated evidence;
- plausible abstractions that turn out to be wrong;
- relationships that become meaningful only when independent systems meet.

The purpose of semantic preservation is therefore not merely to constrain future implementation to a plan written in advance. It also preserves what implementation and experience taught us.

## Division of authority

The collaboration does not require the human to choose every implementation detail, nor the model to decide every consequential semantic question.

The current useful division is approximately:

### Human

The human owns salience and consequential intent.

Human attention is concentrated on:

- what is worth pursuing;
- experiential judgment;
- materially different semantic directions;
- consequences important enough to require explicit choice;
- whether an observed behavior has earned continued attention.

### Model

The model receives substantial autonomy over ordinary realization and low-salience semantic maintenance.

This can include:

- implementation details;
- bounded engineering decisions;
- diagnosis and repair;
- keeping semantic surfaces coherent;
- preserving research questions and change archaeology;
- carrying context at a granularity beneath the human's useful attention threshold;
- surfacing an issue when it becomes consequential.

This delegation is useful because it is inspectable and reversible. It is not a requirement for uncritical trust.

### Executable evidence

The executable mediates between intention and interpretation.

It can confirm a hypothesis, falsify it, expose a missing distinction, or produce behavior neither collaborator had fully specified.

Human experience of the executable is itself evidence where the question is experiential or perceptual. Mechanical probes, deterministic tests, diagnostics, and adversarial inspection provide other forms of evidence where appropriate.

The required standard of review depends on consequence and domain. This practice does not imply that low-salience model maintenance is acceptable for every kind of software.

## Repository as externalized continuity

The repository increasingly carries collaboration context that would otherwise have to survive in human memory, model conversational context, or implementation archaeology.

Current surfaces have different jobs.

### Semantic Surface

`SEMANTIC_SURFACE.md` preserves durable present-tense semantic truth:

- what the system is;
- what owns what;
- which boundaries matter;
- which invariants and relationships a successor realization should preserve.

It is not a copy of the executable's embedded documentation.

### Embedded semantic material

The executable may carry semantic material useful to understanding and extending that particular realization.

This can include implementation-local invariants and archaeology whose proximity to the running artifact is valuable.

### Changes

`/changes` preserves consequential transitions:

- the problem or uncertainty;
- relevant evidence and constraints;
- the intended finish line;
- the outcome actually earned.

It explains why an important truth or boundary exists without forcing the present-tense Semantic Surface to replay history.

### Research

`/research` preserves observations and questions that are important enough not to lose but have not earned promotion into current system authority.

Research notes may remain dormant indefinitely. They should not constrain ordinary work merely because they exist.

### Git

Git preserves exact implementation lineage beneath these semantic surfaces.

It answers a different question from all of them: what bytes changed, when, and along which lineage?

## Human attention and semantic volume

A model can cheaply maintain useful context below the granularity at which human review remains productive.

The current working principle is:

> Human attention should scale with consequence, not artifact volume.

This creates the possibility of remembering more than the human should be required to actively remember.

The goal is not maximal documentation. Low-salience knowledge should live in appropriately typed, discoverable surfaces rather than accumulate in one mandatory context document.

Evidence or future relevance can promote dormant material back into human attention when it becomes consequential.

## Semantic inheritance

If repository context is sufficiently durable and legible, a fresh model or human/model team may be able to inherit more than source code.

They may inherit:

- present semantic truth;
- earned boundaries;
- important historical reasons;
- unresolved research questions;
- executable evidence;
- exact implementation lineage.

This creates the possibility that increasingly transient implementations can remain coherent because important system knowledge survives outside any one realization.

It also raises the open possibility of forkable semantic inheritance: divergent descendants may earn useful architectural knowledge that can travel between lineages even when their implementations should not merge.

That possibility remains research, not established capability.

## What this model currently does not claim

This working model does not claim that:

- specifications are unnecessary;
- architecture should never be designed before implementation;
- executable experimentation is appropriate for every decision;
- human review can be skipped regardless of consequence;
- semantic documentation can replace tests or working software;
- models can reliably regenerate arbitrary systems from semantic surfaces;
- every project should use these repository surfaces;
- forked semantic discoveries can already be merged coherently;
- the present vocabulary is final.

The practice should remain subordinate to evidence.

## Current compact form

As presently understood:

```text
Human owns consequential intent and salience.
Model owns much of ordinary realization and low-salience semantic housekeeping.
Executable work produces evidence available to both.
Semantic surfaces preserve what that evidence teaches.
Repository history preserves how realizations changed.
Research preserves questions before they deserve authority.
Future collaborators inherit the result and continue the loop.
```

The implementation is therefore neither merely the output of the collaboration nor the sole source of truth.

It is one of the instruments through which the collaboration learns.
