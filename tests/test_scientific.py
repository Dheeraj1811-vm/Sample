"""Unit tests for :mod:`scientific`.

Run from the project root with:

    python3 -m unittest discover tests
"""

from __future__ import annotations

import contextlib
import io
import json
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

    def test_asin_deg(self):
        self.assertAlmostEqual(sci.asin_deg(0), 0.0)
        self.assertAlmostEqual(sci.asin_deg(0.5), 30.0)
        self.assertAlmostEqual(sci.asin_deg(-1), -90.0)

    def test_acos_deg(self):
        self.assertAlmostEqual(sci.acos_deg(1), 0.0)
        self.assertAlmostEqual(sci.acos_deg(0.5), 60.0)
        self.assertAlmostEqual(sci.acos_deg(-1), 180.0)

    def test_inverse_trig_rejects_out_of_domain(self):
        for value in (-1.5, 1.5):
            with self.assertRaises(ValueError):
                sci.asin_deg(value)
            with self.assertRaises(ValueError):
                sci.acos_deg(value)

    def test_atan_deg(self):
        self.assertAlmostEqual(sci.atan_deg(0), 0.0)
        self.assertAlmostEqual(sci.atan_deg(1), 45.0)
        self.assertAlmostEqual(sci.atan_deg(-1), -45.0)

    def test_atan2_deg_keeps_quadrant(self):
        self.assertAlmostEqual(sci.atan2_deg(1, 1), 45.0)
        self.assertAlmostEqual(sci.atan2_deg(1, -1), 135.0)
        self.assertAlmostEqual(sci.atan2_deg(-1, -1), -135.0)
        self.assertAlmostEqual(sci.atan2_deg(0, -1), 180.0)

    def test_inverse_trig_round_trips(self):
        for angle in (-60, -15, 0, 15, 60):
            self.assertAlmostEqual(sci.asin_deg(sci.sin_deg(angle)), angle)
            self.assertAlmostEqual(sci.atan_deg(sci.tan_deg(angle)), angle)


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

    def test_mode(self):
        self.assertAlmostEqual(sci.mode(self.DATA), 4.0)
        self.assertAlmostEqual(sci.mode([7]), 7.0)

    def test_mode_rejects_multimodal_and_empty_input(self):
        with self.assertRaises(ValueError):
            sci.mode([1, 1, 2, 2])
        with self.assertRaises(ValueError):
            sci.mode([])

    def test_percentile(self):
        values = [1, 2, 3, 4]
        self.assertAlmostEqual(sci.percentile(values, 0), 1.0)
        self.assertAlmostEqual(sci.percentile(values, 100), 4.0)
        self.assertAlmostEqual(sci.percentile(values, 50), 2.5)
        self.assertAlmostEqual(sci.percentile(values, 25), 1.75)

    def test_percentile_50_matches_median(self):
        for values in ([3, 1, 2], [4, 1, 3, 2], [5]):
            self.assertAlmostEqual(
                sci.percentile(values, 50), sci.median(values)
            )

    def test_percentile_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            sci.percentile([], 50)
        for p in (-1, 101):
            with self.assertRaises(ValueError):
                sci.percentile([1, 2, 3], p)

    def test_correlation(self):
        xs = [1, 2, 3, 4, 5]
        self.assertAlmostEqual(sci.correlation(xs, [2, 4, 6, 8, 10]), 1.0)
        self.assertAlmostEqual(sci.correlation(xs, [10, 8, 6, 4, 2]), -1.0)
        self.assertAlmostEqual(sci.correlation(xs, xs), 1.0)

    def test_correlation_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            sci.correlation([1, 2, 3], [1, 2])
        with self.assertRaises(ValueError):
            sci.correlation([1], [2])
        with self.assertRaises(ValueError):
            sci.correlation([1, 1, 1], [1, 2, 3])

    def test_linear_regression_recovers_an_exact_line(self):
        slope, intercept = sci.linear_regression([0, 1, 2, 3], [1, 3, 5, 7])
        self.assertAlmostEqual(slope, 2.0)
        self.assertAlmostEqual(intercept, 1.0)

    def test_linear_regression_least_squares_fit(self):
        slope, intercept = sci.linear_regression([0, 1, 2, 3], [1, 3, 5, 8])
        self.assertAlmostEqual(slope, 2.3)
        self.assertAlmostEqual(intercept, 0.8)

    def test_linear_regression_handles_constant_ys(self):
        # correlation is undefined here, but the fitted line is not.
        slope, intercept = sci.linear_regression([1, 2, 3], [5, 5, 5])
        self.assertAlmostEqual(slope, 0.0)
        self.assertAlmostEqual(intercept, 5.0)

    def test_linear_regression_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            sci.linear_regression([1, 2, 3], [1, 2])
        with self.assertRaises(ValueError):
            sci.linear_regression([1], [2])
        with self.assertRaises(ValueError):
            sci.linear_regression([2, 2, 2], [1, 2, 3])


class TestVectors(unittest.TestCase):
    def test_dot(self):
        self.assertAlmostEqual(sci.dot([1, 2, 3], [4, 5, 6]), 32.0)
        self.assertAlmostEqual(sci.dot([1, 0], [0, 1]), 0.0)
        self.assertAlmostEqual(sci.dot([-2, 3], [4, 1]), -5.0)

    def test_dot_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            sci.dot([1, 2, 3], [1, 2])
        with self.assertRaises(ValueError):
            sci.dot([], [])

    def test_magnitude(self):
        self.assertAlmostEqual(sci.magnitude([3, 4]), 5.0)
        self.assertAlmostEqual(sci.magnitude([1, 2, 2]), 3.0)
        self.assertAlmostEqual(sci.magnitude([0, 0]), 0.0)

    def test_magnitude_matches_hypotenuse_in_two_dimensions(self):
        self.assertAlmostEqual(sci.magnitude([5, 12]), sci.hypotenuse(5, 12))

    def test_magnitude_rejects_empty_vector(self):
        with self.assertRaises(ValueError):
            sci.magnitude([])

    def test_normalize(self):
        self.assertEqual(sci.normalize([3, 4]), [0.6, 0.8])
        self.assertAlmostEqual(sci.magnitude(sci.normalize([1, 2, 3])), 1.0)

    def test_normalize_rejects_zero_vector(self):
        with self.assertRaises(ValueError):
            sci.normalize([0, 0, 0])

    def test_angle_between_deg(self):
        self.assertAlmostEqual(sci.angle_between_deg([1, 0], [0, 1]), 90.0)
        self.assertAlmostEqual(sci.angle_between_deg([1, 0], [1, 1]), 45.0)
        self.assertAlmostEqual(sci.angle_between_deg([1, 0], [-1, 0]), 180.0)

    def test_angle_between_deg_is_zero_for_parallel_vectors(self):
        # Exercises the cosine clamp: rounding can nudge this past 1.0.
        self.assertAlmostEqual(sci.angle_between_deg([1, 1, 1], [2, 2, 2]), 0.0)
        self.assertAlmostEqual(sci.angle_between_deg([0.1, 0.7], [0.3, 2.1]), 0.0)

    def test_angle_between_deg_rejects_zero_vector(self):
        with self.assertRaises(ValueError):
            sci.angle_between_deg([0, 0], [1, 1])


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

    def test_newton_root(self):
        self.assertAlmostEqual(
            sci.newton_root(lambda x: x * x - 2, 1), math.sqrt(2), places=9
        )
        self.assertAlmostEqual(
            sci.newton_root(lambda x: math.cos(x) - x, 0.5), 0.739085133, places=8
        )

    def test_newton_root_uses_supplied_derivative(self):
        self.assertAlmostEqual(
            sci.newton_root(lambda x: x * x - 9, 1, fprime=lambda x: 2 * x),
            3.0,
            places=12,
        )

    def test_newton_root_agrees_with_bisection(self):
        f = lambda x: x ** 3 - x - 2  # noqa: E731
        self.assertAlmostEqual(
            sci.newton_root(f, 2), sci.find_root(f, 1, 2), places=8
        )

    def test_newton_root_returns_starting_point_at_a_root(self):
        self.assertEqual(sci.newton_root(lambda x: x * x, 0), 0)

    def test_newton_root_rejects_vanishing_derivative(self):
        with self.assertRaises(ValueError):
            sci.newton_root(lambda x: x * x + 1, 0)

    def test_newton_root_reports_non_convergence(self):
        # Newton's method cycles between 0 and 1 for this cubic.
        with self.assertRaises(ValueError):
            sci.newton_root(
                lambda x: x ** 3 - 2 * x + 2,
                0,
                fprime=lambda x: 3 * x * x - 2,
                max_iterations=10,
            )

    def test_newton_root_rejects_non_positive_tolerance(self):
        with self.assertRaises(ValueError):
            sci.newton_root(lambda x: x - 1, 0, tolerance=0)


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

    def test_kelvin_to_celsius(self):
        self.assertAlmostEqual(sci.kelvin_to_celsius(273.15), 0.0)
        self.assertAlmostEqual(sci.kelvin_to_celsius(0), -273.15)
        self.assertAlmostEqual(sci.kelvin_to_celsius(300), 26.85)

    def test_kelvin_round_trip(self):
        for celsius in (-100, 0, 37, 1000):
            self.assertAlmostEqual(
                sci.kelvin_to_celsius(sci.celsius_to_kelvin(celsius)), celsius
            )

    def test_kelvin_to_celsius_rejects_negative_kelvin(self):
        with self.assertRaises(ValueError):
            sci.kelvin_to_celsius(-1)

    def test_fahrenheit_kelvin_conversions(self):
        self.assertAlmostEqual(sci.fahrenheit_to_kelvin(32), 273.15)
        self.assertAlmostEqual(sci.kelvin_to_fahrenheit(273.15), 32.0)
        self.assertAlmostEqual(sci.fahrenheit_to_kelvin(-459.67), 0.0)

    def test_fahrenheit_kelvin_round_trip(self):
        for fahrenheit in (-40, 32, 98.6, 212):
            self.assertAlmostEqual(
                sci.kelvin_to_fahrenheit(sci.fahrenheit_to_kelvin(fahrenheit)),
                fahrenheit,
            )

    def test_fahrenheit_to_kelvin_rejects_below_absolute_zero(self):
        with self.assertRaises(ValueError):
            sci.fahrenheit_to_kelvin(-500)


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

class TestPhysics(unittest.TestCase):
    def test_gravitational_force_unit_case(self):
        self.assertAlmostEqual(
            sci.gravitational_force(1, 1, 1), sci.GRAVITATIONAL
        )

    def test_gravitational_force_obeys_inverse_square_law(self):
        near = sci.gravitational_force(1e6, 1e6, 1)
        far = sci.gravitational_force(1e6, 1e6, 2)
        self.assertAlmostEqual(near / far, 4.0)

    def test_gravitational_force_reproduces_surface_gravity(self):
        # 1 kg at the Earth's mean radius should weigh about 9.8 N.
        self.assertAlmostEqual(
            sci.gravitational_force(5.972e24, 1, 6.371e6), 9.82, delta=0.05
        )

    def test_gravitational_force_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            sci.gravitational_force(-1, 1, 1)
        for distance in (0, -1):
            with self.assertRaises(ValueError):
                sci.gravitational_force(1, 1, distance)

    def test_photon_energy(self):
        self.assertAlmostEqual(
            sci.photon_energy(500e-9) / 1e-19, 3.9729, places=3
        )
        self.assertAlmostEqual(
            sci.photon_energy(1e-6), sci.PLANCK * sci.SPEED_OF_LIGHT / 1e-6
        )

    def test_photon_energy_is_inversely_proportional_to_wavelength(self):
        self.assertAlmostEqual(
            sci.photon_energy(250e-9) / sci.photon_energy(500e-9), 2.0
        )

    def test_photon_energy_rejects_non_positive_wavelength(self):
        for wavelength in (0, -1e-9):
            with self.assertRaises(ValueError):
                sci.photon_energy(wavelength)

    def test_ideal_gas_pressure_at_stp(self):
        # One mole in a molar volume at 0 C is one standard atmosphere.
        self.assertAlmostEqual(
            sci.ideal_gas_pressure(1, 273.15, 0.022414), 101325, delta=5
        )

    def test_ideal_gas_pressure_satisfies_pv_equals_nrt(self):
        moles, temperature, volume = 2.5, 310.0, 0.05
        pressure = sci.ideal_gas_pressure(moles, temperature, volume)
        self.assertAlmostEqual(
            pressure * volume, moles * sci.GAS_CONSTANT * temperature
        )

    def test_ideal_gas_pressure_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            sci.ideal_gas_pressure(-1, 300, 1)
        with self.assertRaises(ValueError):
            sci.ideal_gas_pressure(1, -1, 1)
        for volume in (0, -1):
            with self.assertRaises(ValueError):
                sci.ideal_gas_pressure(1, 300, volume)

class TestCLI(unittest.TestCase):
    def run_cli(self, *argv):
        """Run the CLI in-process, returning ``(exit code, stdout, stderr)``."""
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = sci.main(list(argv))
        return code, out.getvalue().strip(), err.getvalue().strip()

    def assert_usage_error(self, *argv):
        """Assert that argparse rejects ``argv`` with the conventional code 2."""
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(
            io.StringIO()
        ):
            with self.assertRaises(SystemExit) as caught:
                sci.main(list(argv))
        self.assertEqual(caught.exception.code, 2)

    def test_scalar_commands(self):
        self.assertEqual(self.run_cli("power", "2", "10"), (0, "1024", ""))
        self.assertEqual(self.run_cli("sin-deg", "30"), (0, "0.5", ""))
        self.assertEqual(self.run_cli("celsius-to-fahrenheit", "100"), (0, "212", ""))

    def test_series_command_takes_space_separated_numbers(self):
        self.assertEqual(self.run_cli("mean", "2.5", "3.1", "4.8"), (0, "3.466667", ""))

    def test_vector_commands_take_comma_separated_groups(self):
        self.assertEqual(self.run_cli("dot", "1,2,3", "4,5,6"), (0, "32", ""))
        self.assertEqual(self.run_cli("angle-between-deg", "1,0", "1,1"), (0, "45", ""))

    def test_optional_arguments(self):
        self.assertEqual(self.run_cli("log", "1024", "--base", "2"), (0, "10", ""))
        self.assertEqual(
            self.run_cli("std-dev", "2", "4", "4", "4", "5", "5", "7", "9",
                         "--population"),
            (0, "2", ""),
        )

    def test_percentile_takes_the_percentile_first(self):
        self.assertEqual(
            self.run_cli("percentile", "90", "1", "2", "3", "4", "5"), (0, "4.6", "")
        )

    def test_sequence_results_print_one_per_line(self):
        self.assertEqual(self.run_cli("normalize", "3", "4"), (0, "0.6\n0.8", ""))
        self.assertEqual(
            self.run_cli("solve-quadratic", "1", "2", "5"), (0, "-1+2j\n-1-2j", "")
        )

    def test_integer_results_are_printed_exactly(self):
        code, out, _ = self.run_cli("factorial", "25")
        self.assertEqual(code, 0)
        self.assertEqual(out, str(math.factorial(25)))

    def test_json_output(self):
        code, out, _ = self.run_cli("photon-energy", "500e-9", "--json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload["function"], "photon_energy")
        self.assertAlmostEqual(payload["result"], sci.photon_energy(500e-9))

    def test_json_output_for_sequences_and_complex_numbers(self):
        _, out, _ = self.run_cli("linear-regression", "0,1,2,3", "1,3,5,7", "--json")
        self.assertEqual(json.loads(out)["result"], [2.0, 1.0])

        _, out, _ = self.run_cli("solve-quadratic", "1", "2", "5", "--json")
        first = json.loads(out)["result"][0]
        self.assertAlmostEqual(first["real"], -1.0)
        self.assertAlmostEqual(first["imag"], 2.0)

    def test_domain_errors_exit_with_code_one(self):
        for argv in (("log", "0"), ("tan-deg", "90"), ("nth-root", "-16", "2")):
            code, out, err = self.run_cli(*argv)
            self.assertEqual(code, 1, argv)
            self.assertEqual(out, "")
            self.assertTrue(err.startswith("error: "), err)

    def test_usage_errors_exit_with_code_two(self):
        self.assert_usage_error("no-such-command")
        self.assert_usage_error("mean", "not-a-number")
        self.assert_usage_error("dot", "1,x,3", "4,5,6")
        self.assert_usage_error("power", "2")

    def test_constants_command(self):
        code, out, _ = self.run_cli("constants")
        self.assertEqual(code, 0)
        # Names are padded to a fixed column, so match the value alone.
        self.assertRegex(out, r"SPEED_OF_LIGHT\s+= 299792458\.0")

        _, out, _ = self.run_cli("constants", "--json")
        self.assertEqual(json.loads(out)["PLANCK"], sci.PLANCK)

    def test_demo_runs_with_and_without_a_subcommand(self):
        for argv in ((), ("demo",)):
            code, out, _ = self.run_cli(*argv)
            self.assertEqual(code, 0)
            self.assertIn("Elementary", out)

    def test_every_public_function_is_reachable_from_the_cli(self):
        # Subcommands, plus the two commands named differently from their
        # function (eval -> evaluate, repl). The functions that take a
        # function to work on are reachable through eval rather than having
        # a subcommand of their own.
        exposed = {name.replace("-", "_") for name in sci._COMMANDS}
        exposed |= {"evaluate", "repl"}
        eval_only = set(sci._DEFERRED_FIRST_ARGUMENT)
        public = {name for name in sci.__all__ if not name.isupper()}
        self.assertEqual(public - exposed - eval_only, {"main"})

    def test_eval_subcommand(self):
        self.assertEqual(
            self.run_cli("eval", "2 * sin_deg(30) + log(100, 10)"), (0, "3", "")
        )
        # The words of an unquoted expression are joined back together.
        self.assertEqual(self.run_cli("eval", "1", "+", "1"), (0, "2", ""))

    def test_eval_subcommand_json_reports_the_expression(self):
        code, out, _ = self.run_cli("eval", "mean([1, 2, 3, 4])", "--json")
        self.assertEqual(code, 0)
        self.assertEqual(
            json.loads(out), {"expression": "mean([1, 2, 3, 4])", "result": 2.5}
        )

    def test_eval_subcommand_reports_errors(self):
        code, out, err = self.run_cli("eval", "1 / 0")
        self.assertEqual((code, out), (1, ""))
        self.assertTrue(err.startswith("error: "), err)

    def test_eval_only_functions_are_in_the_expression_namespace(self):
        for name in sci._DEFERRED_FIRST_ARGUMENT:
            self.assertIn(name, sci._NAMESPACE)

class TestExpressions(unittest.TestCase):
    def test_arithmetic_and_precedence(self):
        self.assertAlmostEqual(sci.evaluate("1 + 2 * 3"), 7.0)
        self.assertAlmostEqual(sci.evaluate("(1 + 2) * 3"), 9.0)
        self.assertAlmostEqual(sci.evaluate("7 % 4"), 3.0)
        self.assertAlmostEqual(sci.evaluate("10 / 4"), 2.5)

    def test_power_is_right_associative_and_binds_tighter_than_unary_minus(self):
        self.assertAlmostEqual(sci.evaluate("2^3^2"), 512.0)
        self.assertAlmostEqual(sci.evaluate("-2^2"), -4.0)
        self.assertAlmostEqual(sci.evaluate("2^-1"), 0.5)
        self.assertAlmostEqual(sci.evaluate("--3"), 3.0)

    def test_double_star_is_accepted_for_power(self):
        self.assertAlmostEqual(sci.evaluate("2 ** 10"), sci.evaluate("2 ^ 10"))

    def test_function_calls(self):
        self.assertAlmostEqual(sci.evaluate("2 * sin_deg(30) + log(100, 10)"), 3.0)
        self.assertAlmostEqual(sci.evaluate("log(power(2, 10), 2)"), 10.0)
        self.assertAlmostEqual(sci.evaluate("sqrt(16)"), 4.0)

    def test_list_literals_feed_the_sequence_functions(self):
        self.assertAlmostEqual(sci.evaluate("mean([1, 2, 3, 4])"), 2.5)
        self.assertAlmostEqual(sci.evaluate("dot([1, 2, 3], [4, 5, 6])"), 32.0)
        self.assertEqual(sci.evaluate("normalize([3, 4])"), [0.6, 0.8])

    def test_constants_are_in_scope(self):
        self.assertAlmostEqual(sci.evaluate("pi"), math.pi)
        self.assertAlmostEqual(sci.evaluate("SPEED_OF_LIGHT"), sci.SPEED_OF_LIGHT)

    def test_deferred_first_argument_binds_x(self):
        self.assertAlmostEqual(sci.evaluate("derivative(x^2, 3)"), 6.0, places=5)
        self.assertAlmostEqual(sci.evaluate("integrate(x^2, 0, 1)"), 1 / 3, places=9)
        self.assertAlmostEqual(
            sci.evaluate("find_root(x^2 - 2, 0, 2)"), math.sqrt(2), places=9
        )
        self.assertAlmostEqual(
            sci.evaluate("newton_root(x^2 - 2, 1)"), math.sqrt(2), places=9
        )

    def test_deferred_argument_sees_the_surrounding_variables(self):
        variables = {"k": 3.0}
        self.assertAlmostEqual(
            sci.evaluate("derivative(k * x, 1)", variables), 3.0, places=6
        )

    def test_variables_persist_across_calls(self):
        variables = {}
        self.assertAlmostEqual(sci.evaluate("radius = 2.5", variables), 2.5)
        self.assertAlmostEqual(sci.evaluate("pi * radius^2", variables), math.pi * 6.25)
        self.assertEqual(variables["radius"], 2.5)

    def test_assignment_cannot_shadow_the_calculator(self):
        for expression in ("pi = 3", "mean = 1"):
            with self.assertRaises(ValueError):
                sci.evaluate(expression)

    def test_syntax_errors(self):
        for expression in ("2 +", "(1 + 2", "1 2", "", "[1, 2", "2 & 3"):
            with self.assertRaises(ValueError):
                sci.evaluate(expression)

    def test_name_errors(self):
        for expression in ("foo(2)", "bar", "pi(2)", "sin_deg"):
            with self.assertRaises(ValueError):
                sci.evaluate(expression)

    def test_division_by_zero_is_a_value_error(self):
        for expression in ("1 / 0", "1 % 0"):
            with self.assertRaises(ValueError):
                sci.evaluate(expression)

    def test_bad_call_reports_the_function(self):
        with self.assertRaisesRegex(ValueError, "bad call to mean"):
            sci.evaluate("mean(1, 2, 3)")

    def test_python_is_not_reachable(self):
        for expression in (
            "__import__('os')",
            "open('/etc/passwd')",
            "[].__class__",
            "eval('1')",
        ):
            with self.assertRaises(ValueError):
                sci.evaluate(expression)


class TestRepl(unittest.TestCase):
    def run_repl(self, *lines):
        """Drive the REPL with ``lines``, returning ``(code, stdout, stderr)``."""
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = sci.repl(list(lines))
        return code, out.getvalue().strip(), err.getvalue().strip()

    def test_evaluates_each_line(self):
        code, out, err = self.run_repl("1 + 1", "sin_deg(30)")
        self.assertEqual((code, err), (0, ""))
        self.assertEqual(out, "2\n0.5")

    def test_underscore_holds_the_previous_result(self):
        _, out, _err = self.run_repl("2 + 3", "_ * 2")
        self.assertEqual(out, "5\n10")

    def test_assignments_and_vars(self):
        _, out, _err = self.run_repl("radius = 2", "radius^2", "vars")
        # vars lists what the user defined, not the implicit "_".
        self.assertEqual(out, "2\n4\nradius = 2")

    def test_errors_do_not_stop_the_loop(self):
        code, out, err = self.run_repl("1 / 0", "1 + 1")
        self.assertEqual(code, 0)
        self.assertEqual(out, "2")
        self.assertTrue(err.startswith("error: "), err)

    def test_quit_stops_reading(self):
        _, out, _err = self.run_repl("1 + 1", "quit", "2 + 2")
        self.assertEqual(out, "2")

    def test_blank_lines_and_comments_are_skipped(self):
        _, out, _err = self.run_repl("", "   ", "# a note", "3")
        self.assertEqual(out, "3")

    def test_help_is_available(self):
        _, out, _err = self.run_repl("help")
        self.assertIn("quit", out)


if __name__ == "__main__":
    unittest.main()
