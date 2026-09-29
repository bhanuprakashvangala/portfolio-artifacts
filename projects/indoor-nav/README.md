# Autonomous indoor navigation

BLE beacons and a Raspberry Pi running A* and Dijkstra pathfinding, paired with a Kotlin app giving turn-by-turn guidance indoors where GPS fails.

**Project status:** Completed

![Indoor navigation overview: BLE location to Route planning to Turn guidance](overview.svg)

Conceptual system diagram, drawn for this portfolio.

## Available materials

- Project overview and conceptual diagram in this directory.
- [Academic portfolio](https://bhanuprakashvangala.github.io/)

## Runnable companion example

[Standalone example repository](https://github.com/bhanuprakashvangala/indoor-navigation)

Compute a shortest route with Dijkstra’s algorithm. The included floor graph is synthetic. BLE positioning, the Android app, and physical guidance hardware are not bundled.

Requires Python 3.10+; no third-party packages. Run from the repository root:

```sh
python examples/navigation.py examples/data/floor.json entrance lab
```

[Source](../../examples/navigation.py) · [Tests](../../tests/test_examples.py) · [Input formats](../../examples/README.md)

## Scope and provenance

The companion code was newly written for this portfolio in September 2026. It is a minimal reference example, not a recovered historical implementation. The example data are synthetic, and their output is not a research result.
