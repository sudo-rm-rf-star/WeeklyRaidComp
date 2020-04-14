import unittest
from logic.Roster import _calculate_importance


class TestRoster(unittest.TestCase):
    def test_calculate_importance(self):
        self.assertEqual(_calculate_importance(0, 1, 4), 1)
        self.assertEqual(_calculate_importance(1, 1, 4), 0.75)
        self.assertEqual(_calculate_importance(2, 1, 4), 0.5)
        self.assertEqual(_calculate_importance(3, 1, 4), 0.25)
        self.assertEqual(_calculate_importance(4, 1, 4), 0)

        self.assertEqual(_calculate_importance(0, 0, 1), 0.5)
        self.assertEqual(_calculate_importance(1, 0, 1), 0)

        self.assertEqual(_calculate_importance(0, 0, 0), 0)


if __name__ == "__main__":
    unittest.main()
