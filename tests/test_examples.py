import csv
import math
from pathlib import Path
import tempfile
import unittest

from examples.evaluate import evaluate
from examples.memory import Memory
from examples.navigation import shortest_path
from examples.routing import UCBRouter, simulate


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        with (Path(__file__).resolve().parents[1] / 'examples/data/predictions.csv').open() as stream:
            self.rows = list(csv.DictReader(stream))

    def test_metrics(self):
        result = evaluate(self.rows)
        self.assertEqual(result['overall']['accuracy'], .75)
        self.assertAlmostEqual(result['overall']['macro_f1'], (0.8 + 2/3) / 2)
        self.assertEqual(result['by_language']['te']['macro_f1'], 1)

    def test_leakage_duplicate_and_empty(self):
        with self.assertRaisesRegex(ValueError, 'Groups span'):
            evaluate(self.rows + [dict(self.rows[1], id='new', split='train')])
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            evaluate(self.rows + [self.rows[0]])
        with self.assertRaisesRegex(ValueError, 'No test'):
            evaluate([])


class RouteTests(unittest.TestCase):
    def test_shortest_path_and_zero_cycle(self):
        graph = {'a': {'b': 0, 'c': 9}, 'b': {'a': 0, 'c': 2}, 'c': {}}
        self.assertEqual(shortest_path(graph, 'a', 'c'), {'distance': 2, 'path': ['a','b','c']})
        self.assertEqual(shortest_path(graph, 'a', 'a')['path'], ['a'])

    def test_invalid_edges_and_unreachable(self):
        for weight in (-1, math.nan, math.inf):
            with self.assertRaises(ValueError):
                shortest_path({'a': {'b': weight}, 'b': {}}, 'a', 'b')
        with self.assertRaisesRegex(ValueError, 'No route'):
            shortest_path({'a': {}, 'b': {}}, 'a', 'b')


class MemoryTests(unittest.TestCase):
    def test_persistence_unicode_and_query_syntax(self):
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory) / 'memory.db')
            memory = Memory(path)
            memory.add('తెలుగు language evaluation')
            memory.add('Kubernetes deployment')
            memory.close()
            memory = Memory(path)
            try:
                self.assertEqual(memory.search('తెలుగు')[0]['id'], 1)
                self.assertEqual(memory.search('"deployment" OR --')[0]['id'], 2)
                self.assertEqual(memory.search('!!!'), [])
                with self.assertRaises(ValueError): memory.add(' ')
                with self.assertRaises(ValueError): memory.search('test', -1)
            finally:
                memory.close()


class RoutingTests(unittest.TestCase):
    def test_exploration_and_validation(self):
        router = UCBRouter(['a','b'])
        self.assertEqual(router.select(), 'a')
        router.update('a', .5)
        self.assertEqual(router.select(), 'b')
        for reward in (-1, 2, math.nan):
            with self.assertRaises(ValueError): router.update('a', reward)
        with self.assertRaises(ValueError): UCBRouter([])

    def test_reproducible_simulation(self):
        result = simulate()
        self.assertEqual(result, simulate())
        self.assertEqual(sum(result['selections'].values()), 1000)
        self.assertGreater(result['selections']['medium'], result['selections']['small'])


if __name__ == '__main__':
    unittest.main()
