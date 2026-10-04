import unittest

from congruencias import (
    are_congruent,
    euclidean_division,
    generate_question,
    modular_inverse,
    residue_table,
    solve_linear_congruence,
)


class CongruenceTests(unittest.TestCase):
    def test_euclidean_division_supports_negative_dividend(self):
        self.assertEqual(euclidean_division(-17, 5), (-4, 3))

    def test_congruence(self):
        self.assertTrue(are_congruent(38, 3, 7))
        self.assertFalse(are_congruent(38, 4, 7))

    def test_inverse(self):
        self.assertEqual(modular_inverse(3, 7), 5)
        self.assertIsNone(modular_inverse(6, 9))

    def test_linear_congruence_with_multiple_solutions(self):
        self.assertEqual(solve_linear_congruence(4, 2, 6), [2, 5])

    def test_multiplication_table(self):
        table = residue_table(4, "×")
        self.assertEqual(table[3][3], 1)

    def test_question_is_reproducible_and_valid(self):
        first = generate_question("Difícil", seed=42)
        second = generate_question("Difícil", seed=42)
        self.assertEqual(first, second)
        self.assertIn(first.answer, first.choices)


if __name__ == "__main__":
    unittest.main()
