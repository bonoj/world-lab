# Executable Evidence

Status: open research note  
Date: 2026-09-27

This note preserves a development pattern repeatedly encountered in the labs. It is not a universal engineering methodology and does not claim that every architectural decision must be discovered experimentally.

## Observation

Several useful architectural boundaries were not fully known before implementation.

They emerged through a repeated sequence:

```text
intention
→ smallest useful executable hypothesis
→ experience / inspection
→ failure or successful composition
→ revised mechanism
→ repeated evidence
→ semantic or architectural promotion
```

Examples have included interaction grammar, simulation vocabulary, physical relationships, lifecycle behavior, ownership boundaries, and persistence identity.

In these cases, executable behavior did more than verify an implementation. It produced information that changed what the system was understood to be.

## Working hypothesis

Executable artifacts can function as research apparatus.

A proposed mechanism is implemented narrowly enough to expose the relevant question. Its behavior then provides evidence for or against semantic vocabulary, architectural boundaries, and future constraints.

Under this model, architecture is neither wholly designed in advance nor merely allowed to emerge accidentally from code. Some boundaries are deliberately withheld until evidence earns them.

## Questions to leave open

- What kinds of architectural questions benefit from executable investigation?
- What is the smallest useful executable hypothesis for a given question?
- What counts as enough evidence to promote an observation into an invariant or architectural boundary?
- How should failed mechanisms be preserved so later models do not rediscover them unnecessarily?
- When is human perceptual inspection legitimate evidence, and when is mechanical validation required?
- How should deterministic probes, adversarial tests, and ordinary use complement one another?
- How can an experiment remain open-ended without becoming unbounded implementation?
- How do we distinguish an earned mechanism from a local workaround that merely survived one probe?
- When should architecture be decided before implementation because experimentation would be unsafe, expensive, or misleading?
- Can executable evidence be compared across divergent implementations?
- How should uncertainty remain visible after a mechanism has been provisionally promoted?

## Possible future probe

Choose one architectural question before implementation and explicitly record:

- the uncertainty;
- the smallest executable probe;
- the observations expected to distinguish competing interpretations;
- the conditions under which a mechanism would earn promotion.

Run the experiment without requiring the eventual architecture to match the initial hypothesis.

Afterward, compare the pre-experiment question, executable evidence, and resulting semantic change. Repeat across different domains to see whether the method remains useful outside the kinds of simulations that first exposed it.

## Relationship to current repository surfaces

World Lab and its source laboratories contain examples of this pattern, but this note does not promote those examples into a general rule.

The repository's `/changes` records are a useful place to preserve cases where executable evidence actually changed an important boundary. This research note asks what can be learned from that practice across many such cases.
