"""Deterministic UCB1 routing example with caller-supplied quality/cost rewards."""
import argparse
import json
import math
import random


class UCBRouter:
    def __init__(self, models):
        if not models or len(set(models)) != len(models):
            raise ValueError('Provide distinct model names')
        self.counts = dict.fromkeys(models, 0)
        self.means = dict.fromkeys(models, 0.0)

    def select(self):
        for name, count in self.counts.items():
            if count == 0:
                return name
        total = sum(self.counts.values())
        return max(self.counts, key=lambda name: self.means[name] + math.sqrt(2 * math.log(total) / self.counts[name]))

    def update(self, name, reward):
        if name not in self.counts or not math.isfinite(reward) or not 0 <= reward <= 1:
            raise ValueError('Unknown model or reward outside [0, 1]')
        self.counts[name] += 1
        self.means[name] += (reward - self.means[name]) / self.counts[name]


def simulate(rounds=1000, seed=7):
    if rounds < 1:
        raise ValueError('Rounds must be positive')
    rng = random.Random(seed)
    probabilities = {'small': .55, 'medium': .8, 'large': .65}
    router = UCBRouter(list(probabilities))
    for _ in range(rounds):
        selected = router.select()
        router.update(selected, float(rng.random() < probabilities[selected]))
    return {'synthetic': True, 'seed': seed, 'rounds': rounds, 'selections': router.counts, 'mean_reward': router.means}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rounds', type=int, default=1000)
    parser.add_argument('--seed', type=int, default=7)
    args = parser.parse_args()
    try:
        print(json.dumps(simulate(args.rounds, args.seed), indent=2))
    except ValueError as exc:
        parser.exit(2, f'Error: {exc}\n')
