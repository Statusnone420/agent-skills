---
name: codebase-design
description: Designs deep modules with small interfaces, real seams, and interface-level tests. Use when shaping a module's API, restructuring code, or choosing test seams. Not for quick fixes.
---

# Codebase Design

Design **deep modules**: a lot of behavior behind a small interface, placed at a seam where callers and tests meet. Aim for leverage for callers, locality for maintainers, and tests that survive refactors.

## Rules

- **Depth is a property of the interface, not the implementation.** A deep module can be built from small, swappable parts; they just are not part of its interface. It may have internal seams for its own tests as well as the external seam at its interface.
- **Run the deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across callers, it earns its keep.
- **The interface is the test surface.** Callers and tests cross the same seam. If you need to test past the interface, the module is probably the wrong shape.
- **One adapter means a hypothetical seam; two make it real.** Add a seam only where something actually varies, usually production and test.
- **Shrink the interface.** Fewer methods, simpler parameters, more complexity hidden inside.
- **Accept dependencies instead of creating them.** Pass the payment gateway in rather than constructing it inside the function.
- **Return results instead of producing side effects** where the design allows it.

## Vocabulary

Use these terms exactly. Do not substitute "component", "service", "API", or "boundary".

- **Module:** anything with an interface and an implementation, at any scale: a function, class, package, or slice across tiers.
- **Interface:** everything a caller must know to use the module correctly: types, invariants, ordering, error modes, required configuration, and performance. Not just the signature.
- **Implementation:** the code inside a module. A small adapter can have a large implementation (a Postgres repository), and a large adapter a small one (an in-memory fake).
- **Depth:** leverage at the interface, meaning the behavior a caller or test can exercise per unit of interface it must learn. A module is **deep** when much behavior sits behind a small interface and **shallow** when the interface is nearly as complex as the implementation.
- **Seam** (Michael Feathers): a place where behavior can change without editing that place; where a module's interface lives. Choosing the seam is its own decision.
- **Adapter:** a concrete thing that fills an interface at a seam. It names a role, not the contents.
- **Leverage:** what callers gain from depth. One implementation pays back across many call sites and tests.
- **Locality:** what maintainers gain from depth. Change, bugs, knowledge, and verification concentrate in one place.

Rejected framings: depth as the ratio of implementation lines to interface lines, because it rewards padding; "interface" as only a type keyword or the public methods, because it is too narrow; "boundary", because it clashes with DDD's bounded context.

If the project keeps a `CONTEXT.md` glossary, use its domain terms alongside these.

## Going deeper

- To deepen a cluster of shallow modules by dependency type, read [DEEPENING.md](DEEPENING.md).
- To compare several radically different interfaces, read [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md). It starts three or more subagents, so use it only when the user asks for it.
