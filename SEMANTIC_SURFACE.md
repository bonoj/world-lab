# World Lab — Semantic Surface

## Role

World Lab is an executable spatial index of independent simulation laboratories.

It is not a menu dressed as a world, a miniature portfolio, or a promise that every laboratory participates in one shared simulation. Each lab keeps its own executable authority. World Lab provides a common physical substrate in which a small amount of project identity can be experienced before entering the project itself.

The current question is:

> How little project-specific behavior is required for several independent laboratories to become physically distinguishable while remaining members of the same world?

## Present world

Five neutral white presences occupy a ring inside a quiet bounded world: matte white-grey ground, warm-neutral enclosing dome, static light, soft shadows, and restrained distance fog.

Four presences correspond to executable labs:

- **Foundry**
- **Six Cities**
- **Vertical Accretion**
- **Orbital Construction**

The fifth presence is deliberately unassigned. It is a control and available future capacity, not a project waiting to be guessed.

The white marble is the common substrate. Project identity is added only where evidence from the source lab supports it.

## Interaction grammar

A presence can be foregrounded without entering its lab.

Foregrounding moves the presence toward the observer and transfers camera attention to it. Orbit and zoom remain available around the selected presence. Dismissing it restores both the presence and the observer to the exact pre-selection state.

Assigned presences expose two contextual actions:

- **ENTER LAB** — performs Camera Commit and navigates to the executable lab.
- **GITHUB** — opens project provenance.

The controls are viewport-owned rather than object-tethered. Physical inspection remains stable while interface actions remain legible.

Browser Back preserves the focused inspection state. World Lab owns departure; the destination lab owns arrival.

## Identity rule

A lab does not earn identity by receiving decorative miniatures, labels, or a synopsis.

Identity is expressed through the smallest physical behavior or construction vocabulary already supported by that lab's executable evidence.

This has produced four deliberately asymmetric identities.

### Six Cities — exchange

Six Cities retains the neutral marble and adds six small brass fittings with tiny glass containment domes. Deterministic five-bearing material packets travel along raised spherical arcs between fittings.

The identity is exchange across the world.

There is no miniature city scenery, explanatory overlay, universal logistics network, or implied connection to Orbital Construction.

### Vertical Accretion — access

Vertical Accretion carries a small worker, a finite stock of wooden steps, sparse torches, and persistent loose spoil.

The worker constructs access from the stockpile outward. Supply runs must traverse the step graph already built, so extending the route increases its own logistics cost. When the finite stock is exhausted, the worker dismantles the route in reverse and restages elsewhere.

The identity is embodied access accumulating through physical work.

The worker does not dig in World Lab. The spoil is retained as persistent external consequence because it became useful evidence beyond the marble itself.

### Foundry — retrieval

Foundry carries a tiny seated factory: warm beige body, orange cap, black receiving bay, and fifteen orange cube drones.

The drones retrieve actual Vertical Accretion spoil. They claim moving rocks without freezing them, pursue them through world space, pick up the same physical objects, route around obstructing marbles, and return through the live factory mouth. Rocks disappear only after entering the factory.

The identity is retrieval.

This is currently the only cross-marble material relationship. It exists because two independently earned behaviors composed cleanly: one system produces loose physical consequence and another already owns retrieval machinery. No processing output is implied.

### Orbital Construction — orbit

Orbital Construction's identity lives around its marble rather than on it.

A compact asymmetric station uses a reduced form of the source lab's earned vocabulary: pale pressure structures, orthogonal arms, habitation/workshop masses, dark readable collars, a vertical mast, very thin orange service routing, and sparse warm windows.

The station follows a slow wandering elliptical orbit with no visible orbit line while its attitude changes independently.

The identity is orbital construction occupying the space around a world.

It does not receive matter from Six Cities. A possible launcher relationship was considered and rejected because it would force a universal economy where none had been earned.

## Composition rule

World Lab permits interaction between labs but does not require it.

The important distinction is:

> Composition is evidence, not content.

The Vertical Accretion → Foundry relationship survives because existing behaviors produce a legible consequence when placed together. Six Cities and Orbital Construction remain independent because connecting them would currently add invented behavior rather than reveal existing capability.

Asymmetry is therefore healthy. Some presences interact. Some simply live in the same space.

Not every world needs to be busy.

## Architecture

The vestibule uses a deliberately small entity-component-system substrate.

Authoritative state flows:

```text
DATA
→ COMPONENTS
→ SYSTEMS
→ RENDER SYNC
→ THREE.JS
```

Transforms own world state. Three.js objects are render representations, not semantic authorities. Project-specific behavior is introduced through data/components only when behavior earns the distinction.

Current project identity components include exchange, descent/access, Foundry retrieval, and orbital behavior. This is not an invitation to build a general-purpose engine. Architecture expands only when executable evidence requires it.

## Observer and world boundaries

The dome and ground are physical observer bounds. Camera travel is not governed by an arbitrary zoom leash.

The ring is ordinary topology, earned through an earlier layout probe. The initial observer meets an edge of the five-presence ring rather than a single vertex.

The world intentionally contains no paths, pedestals, landmarks, environmental animation, or moving light. Empty space is useful. It provides perceptual separation and, when behavior earns it, actual simulation space between presences.

## Runtime invariants

- Startup, runtime, promise, WebGL, and shader failures fail visibly.
- Touch and mouse orbit/pan/pinch remain available.
- Foreground selection is reversible and restores observer state transactionally.
- Lab departure preserves Back/return continuity.
- Destination preconnect may begin on foreground focus; speculative destination execution does not.
- The common white marble remains recognizable beneath every project identity.
- The unassigned fifth presence remains semantically empty until evidence assigns it.
- Existing labs are not required to implement vocabulary invented by World Lab.

## What World Lab does not claim

World Lab is not currently:

- a unified resource economy;
- a simulation in which all labs causally interact;
- a canonical shared universe for the source projects;
- a replacement for the executable labs;
- a catalog of every mechanism those labs contain;
- a general ECS or world engine;
- a roadmap that assigns the fifth presence in advance.

The source laboratories remain authoritative for their own behavior and semantics.

## Working method

World Lab develops through the same evidence loop used by the laboratories it contains:

```text
human intention
→ smallest executable hypothesis
→ spatial experience
→ perceptual evidence
→ correction
→ repeated evidence
→ semantic / architectural promotion
→ next hypothesis
```

Ordinary implementation decisions belong to the implementation pass. Human inspection determines whether the resulting behavior earns permanence.

The executable is primary evidence. This semantic surface records the current interpretation of that evidence. Implementation archaeology belongs in the executable where it remains useful; this document describes the present-tense object rather than replaying its construction history.

## Current semantic center

Four projects now demonstrate four different relationships between a system and its world:

```text
Six Cities          exchanges across its world.
Vertical Accretion  builds access on its world.
Foundry             retrieves beyond its world.
Orbital Construction lives around its world.
```

Those verbs are descriptions of current executable evidence, not requirements for future projects.

World Lab is strongest when the common substrate stays quiet enough for those differences to be discovered rather than announced.
