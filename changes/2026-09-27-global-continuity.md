# WORLD LAB — GLOBAL CONTINUITY & NAVIGATION REPAIR

Status: pre-implementation expedition specification  
Date: 2026-09-27

This record preserves the intent, evidence, constraints, and finish line for a bounded World Lab change. It is not current runtime authority. The executable semantic surface describes what the system is now; this record describes why and how a change was undertaken. After implementation, append an OUTCOME section rather than rewriting this pre-implementation record.

## PRIMARY PROBLEM

Browser Back currently has a severe lifecycle failure.

Observed behavior:

1. User enters a lab from World Lab.
2. Browser Back briefly restores World Lab.
3. World Lab immediately navigates into the same lab again, as though ENTER LAB had been activated.
4. Subsequent Back navigation can produce a damaged-feeling history sequence, including skipping expected surfaces.

Inspection identified the likely direct cause:

- Camera Commit is represented by live `entryMotion`.
- When the commit completes, `finishEntry()` navigates to the destination.
- The completed departure transaction is not cleared before navigation.
- If World Lab is preserved through BFCache, it can return with that completed `entryMotion` still live.
- The resumed animation loop can therefore invoke `finishEntry()` again and immediately redepart.

Repair this decisively.

### Navigation invariant

**A navigation/departure transaction may execute at most once.**

Before external navigation occurs, all executable departure intent must be consumed/cleared.

Navigation intent is ephemeral runtime command state. It must never be part of persistent WorldState.

Browser Back from a lab must reliably produce:

`Lab → World Lab`

and leave the user in World Lab until they explicitly choose another action.

A subsequent Back should continue naturally to the page that preceded World Lab, including the landing page when that was the user's route.

Do not trap Back, synthesize replacement history, or fight the browser history stack unless executable evidence demonstrates that ordinary browser navigation cannot satisfy this contract.

---

# SECONDARY PROBLEM: WORLD CONTINUITY

The existing return-snapshot mechanism is too narrow.

It primarily preserves observer/focus state for navigation reconstruction, while meaningful simulation state depends heavily on the browser retaining the live document.

World Lab is now a small persistent simulated place. Returning from a lab or reconstructing World Lab should preserve meaningful world evolution.

Examples include:

- Vertical Accretion spoil rocks already produced and lying/falling in world space.
- Vertical Accretion worker/path progress, stock, torches, and current build/deconstruct cycle.
- Foundry drones already launched.
- Drone cargo/claims and rocks being retrieved.
- Six Cities exchange progression and deterministic scheduling state where meaningful.
- Orbital Construction's evolving orbital state.
- Observer/camera state and foreground selection.

The solution should be a **single global WorldState persistence boundary**, not scattered ad-hoc persistence calls and not a requirement that every rendered object become an individually persisted ECS entity.

---

# DESIGN PRINCIPLE

Persist **authoritative semantic/simulation state**, not rendered representation.

Three.js objects are views and may be reconstructed.

Examples:

A spoil rock may require:

- stable persistence identity if referenced by another system;
- position;
- velocity;
- sleep/settled state;
- delivery/claim state where appropriate.

It does not require serialization of its `THREE.Mesh`.

A Foundry drone may require:

- simulation state;
- position;
- cargo/target rock identity;
- relevant route/progress state;
- whatever is minimally necessary to resume coherently.

It does not require serialization of its `THREE.Group`.

Likewise, persistent identity should be introduced only where relationships across restoration require it. Do not turn every transient visual object into heavyweight globally managed persistence merely for architectural symmetry.

---

# GLOBAL WORLDSTATE

Establish one versioned global snapshot model.

The exact representation is an implementation decision, but conceptually it owns:

## Observer / vestibule interaction

- camera position/orientation or equivalent authoritative observer representation;
- orbit/target state;
- foregrounded presence;
- pre-selection ObserverReturn state when applicable;
- whatever is required to restore the same inspectable vestibule state.

## Vertical Accretion identity

Persist the smallest state required to reconstruct meaningful continuity, including as applicable:

- current route/run;
- worker phase and progress;
- stock;
- laid steps/path;
- torch infrastructure;
- spoil rocks and their physical state;
- deterministic RNG progression.

## Foundry identity

Persist the smallest state required to reconstruct:

- launched drones;
- drone behavioral states;
- drone positions;
- target/claim relationships;
- carried rocks;
- relevant return path/progress;
- launch scheduling;
- relationships to surviving spoil.

Foundry and Vertical Accretion share physical consequences through spoil. Their persisted state must therefore reconstruct coherent cross-system relationships rather than two contradictory copies of the same rocks.

## Six Cities identity

Preserve enough state that restoration does not perceptibly reset the identity simulation.

Consider:

- deterministic RNG state;
- active exchanges;
- route reservations;
- bearing progression;
- next scheduling point.

Do not serialize disposable packet meshes.

## Orbital Construction identity

Preserve whatever evolving phase/state is necessary to prevent a reconstruction from visibly resetting its motion.

## Metadata

Include:

- schema/version identifier;
- whatever validation information is useful for safely rejecting incompatible stale snapshots.

Do not include active navigation/departure commands.

---

# TIME

The current simulation uses `performance.now()` extensively.

Absolute `performance.now()` values are not persistent state.

Normalize persisted temporal state into reconstructable values such as:

- elapsed progress;
- remaining delay;
- phase;
- simulation-relative time;

or another small coherent mechanism.

Restoration should not accidentally interpret timestamps from a previous document lifetime against a new `performance.now()` epoch.

Do not create a general-purpose simulation clock unless the existing systems actually need one.

---

# RNG

Deterministic systems should continue their sequence across reconstruction where that continuation is perceptually or behaviorally meaningful.

The existing seeded RNG implementation hides its internal state inside a closure. Adjust this minimally if necessary so relevant RNG state can be snapshotted and restored.

Do not introduce a large random-number framework.

---

# STORAGE / LIFETIME

Choose browser-local storage semantics appropriate to this world.

The immediate required continuity boundary is:

- ordinary live use;
- departure to a lab;
- Browser Back;
- BFCache restoration;
- document reconstruction/reload during the same meaningful visit.

Prefer the smallest storage lifetime that satisfies the experience.

Do not accidentally turn World Lab into a permanent save game across indefinite future visits unless that behavior is deliberately justified.

A fresh visit must remain distinguishable from restoration of an existing world session.

---

# BFCACHE

BFCache and serialized reconstruction should no longer represent two fundamentally different semantic models.

BFCache may preserve the live world as an optimization.

However, the versioned WorldState defines what **continuity means**.

On BFCache restoration:

- retain valid live simulation state when appropriate;
- ensure no completed navigation transaction can resume;
- reconcile/refresh persistence bookkeeping as needed.

On reconstruction:

- rebuild the equivalent meaningful world from WorldState.

Do not destroy good live BFCache state merely to force serialization through an unnecessary round trip.

---

# SAVE POLICY

Do not serialize the entire world every animation frame.

Choose a small coherent persistence policy.

Reasonable triggers may include:

- meaningful simulation mutations;
- bounded throttled checkpoints while the world is active;
- immediately before lab/GitHub departure;
- page lifecycle events where reliable;
- important interaction transitions.

Correctness and simplicity matter more than microscopic write optimization, but avoid obviously pathological storage churn.

---

# RESTORATION ORDER

Pay attention to dependencies.

In particular:

Vertical Accretion can create spoil.

Foundry can claim, carry, and remove that spoil.

Therefore restoration must reconstruct shared physical state and stable relationships in an order that prevents:

- duplicate rocks;
- claims referring to nonexistent rocks;
- two drones claiming the same rock;
- carried rocks reappearing on the floor;
- delivered rocks resurrecting.

Similarly, rendered views should be rebuilt only after the semantic state they represent exists.

---

# FAILURE BEHAVIOR

Preserve World Lab's existing visible diagnostic philosophy.

Malformed, incompatible, or partially stale persistence must not silently corrupt the world.

Prefer:

- validation;
- safe fallback to a fresh world where necessary;
- visible diagnostic information for genuine implementation/runtime failures.

A bad saved snapshot must never make World Lab permanently unusable.

---

# SEMANTIC SURFACE

Update the embedded vestibule semantic documentation after implementation.

Remove or revise claims that are no longer true, particularly the current narrow BACK / RETURN CONTINUITY model in which BFCache live state is authoritative and a one-shot return snapshot handles reconstruction.

Document the earned architecture:

- global WorldState;
- semantic-state persistence;
- disposable rendering;
- shared spoil identity where applicable;
- navigation transactions are ephemeral and exactly-once;
- BFCache and reconstruction obey the same continuity contract.

Preserve useful archaeology about the old failure and why it was replaced.

---

# VALIDATION

Do not stop after code appears correct.

Exercise the implementation conceptually and, where executable tooling permits, directly against the following cases.

## Navigation regression

Repeatedly:

`Landing → World Lab → Foundry → Back → World Lab`

`World Lab → Six Cities → Back → World Lab`

`World Lab → Vertical Accretion → Back → World Lab`

`World Lab → Orbital Construction → Back → World Lab`

Then:

`World Lab → Back → Landing`

There must be:

- no automatic re-entry;
- no phantom ENTER LAB activation;
- no double-Back behavior;
- no artificial history trapping;
- no lost landing-page history entry caused by World Lab.

## Simulation continuity

Allow the vestibule to evolve enough that:

- Vertical Accretion has materially changed its path;
- spoil exists away from its source;
- Foundry drones are active;
- at least some rocks are claimed/carried/delivered;
- other identity simulations have progressed.

Depart to a lab and return.

The world should continue from the meaningful prior state rather than restarting.

## Reconstruction

With materially evolved world state, force document reconstruction/reload within the intended persistence lifetime.

Verify that the reconstructed world is semantically equivalent:

- path/stock state preserved;
- rocks preserved;
- drones/claims/cargo coherent;
- no duplicate or resurrected spoil;
- deterministic systems do not obviously reset;
- observer/focus state restores appropriately;
- no navigation intent executes.

## Repetition

Perform multiple departure/return cycles from the same evolving world.

Continuity must remain stable rather than accumulating stale snapshots, duplicate entities, or history entries.

---

# NON-GOALS

Do not:

- redesign World Lab;
- alter its visual composition;
- add user-facing save/load UI;
- create accounts/cloud persistence;
- create a generic save-game engine;
- make every visual object a persisted ECS entity;
- refactor unrelated simulation code for elegance;
- modify individual destination labs;
- change their URLs;
- add speculative features;
- solve persistence beyond the lifetime actually required by this experience.

---

# FINISH LINE

The expedition is complete when:

1. Browser Back no longer causes World Lab to redepart automatically.
2. Navigation behaves like ordinary trustworthy browser navigation.
3. World Lab owns one coherent versioned persistence model.
4. Meaningful simulation evolution survives lab departure/return.
5. Reconstruction can restore that meaningful state without relying on BFCache.
6. Cross-system spoil/drone relationships remain coherent.
7. Navigation intent is provably outside persistent state and exactly-once.
8. Existing visible diagnostics remain intact.
9. The embedded semantic surface accurately documents the resulting architecture.
10. No unrelated visual or behavioral redesign has been introduced.

## OUTCOME

Implemented and published to `main/index.html` on 2026-09-27.

The expedition repaired the Browser Back failure and established a global continuity boundary without redesigning the vestibule.

### What shipped

- Camera Commit/departure is ephemeral command state and is consumed before external navigation can replay it.
- Departure checkpoints the stable inspection state before Camera Commit; lifecycle saves cannot overwrite that checkpoint with the terminal commit pose.
- BFCache return clears ephemeral motion and preserves the live simulation while reconciling the saved observer state.
- A versioned, session-scoped `WorldState` now persists authoritative semantic state rather than Three.js representation.
- Vertical Accretion continuity includes worker/path/run state, deterministic RNG progression, and spoil.
- Spoil received stable semantic identity where cross-system relationships require it.
- Foundry continuity includes drones, cargo/claims, routes, scheduling, and references to the shared spoil identities rather than duplicate ownership of rocks.
- Six Cities continuity includes deterministic RNG/scheduling and in-flight exchange progression.
- Rendering remains disposable and reconstructable from semantic state.
- Restore validation rejects incoherent relationships such as duplicate spoil claims, and failed application rolls back rather than leaving a hybrid partially restored world.
- The embedded semantic surface was updated with the new continuity contract and archaeology of the BFCache/navigation failure.

Orbital Construction did not earn additional persisted state in this pass; its current vestibule motion remains time-derived rather than an accumulated simulation relationship.

### Executable evidence

The hardened candidate was syntax-checked before publication and transported to GitHub with exact full-text equality verification. Published blob:

`d4a0888f0f1fa505234cce58abafed7a2dbfdbb4`

Publication commit:

`78c231024e5d7e677ffd1d8f7239f0945bac2efc`

Human abuse testing after publication confirmed the original navigation behavior was materially improved and that drone/simulation state now survives the tested departure/return path.

### Architecture earned

The useful boundary is now explicit:

- **simulation state** owns what has happened;
- **rendering** is a disposable view of that state;
- **navigation/lifecycle** checkpoints and transports the observer but does not become world ontology.

The important cross-system result is the Vertical Accretion → Foundry relationship. The systems remain separately owned, but they interact through the persistent semantic identity of spoil: Vertical Accretion produces it, Foundry may claim/carry/remove it, and WorldState preserves the relationship. Persistence therefore did not require collapsing the two simulations into one subsystem or coupling them through rendered objects.

This outcome is evidence for the broader World Lab practice: preserve semantic boundaries and the reasons they were earned close enough to the executable that a later human or model can extend the system without having to rediscover them from implementation alone.
