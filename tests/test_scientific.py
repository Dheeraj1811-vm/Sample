"""Unit tests for :mod:`scientific`.

Run from the project root with:

    python3 -m unittest discover tests
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import scientific as sci  # noqa: E402  (import follows sys.path setup)


class TestElementary(unittest.TestCase):
    def test_power(self):
        self.assertEqual(sci.power(2, 10), 1024.0)
        self.assertAlmostEqual(sci.power(9, 0.5), 3.0)
        self.assertAlmostEqual(sci.power(2, -2), 0.25)

    def test_nth_root(self):
        self.assertAlmostEqual(sci.nth_root(27, 3), 3.0)
        self.assertAlmostEqual(sci.nth_root(16, 4), 2.0)

    def test_nth_root_of_negative_is_real_for_odd_degrees(self):
        self.assertAlmostEqual(sci.nth_root(-8, 3), -2.0)
        self.assertAlmostEqual(sci.nth_root(-32, 5), -2.0)

    def test_nth_root_rejects_even_root_of_negative(self):
        with self.assertRaises(ValueError):
            sci.nth_root(-16, 2)

    def test_nth_root_rejects_zero_degree(self):
        with self.assertRaises(ValueError):
            sci.nth_root(8, 0)

    def test_log(self):
        self.assertAlmostEqual(sci.log(1024, 2), 10.0)
        self.assertAlmostEqual(sci.log(math.e), 1.0)
        self.assertAlmostEqual(sci.log(1000, 10), 3.0)

    def test_log_rejects_bad_domain(self):
        for value in (0, -1):
            with self.assertRaises(ValueError):
                sci.log(value)
        for base in (0, 1, -2):
            with self.assertRaises(ValueError):
                sci.log(10, base)

    def test_factorial(self):
        self.assertEqual(sci.factorial(0), 1)
        self.assertEqual(sci.factorial(10), 3_628_800)
        with self.assertRaises(ValueError):
            sci.factorial(-1)

    def test_combinations_and_permutations(self):
        self.assertEqual(sci.combinations(52, 5), 2_598_960)
        self.assertEqual(sci.combinations(5, 0), 1)
        self.assertEqual(sci.permutations(5, 2), 20)
        with self.assertRaises(ValueError):
            sci.combinations(-1, 2)
        with self.assertRaises(ValueError):
            sci.permutations(5, -2)

    def test_hypotenuse(self):
        self.assertAlmostEqual(sci.hypotenuse(3, 4), 5.0)


class TestTrigonometry(unittest.TestCase):
    def test_sin_deg(self):
        self.assertAlmostEqual(sci.sin_deg(0), 0.0)
        self.assertAlmostEqual(sci.sin_deg(30), 0.5)
        self.assertAlmostEqual(sci.sin_deg(90), 1.0)

    def test_cos_deg(self):
        self.assertAlmostEqual(sci.cos_deg(0), 1.0)
        self.assertAlmostEqual(sci.cos_deg(60), 0.5)
        self.assertAlmostEqual(sci.cos_deg(180), -1.0)

    def test_tan_deg(self):
        self.assertAlmostEqual(sci.tan_deg(45), 1.0)
        self.assertAlmostEqual(sci.tan_deg(0), 0.0)

    def test_tan_deg_rejects_undefined_angles(self):
        for angle in (90, 270, -90):
            with self.assertRaises(ValueError):
                sci.tan_deg(angle)


class TestStatistics(unittest.TestCase):
    # Population variance 4.0, sample variance 32/7.
    DATA = [2, 4, 4, 4, 5, 5, 7, 9]

    def test_mean(self):
        self.assertAlmostEqual(sci.mean(self.DATA), 5.0)
        self.assertAlmostEqual(sci.mean([1.5]), 1.5)

    def test_median_odd_and_even_lengths(self):
        self.assertAlmostEqual(sci.median([3, 1, 2]), 2.0)
        self.assertAlmostEqual(sci.median([4, 1, 3, 2]), 2.5)

    def test_median_does_not_mutate_input(self):
        values = [3, 1, 2]
        sci.median(values)
        self.assertEqual(values, [3, 1, 2])

    def test_variance(self):
        self.assertAlmostEqual(sci.variance(self.DATA, sample=False), 4.0)
        self.assertAlmostEqual(sci.variance(self.DATA, sample=True), 32 / 7)

    def test_std_dev(self):
        self.assertAlmostEqual(sci.std_dev(self.DATA, sample=False), 2.0)
        self.assertAlmostEqual(
            sci.std_dev(self.DATA, sample=True), math.sqrt(32 / 7)
        )

    def test_empty_input_is_rejected(self):
        for fn in (sci.mean, sci.median, sci.variance, sci.std_dev):
            with self.assertRaises(ValueError):
                fn([])

    def test_sample_variance_needs_two_points(self):
        with self.assertRaises(ValueError):
            sci.variance([1.0], sample=True)
        self.assertAlmostEqual(sci.variance([1.0], sample=False), 0.0)


class TestNumericalMethods(unittest.TestCase):
    def test_derivative(self):
        self.assertAlmostEqual(sci.derivative(lambda x: x ** 2, 3), 6.0, places=5)
        self.assertAlmostEqual(sci.derivative(math.sin, 0), 1.0, places=5)
        self.assertAlmostEqual(sci.derivative(math.exp, 1), math.e, places=5)

    def test_derivative_rejects_non_positive_step(self):
        with self.assertRaises(ValueError):
            sci.derivative(lambda x: x, 1, h=0)

    def test_integrate(self):
        self.assertAlmostEqual(sci.integrate(math.sin, 0, math.pi), 2.0, places=8)
        self.assertAlmostEqual(
            sci.integrate(lambda x: x ** 2, 0, 1), 1 / 3, places=10
        )

    def test_integrate_is_exact_for_cubics(self):
        # Simpson's rule integrates polynomials up to degree 3 exactly.
        self.assertAlmostEqual(
            sci.integrate(lambda x: x ** 3, 0, 2, intervals=2), 4.0, places=10
        )

    def test_integrate_rounds_odd_intervals_up(self):
        self.assertAlmostEqual(
            sci.integrate(lambda x: x ** 2, 0, 1, intervals=3), 1 / 3, places=10
        )

    def test_integrate_rejects_too_few_intervals(self):
        with self.assertRaises(ValueError):
            sci.integrate(math.sin, 0, 1, intervals=1)

    def test_find_root(self):
        self.assertAlmostEqual(
            sci.find_root(lambda x: x * x - 2, 0, 2), math.sqrt(2), places=9
        )
        self.assertAlmostEqual(
            sci.find_root(lambda x: math.cos(x) - x, 0, 1), 0.739085133, places=8
        )

    def test_find_root_returns_exact_endpoint(self):
        self.assertEqual(sci.find_root(lambda x: x - 2, 2, 5), 2)
        self.assertEqual(sci.find_root(lambda x: x - 5, 2, 5), 5)

    def test_find_root_requires_sign_change(self):
        with self.assertRaises(ValueError):
            sci.find_root(lambda x: x * x + 1, -1, 1)

    def test_solve_quadratic_real_roots(self):
        r1, r2 = sci.solve_quadratic(1, -3, 2)
        self.assertAlmostEqual(r1.real, 2.0)
        self.assertAlmostEqual(r2.real, 1.0)
        self.assertAlmostEqual(r1.imag, 0.0)
        self.assertAlmostEqual(r2.imag, 0.0)

    def test_solve_quadratic_repeated_root(self):
        r1, r2 = sci.solve_quadratic(1, -2, 1)
        self.assertAlmostEqual(r1.real, 1.0)
        self.assertAlmostEqual(r2.real, 1.0)

    def test_solve_quadratic_complex_roots(self):
        r1, r2 = sci.solve_quadratic(1, 2, 5)
        self.assertAlmostEqual(r1.real, -1.0)
        self.assertAlmostEqual(r1.imag, 2.0)
        self.assertAlmostEqual(r2.real, -1.0)
        self.assertAlmostEqual(r2.imag, -2.0)

    def test_solve_quadratic_rejects_zero_leading_coefficient(self):
        with self.assertRaises(ValueError):
            sci.solve_quadratic(0, 2, 1)


class TestConversions(unittest.TestCase):
    def test_celsius_to_fahrenheit(self):
        self.assertAlmostEqual(sci.celsius_to_fahrenheit(0), 32.0)
        self.assertAlmostEqual(sci.celsius_to_fahrenheit(100), 212.0)
        self.assertAlmostEqual(sci.celsius_to_fahrenheit(-40), -40.0)

    def test_fahrenheit_to_celsius(self):
        self.assertAlmostEqual(sci.fahrenheit_to_celsius(32), 0.0)
        self.assertAlmostEqual(sci.fahrenheit_to_celsius(212), 100.0)

    def test_conversions_round_trip(self):
        for celsius in (-40, 0, 37, 100):
            self.assertAlmostEqual(
                sci.fahrenheit_to_celsius(sci.celsius_to_fahrenheit(celsius)),
                celsius,
            )

    def test_celsius_to_kelvin(self):
        self.assertAlmostEqual(sci.celsius_to_kelvin(0), 273.15)
        self.assertAlmostEqual(sci.celsius_to_kelvin(-273.15), 0.0)

    def test_celsius_to_kelvin_rejects_below_absolute_zero(self):
        with self.assertRaises(ValueError):
            sci.celsius_to_kelvin(-300)


class TestConstants(unittest.TestCase):
    def test_exact_si_definitions(self):
        # These constants are exact by SI definition, not measured.
        self.assertEqual(sci.SPEED_OF_LIGHT, 299_792_458.0)
        self.assertEqual(sci.PLANCK, 6.626_070_15e-34)
        self.assertEqual(sci.AVOGADRO, 6.022_140_76e23)
        self.assertEqual(sci.BOLTZMANN, 1.380_649e-23)
        self.assertEqual(sci.ELEMENTARY_CHARGE, 1.602_176_634e-19)

    def test_gas_constant_matches_derivation(self):
        self.assertAlmostEqual(
            sci.GAS_CONSTANT, sci.BOLTZMANN * sci.AVOGADRO, places=6
        )


if __name__ == "__main__":
    unittest.main()
