# Companion examples

Run commands from the repository root with Python 3.10 or newer. These examples use only the standard library and run offline. They were added for the portfolio in September 2026; none is the original research implementation.

## Prediction evaluation

```sh
python examples/evaluate.py examples/data/predictions.csv
```

CSV columns: `id,group,split,language,true,predicted`. Each sample ID must be unique. `group` identifies the unit that must stay within a split, such as a user or patient. `split=test` rows are scored; all rows participate in the split-leakage check. For a monolingual or imaging task, use a fixed language value such as `und`.

Output includes overall and per-language accuracy, macro-F1, per-label F1, and confusion counts (rows = true labels, columns = predictions). Each group uses the global union of test labels for comparable macro-F1; a label absent in both truth and predictions receives zero F1. Evaluation is linear in the number of records plus the size of the reported confusion matrices. The tool catches identifier-level leakage, not duplicates with different IDs or semantic contamination. Supply the complete split manifest to check separation.

The included five rows are synthetic sentiment predictions, not clinical examples or outputs of the original KOO model.

## Indoor route planning

```sh
python examples/navigation.py examples/data/floor.json entrance lab
```

The JSON file maps each node name to its outgoing neighbors and nonnegative distances. Edges are directed; include both directions for a two-way corridor. Unknown nodes, nonfinite/negative weights, and disconnected destinations produce errors. The example returns `entrance → hall → lab`, distance `9`.

Dijkstra’s algorithm uses a heap and predecessor links instead of copying full paths during search: O((V + E) log V) time for a simple graph. This is a route-planning component, without BLE localization, live obstacle detection, or hardware integration.

## Persistent context retrieval

```sh
python examples/memory.py notes.db add "Kubernetes deployment notes"
python examples/memory.py notes.db search "deployment"
```

Stores notes in a local SQLite FTS5 index and returns ranked matches as JSON. Unicode query terms are quoted and parameterized. Empty searches return no results; blank notes are rejected. This is lexical search, not vector retrieval. The local database is excluded from version control. A Python build with SQLite FTS5 support is required (verified with Python 3.12 on Windows).

## Adaptive routing

```sh
python examples/routing.py --rounds 1000 --seed 7
```

The UCB1 router explores each model, then selects using the empirical mean reward plus an exploration bonus. Rewards must be finite and within [0, 1]. Selection is O(number of models); each update uses an O(1) incremental mean. The included simulation uses fixed, synthetic Bernoulli rewards and a seeded random generator.

This stationary baseline has no drift detector, GPU scheduler, cold-start model, or live inference endpoint. It illustrates a model-selection component; it is not FlexiFlow or AdaptFlow’s full implementation.

## Verification

```sh
python -m unittest discover -s tests -v
```

Tests cover numeric metric correctness, leakage, duplicate IDs, empty input, shortest paths, zero-weight cycles, invalid edges, unreachable routes, persisted Unicode notes, query syntax, reward validation, and deterministic simulation.
