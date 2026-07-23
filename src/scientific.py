"""Scientific calculation utilities.

A dependency-free collection of common scientific helpers: elementary
functions, trigonometry, statistics, numerical methods, and physical
constants.

Run directly for a short demonstration:

    python src/scientific.py
"""

from __future__ import annotations

import math
from typing import Callable, Sequence

__all__ = [
    "SPEED_OF_LIGHT",
    "PLANCK",
    "GRAVITATIONAL",
    "AVOGADRO",
    "BOLTZMANN",
    "ELEMENTARY_CHARGE",
    "GAS_CONSTANT",
    "power",
    "nth_root",
    "log",
    "factorial",
    "combinations",
    "permutations",
    "hypotenuse",
    "sin_deg",
    "cos_deg",
    "tan_deg",
    "mean",
    "median",
    "variance",
    "std_dev",
    "derivative",
    "integrate",
    "find_root",
    "solve_quadratic",
    "celsius_to_fahrenheit",
    "fahrenheit_to_celsius",
    "celsius_to_kelvin",
]

# --------------------------------------------------------------------------
# Physical constants (SI units, CODATA 2018)
# --------------------------------------------------------------------------

SPEED_OF_LIGHT = 299_792_458.0          # m / s
PLANCK = 6.626_070_15e-34               # J * s
GRAVITATIONAL = 6.674_30e-11            # m^3 / (kg * s^2)
AVOGADRO = 6.022_140_76e23              # 1 / mol
BOLTZMANN = 1.380_649e-23               # J / K
ELEMENTARY_CHARGE = 1.602_176_634e-19   # C
GAS_CONSTANT = 8.314_462_618            # J / (mol * K)


# --------------------------------------------------------------------------
# Elementary functions
# --------------------------------------------------------------------------

def power(base: float, exponent: float) -> float:
    """Return ``base`` raised to ``exponent``."""
    return math.pow(base, exponent)


def nth_root(value: float, n: int) -> float:
    """Return the real ``n``-th root of ``value``.

    Negative values are supported for odd roots (e.g. the cube root of -8
    is -2), matching the real-valued convention.
    """
    if n == 0:
        raise ValueError("root degree must be non-zero")
    if value < 0:
        if n % 2 == 0:
            raise ValueError("even root of a negative number is not real")
        return -math.pow(-value, 1.0 / n)
    return math.pow(value, 1.0 / n)


def log(value: float, base: float = math.e) -> float:
    """Return the logarithm of ``value`` in the given ``base``."""
    if value <= 0:
        raise ValueError("logarithm is undefined for non-positive values")
    if base <= 0 or base == 1:
        raise ValueError("logarithm base must be positive and not equal to 1")
    return math.log(value, base)


def factorial(n: int) -> int:
    """Return ``n!`` for a non-negative integer ``n``."""
    if n < 0:
        raise ValueError("factorial is undefined for negative numbers")
    return math.factorial(n)


def combinations(n: int, k: int) -> int:
    """Return the number of ways to choose ``k`` items from ``n`` (nCk)."""
    if n < 0 or k < 0:
        raise ValueError("n and k must be non-negative")
    return math.comb(n, k)


def permutations(n: int, k: int) -> int:
    """Return the number of ordered arrangements of ``k`` items from ``n``."""
    if n < 0 or k < 0:
        raise ValueError("n and k must be non-negative")
    return math.perm(n, k)


def hypotenuse(a: float, b: float) -> float:
    """Return the Euclidean distance ``sqrt(a^2 + b^2)``."""
    return math.hypot(a, b)


# --------------------------------------------------------------------------
# Trigonometry (degree-based wrappers around the radian built-ins)
# --------------------------------------------------------------------------

def sin_deg(angle: float) -> float:
    """Return the sine of ``angle`` given in degrees."""
    return math.sin(math.radians(angle))


def cos_deg(angle: float) -> float:
    """Return the cosine of ``angle`` given in degrees."""
    return math.cos(math.radians(angle))


def tan_deg(angle: float) -> float:
    """Return the tangent of ``angle`` given in degrees."""
    if (angle - 90) % 180 == 0:
        raise ValueError(f"tangent is undefined at {angle} degrees")
    return math.tan(math.radians(angle))


# --------------------------------------------------------------------------
# Descriptive statistics
# --------------------------------------------------------------------------

def mean(values: Sequence[float]) -> float:
    """Return the arithmetic mean of ``values``."""
    if not values:
        raise ValueError("mean requires at least one value")
    return math.fsum(values) / len(values)


def median(values: Sequence[float]) -> float:
    """Return the median of ``values``."""
    if not values:
        raise ValueError("median requires at least one value")
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return float(ordered[mid])
    return (ordered[mid - 1] + ordered[mid]) / 2


def variance(values: Sequence[float], sample: bool = True) -> float:
    """Return the variance of ``values``.

    With ``sample=True`` (the default) the unbiased sample variance is used
    (Bessel's correction, dividing by ``n - 1``); otherwise the population
    variance is returned.
    """
    n = len(values)
    minimum = 2 if sample else 1
    if n < minimum:
        raise ValueError("not enough data points to compute variance")
    mu = mean(values)
    total = math.fsum((x - mu) ** 2 for x in values)
    return total / (n - 1 if sample else n)


def std_dev(values: Sequence[float], sample: bool = True) -> float:
    """Return the standard deviation of ``values``."""
    return math.sqrt(variance(values, sample=sample))


# --------------------------------------------------------------------------
# Numerical methods
# --------------------------------------------------------------------------

def derivative(f: Callable[[float], float], x: float, h: float = 1e-6) -> float:
    """Approximate ``f'(x)`` using a symmetric difference quotient.

    The central difference is second-order accurate, so it is noticeably
    more precise than the naive forward difference for the same step size.
    """
    if h <= 0:
        raise ValueError("step size must be positive")
    return (f(x + h) - f(x - h)) / (2 * h)


def integrate(
    f: Callable[[float], float],
    a: float,
    b: float,
    intervals: int = 1000,
) -> float:
    """Approximate the definite integral of ``f`` from ``a`` to ``b``.

    Uses composite Simpson's rule; ``intervals`` is rounded up to the next
    even number as the rule requires paired subintervals.
    """
    if intervals < 2:
        raise ValueError("intervals must be at least 2")
    if intervals % 2:
        intervals += 1

    h = (b - a) / intervals
    total = f(a) + f(b)
    for i in range(1, intervals):
        weight = 4 if i % 2 else 2
        total += weight * f(a + i * h)
    return total * h / 3


def find_root(
    f: Callable[[float], float],
    low: float,
    high: float,
    tolerance: float = 1e-10,
    max_iterations: int = 200,
) -> float:
    """Find a root of ``f`` in ``[low, high]`` by bisection.

    ``f(low)`` and ``f(high)`` must have opposite signs so that a root is
    guaranteed to lie in the bracket.
    """
    f_low, f_high = f(low), f(high)
    if f_low == 0:
        return low
    if f_high == 0:
        return high
    if f_low * f_high > 0:
        raise ValueError("f(low) and f(high) must have opposite signs")

    for _ in range(max_iterations):
        mid = (low + high) / 2
        f_mid = f(mid)
        if f_mid == 0 or (high - low) / 2 < tolerance:
            return mid
        if f_low * f_mid < 0:
            high = mid
        else:
            low, f_low = mid, f_mid
    return (low + high) / 2


def solve_quadratic(a: float, b: float, c: float) -> tuple[complex, complex]:
    """Return both roots of ``a*x^2 + b*x + c = 0``.

    Roots are returned as complex numbers so that negative discriminants
    are handled uniformly.
    """
    if a == 0:
        raise ValueError("coefficient 'a' must be non-zero for a quadratic")
    discriminant = complex(b * b - 4 * a * c)
    root = discriminant ** 0.5
    return (-b + root) / (2 * a), (-b - root) / (2 * a)


# --------------------------------------------------------------------------
# Unit conversions
# --------------------------------------------------------------------------

def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert degrees Celsius to degrees Fahrenheit."""
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert degrees Fahrenheit to degrees Celsius."""
    return (fahrenheit - 32) * 5 / 9


def celsius_to_kelvin(celsius: float) -> float:
    """Convert degrees Celsius to kelvin."""
    kelvin = celsius + 273.15
    if kelvin < 0:
        raise ValueError("temperature is below absolute zero")
    return kelvin


# --------------------------------------------------------------------------
# Demo
# --------------------------------------------------------------------------

def _demo() -> None:
    samples = [2.5, 3.1, 4.8, 5.0, 6.2, 7.7]

    print("Elementary")
    print(f"  2^10            = {power(2, 10)}")
    print(f"  cube root of -8 = {nth_root(-8, 3)}")
    print(f"  log2(1024)      = {log(1024, 2)}")
    print(f"  10!             = {factorial(10)}")
    print(f"  C(52, 5)        = {combinations(52, 5)}")

    print("\nTrigonometry")
    print(f"  sin(30 deg)     = {sin_deg(30):.6f}")
    print(f"  cos(60 deg)     = {cos_deg(60):.6f}")

    print("\nStatistics")
    print(f"  data            = {samples}")
    print(f"  mean            = {mean(samples):.4f}")
    print(f"  median          = {median(samples):.4f}")
    print(f"  std dev         = {std_dev(samples):.4f}")

    print("\nNumerical methods")
    print(f"  d/dx x^2 at x=3 = {derivative(lambda x: x ** 2, 3):.6f}")
    print(f"  integral sin(x) over [0, pi] = {integrate(math.sin, 0, math.pi):.6f}")
    print(f"  root of x^2 - 2 = {find_root(lambda x: x * x - 2, 0, 2):.10f}")
    print(f"  roots of x^2 + 2x + 5 = {solve_quadratic(1, 2, 5)}")

    print("\nConversions")
    print(f"  100 C           = {celsius_to_fahrenheit(100)} F")
    print(f"  98.6 F          = {fahrenheit_to_celsius(98.6):.2f} C")
    print(f"  25 C            = {celsius_to_kelvin(25)} K")

    print("\nConstants")
    print(f"  c               = {SPEED_OF_LIGHT} m/s")
    print(f"  h               = {PLANCK} J*s")
    print(f"  N_A             = {AVOGADRO} 1/mol")


if __name__ == "__main__":
    _demo()
