import unittest
from pi.health import PROFILES, evaluate, metric

class HealthTests(unittest.TestCase):
    def test_good(self):
        mood, states = evaluate(50, 500, 23, PROFILES[0])
        self.assertEqual(mood, "happy")
        self.assertEqual(set(states.values()), {"good"})

    def test_one_warning(self):
        mood, _ = evaluate(33, 500, 23, PROFILES[0])
        self.assertEqual(mood, "neutral")

    def test_one_bad(self):
        mood, _ = evaluate(0, 500, 23, PROFILES[0])
        self.assertEqual(mood, "worried")

    def test_two_bad(self):
        mood, _ = evaluate(0, 0, 23, PROFILES[0])
        self.assertEqual(mood, "sad")

    def test_boundaries(self):
        self.assertEqual(metric(35, (35, 65)), "good")
        self.assertEqual(metric(65, (35, 65)), "good")
        with self.assertRaises(ValueError):
            metric(10, (20, 5))

if __name__ == "__main__":
    unittest.main()
