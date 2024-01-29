import unittest
from calc import calc

class CalcTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calc("+", 1, 0, 2), 3)
        self.assertAlmostEqual(calc("+", 0.1, 0.2), 0.3)
    def test_sub(self):
        self.assertEqual(calc("-", 500, 40, 430), 30)
    def test_div(self):
        self.assertAlmostEqual(calc("/", 80, 40), 2)
    def test_mul(self):
        self.assertEqual(calc("*", 1, 2, 3, 4, 5), 120)
    def test_ind(self):
        self.assertEqual(calc("**", 2, 2), 4)
    def test_mod(self):
        self.assertEqual(calc("%", 1, 2), 1)
    def test_fail(self):
        with self.assertRaises(SyntaxError):
            calc("+", 1, 1)


if __name__ == "__main__":
    unittest.main()