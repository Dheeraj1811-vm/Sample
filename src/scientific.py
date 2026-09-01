"""Scientific calculation utilities.

A dependency-free collection of common scientific helpers: elementary
functions, trigonometry, statistics, vector algebra, numerical methods,
unit conversions, and physical constants and the formulas that use them.

The module doubles as a command-line calculator. Run a subcommand, or run
it with no arguments for a short demonstration:

    python src/scientific.py mean 2.5 3.1 4.8
    python src/scientific.py eval "2 * sin_deg(30) + log(100, 10)"
    python src/scientific.py repl
    python src/scientific.py --help
"""

from __future__ import annotations

import argparse
import json
import math
import operator
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from typing import Callable, Iterable, Sequence

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
    "asin_deg",
    "acos_deg",
    "atan_deg",
    "atan2_deg",
    "mean",
    "median",
    "variance",
    "std_dev",
    "mode",
    "percentile",
    "correlation",
    "linear_regression",
    "dot",
    "magnitude",
    "normalize",
    "angle_between_deg",
    "derivative",
    "integrate",
    "find_root",
    "newton_root",
    "solve_quadratic",
    "celsius_to_fahrenheit",
    "fahrenheit_to_celsius",
    "celsius_to_kelvin",
    "kelvin_to_celsius",
    "fahrenheit_to_kelvin",
    "kelvin_to_fahrenheit",
    "gravitational_force",
    "photon_energy",
    "ideal_gas_pressure",
    "evaluate",
    "repl",
    "main",
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


def asin_deg(value: float) -> float:
    """Return the arcsine of ``value`` in degrees, within [-90, 90]."""
    if not -1.0 <= value <= 1.0:
        raise ValueError("arcsine is undefined outside [-1, 1]")
    return math.degrees(math.asin(value))


def acos_deg(value: float) -> float:
    """Return the arccosine of ``value`` in degrees, within [0, 180]."""
    if not -1.0 <= value <= 1.0:
        raise ValueError("arccosine is undefined outside [-1, 1]")
    return math.degrees(math.acos(value))


def atan_deg(value: float) -> float:
    """Return the arctangent of ``value`` in degrees, within (-90, 90)."""
    return math.degrees(math.atan(value))


def atan2_deg(y: float, x: float) -> float:
    """Return the angle of the point ``(x, y)`` in degrees, within (-180, 180].

    Unlike :func:`atan_deg` this keeps the quadrant information, so it is the
    right choice for converting cartesian coordinates to a bearing.
    """
    return math.degrees(math.atan2(y, x))


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


def mode(values: Sequence[float]) -> float:
    """Return the single most frequent value in ``values``.

    Raises ``ValueError`` when the data is multimodal, since there is no
    sensible way to pick between tied candidates.
    """
    if not values:
        raise ValueError("mode requires at least one value")
    ranked = Counter(values).most_common()
    if len(ranked) > 1 and ranked[0][1] == ranked[1][1]:
        raise ValueError("data is multimodal; no unique mode")
    return float(ranked[0][0])


def percentile(values: Sequence[float], p: float) -> float:
    """Return the ``p``-th percentile of ``values`` for ``0 <= p <= 100``.

    Ranks are interpolated linearly between the two neighbouring order
    statistics, matching the default convention of ``numpy.percentile``.
    """
    if not values:
        raise ValueError("percentile requires at least one value")
    if not 0 <= p <= 100:
        raise ValueError("percentile must be between 0 and 100")
    ordered = sorted(values)
    rank = (len(ordered) - 1) * p / 100
    low = math.floor(rank)
    high = math.ceil(rank)
    if low == high:
        return float(ordered[low])
    return ordered[low] + (ordered[high] - ordered[low]) * (rank - low)


def correlation(xs: Sequence[float], ys: Sequence[float]) -> float:
    """Return the Pearson correlation coefficient of ``xs`` and ``ys``."""
    if len(xs) != len(ys):
        raise ValueError("inputs must have the same length")
    if len(xs) < 2:
        raise ValueError("correlation requires at least two data points")
    mx, my = mean(xs), mean(ys)
    covariance = math.fsum((x - mx) * (y - my) for x, y in zip(xs, ys))
    spread_x = math.fsum((x - mx) ** 2 for x in xs)
    spread_y = math.fsum((y - my) ** 2 for y in ys)
    if spread_x == 0 or spread_y == 0:
        raise ValueError("correlation is undefined when an input is constant")
    return covariance / math.sqrt(spread_x * spread_y)


def linear_regression(
    xs: Sequence[float], ys: Sequence[float]
) -> tuple[float, float]:
    """Return ``(slope, intercept)`` of the least-squares fit of ``ys`` on ``xs``.

    Only the fitted line is returned; pair this with :func:`correlation` when
    you also need a goodness-of-fit measure, since ``r`` is undefined for the
    constant-``ys`` case that this function handles fine.
    """
    if len(xs) != len(ys):
        raise ValueError("inputs must have the same length")
    if len(xs) < 2:
        raise ValueError("linear regression requires at least two data points")
    mx, my = mean(xs), mean(ys)
    spread_x = math.fsum((x - mx) ** 2 for x in xs)
    if spread_x == 0:
        raise ValueError("slope is undefined when every x is identical")
    slope = math.fsum((x - mx) * (y - my) for x, y in zip(xs, ys)) / spread_x
    return slope, my - slope * mx


# --------------------------------------------------------------------------
# Vector algebra
# --------------------------------------------------------------------------

def dot(u: Sequence[float], v: Sequence[float]) -> float:
    """Return the dot product of two vectors of equal length."""
    if len(u) != len(v):
        raise ValueError("vectors must have the same length")
    if not u:
        raise ValueError("vectors must not be empty")
    return math.fsum(a * b for a, b in zip(u, v))


def magnitude(v: Sequence[float]) -> float:
    """Return the Euclidean length of ``v``."""
    if not v:
        raise ValueError("vector must not be empty")
    return math.hypot(*v)


def normalize(v: Sequence[float]) -> list[float]:
    """Return a unit vector pointing in the same direction as ``v``."""
    length = magnitude(v)
    if length == 0:
        raise ValueError("cannot normalize the zero vector")
    return [x / length for x in v]


def angle_between_deg(u: Sequence[float], v: Sequence[float]) -> float:
    """Return the angle between ``u`` and ``v`` in degrees, within [0, 180]."""
    scale = magnitude(u) * magnitude(v)
    if scale == 0:
        raise ValueError("angle is undefined for the zero vector")
    # Clamp first: rounding can push the cosine a hair outside [-1, 1] for
    # parallel vectors, which would make acos_deg reject a valid input.
    return acos_deg(max(-1.0, min(1.0, dot(u, v) / scale)))


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


def newton_root(
    f: Callable[[float], float],
    x0: float,
    fprime: Callable[[float], float] | None = None,
    tolerance: float = 1e-12,
    max_iterations: int = 100,
) -> float:
    """Find a root of ``f`` near ``x0`` using the Newton-Raphson method.

    When ``fprime`` is omitted the slope is approximated with
    :func:`derivative`. Convergence is quadratic near a simple root, so this
    is much faster than :func:`find_root` -- but it needs a good starting
    guess and is not guaranteed to converge at all.
    """
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")

    x = x0
    for _ in range(max_iterations):
        fx = f(x)
        if abs(fx) < tolerance:
            return x
        slope = fprime(x) if fprime is not None else derivative(f, x)
        if slope == 0:
            raise ValueError("derivative vanished; Newton's method cannot proceed")
        step = fx / slope
        x -= step
        if abs(step) < tolerance:
            return x
    raise ValueError(
        f"Newton's method did not converge within {max_iterations} iterations"
    )


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


def kelvin_to_celsius(kelvin: float) -> float:
    """Convert kelvin to degrees Celsius."""
    if kelvin < 0:
        raise ValueError("temperature is below absolute zero")
    return kelvin - 273.15


def fahrenheit_to_kelvin(fahrenheit: float) -> float:
    """Convert degrees Fahrenheit to kelvin."""
    return celsius_to_kelvin(fahrenheit_to_celsius(fahrenheit))


def kelvin_to_fahrenheit(kelvin: float) -> float:
    """Convert kelvin to degrees Fahrenheit."""
    return celsius_to_fahrenheit(kelvin_to_celsius(kelvin))


# --------------------------------------------------------------------------
# Physics (SI units throughout, built on the constants above)
# --------------------------------------------------------------------------

def gravitational_force(m1: float, m2: float, distance: float) -> float:
    """Return the Newtonian attraction between two masses, in newtons.

    Masses are in kilograms and ``distance`` -- the separation of the two
    centres of mass -- is in metres.
    """
    if m1 < 0 or m2 < 0:
        raise ValueError("masses must be non-negative")
    if distance <= 0:
        raise ValueError("distance must be positive")
    return GRAVITATIONAL * m1 * m2 / (distance * distance)


def photon_energy(wavelength: float) -> float:
    """Return the energy in joules of a photon of ``wavelength`` metres."""
    if wavelength <= 0:
        raise ValueError("wavelength must be positive")
    return PLANCK * SPEED_OF_LIGHT / wavelength


def ideal_gas_pressure(moles: float, temperature: float, volume: float) -> float:
    """Return the pressure in pascals implied by ``PV = nRT``.

    ``temperature`` is in kelvin and ``volume`` in cubic metres.
    """
    if moles < 0:
        raise ValueError("amount of substance must be non-negative")
    if temperature < 0:
        raise ValueError("temperature is below absolute zero")
    if volume <= 0:
        raise ValueError("volume must be positive")
    return moles * GAS_CONSTANT * temperature / volume


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
    print(f"  asin(0.5)       = {asin_deg(0.5):.6f} deg")
    print(f"  atan2(1, -1)    = {atan2_deg(1, -1):.6f} deg")

    print("\nStatistics")
    print(f"  data            = {samples}")
    print(f"  mean            = {mean(samples):.4f}")
    print(f"  median          = {median(samples):.4f}")
    print(f"  std dev         = {std_dev(samples):.4f}")
    print(f"  90th percentile = {percentile(samples, 90):.4f}")
    print(f"  corr with index = {correlation(samples, range(len(samples))):.4f}")
    slope, intercept = linear_regression(range(len(samples)), samples)
    print(f"  best fit line   = {slope:.4f}x + {intercept:.4f}")

    print("\nVectors")
    print(f"  [1,2,3].[4,5,6] = {dot([1, 2, 3], [4, 5, 6])}")
    print(f"  |[3, 4]|        = {magnitude([3, 4])}")
    print(f"  unit [3, 4]     = {normalize([3, 4])}")
    print(f"  angle [1,0],[1,1] = {angle_between_deg([1, 0], [1, 1]):.4f} deg")

    print("\nNumerical methods")
    print(f"  d/dx x^2 at x=3 = {derivative(lambda x: x ** 2, 3):.6f}")
    print(f"  integral sin(x) over [0, pi] = {integrate(math.sin, 0, math.pi):.6f}")
    print(f"  root of x^2 - 2 = {find_root(lambda x: x * x - 2, 0, 2):.10f}")
    print(f"  same via Newton = {newton_root(lambda x: x * x - 2, 1):.10f}")
    print(f"  roots of x^2 + 2x + 5 = {solve_quadratic(1, 2, 5)}")

    print("\nConversions")
    print(f"  100 C           = {celsius_to_fahrenheit(100)} F")
    print(f"  98.6 F          = {fahrenheit_to_celsius(98.6):.2f} C")
    print(f"  25 C            = {celsius_to_kelvin(25)} K")
    print(f"  300 K           = {kelvin_to_celsius(300):.2f} C")
    print(f"  98.6 F          = {fahrenheit_to_kelvin(98.6):.2f} K")

    print("\nPhysics")
    print(f"  Earth-Moon pull = {gravitational_force(5.972e24, 7.348e22, 3.844e8):.4e} N")
    print(f"  E of 500 nm     = {photon_energy(500e-9):.4e} J")
    print(f"  1 mol at STP    = {ideal_gas_pressure(1, 273.15, 0.022414):.1f} Pa")

    print("\nConstants")
    print(f"  c               = {SPEED_OF_LIGHT} m/s")
    print(f"  h               = {PLANCK} J*s")
    print(f"  N_A             = {AVOGADRO} 1/mol")


# --------------------------------------------------------------------------
# Expression evaluation
# --------------------------------------------------------------------------

_TOKEN_PATTERN = re.compile(
    r"""
      (?P<space>\s+)
    | (?P<number>\d+\.?\d*(?:[eE][-+]?\d+)?|\.\d+(?:[eE][-+]?\d+)?)
    | (?P<name>[A-Za-z_][A-Za-z_0-9]*)
    | (?P<operator>\*\*|[-+*/%^(),\[\]=])
    """,
    re.VERBOSE,
)

_BINARY_OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod,
    "^": operator.pow,
}

# These take a function as their first argument. In an expression that
# argument is left unevaluated and bound to the variable ``x`` instead, so
# ``derivative(x^2, 3)`` reads the way it would on paper.
_DEFERRED_FIRST_ARGUMENT = frozenset(
    {"derivative", "integrate", "find_root", "newton_root"}
)


@dataclass(frozen=True)
class _Token:
    kind: str
    text: str
    position: int


@dataclass(frozen=True)
class _Number:
    value: float


@dataclass(frozen=True)
class _Variable:
    name: str


@dataclass(frozen=True)
class _Series:
    items: tuple


@dataclass(frozen=True)
class _Unary:
    op: str
    operand: object


@dataclass(frozen=True)
class _Binary:
    op: str
    left: object
    right: object


@dataclass(frozen=True)
class _Invocation:
    name: str
    arguments: tuple


def _tokenize(text: str) -> list[_Token]:
    """Split ``text`` into tokens, rejecting anything the grammar cannot use."""
    tokens: list[_Token] = []
    position = 0
    while position < len(text):
        match = _TOKEN_PATTERN.match(text, position)
        if match is None:
            raise ValueError(f"unexpected character {text[position]!r} at {position}")
        kind = match.lastgroup
        if kind != "space":
            # "**" is accepted as a synonym for "^" so that Python habits work.
            token = "^" if match.group() == "**" else match.group()
            tokens.append(_Token(kind, token, position))
        position = match.end()
    return tokens


class _Parser:
    """A recursive descent parser for the calculator grammar.

    The grammar, loosest binding first::

        expression := term (("+" | "-") term)*
        term       := unary (("*" | "/" | "%") unary)*
        unary      := ("+" | "-") unary | power
        power      := primary ("^" unary)?
        primary    := NUMBER | NAME | NAME "(" args ")" | "[" args "]"
                    | "(" expression ")"

    ``^`` binds tighter than unary minus and is right associative, so
    ``-2^2`` is ``-4`` and ``2^-1`` is ``0.5``, matching normal notation.
    """

    def __init__(self, tokens: Sequence[_Token]) -> None:
        self._tokens = tokens
        self._index = 0

    def parse(self) -> object:
        """Parse a complete expression and insist that nothing is left over."""
        node = self._expression()
        if self._peek() is not None:
            raise ValueError(f"unexpected {self._peek().text!r} at {self._peek().position}")
        return node

    def _peek(self) -> _Token | None:
        return self._tokens[self._index] if self._index < len(self._tokens) else None

    def _take(self, text: str) -> bool:
        token = self._peek()
        if token is not None and token.text == text:
            self._index += 1
            return True
        return False

    def _expect(self, text: str) -> None:
        if not self._take(text):
            token = self._peek()
            where = f"at {token.position}" if token else "at end of expression"
            raise ValueError(f"expected {text!r} {where}")

    def _expression(self) -> object:
        node = self._term()
        while (token := self._peek()) is not None and token.text in ("+", "-"):
            self._index += 1
            node = _Binary(token.text, node, self._term())
        return node

    def _term(self) -> object:
        node = self._unary()
        while (token := self._peek()) is not None and token.text in ("*", "/", "%"):
            self._index += 1
            node = _Binary(token.text, node, self._unary())
        return node

    def _unary(self) -> object:
        token = self._peek()
        if token is not None and token.text in ("+", "-"):
            self._index += 1
            return _Unary(token.text, self._unary())
        return self._power()

    def _power(self) -> object:
        base = self._primary()
        if self._take("^"):
            return _Binary("^", base, self._unary())
        return base

    def _primary(self) -> object:
        token = self._peek()
        if token is None:
            raise ValueError("expression ended unexpectedly")
        self._index += 1

        if token.kind == "number":
            return _Number(float(token.text))
        if token.kind == "name":
            if self._take("("):
                return _Invocation(token.text, self._arguments(")"))
            return _Variable(token.text)
        if token.text == "[":
            return _Series(self._arguments("]"))
        if token.text == "(":
            node = self._expression()
            self._expect(")")
            return node
        raise ValueError(f"unexpected {token.text!r} at {token.position}")

    def _arguments(self, closing: str) -> tuple:
        """Parse a comma-separated argument or element list up to ``closing``."""
        if self._take(closing):
            return ()
        arguments = [self._expression()]
        while self._take(","):
            arguments.append(self._expression())
        self._expect(closing)
        return tuple(arguments)


def _expression_namespace() -> dict[str, object]:
    """Return the names an expression may use: the public API plus a few aliases."""
    namespace: dict[str, object] = {
        name: globals()[name]
        for name in __all__
        if name not in ("evaluate", "repl", "main")
    }
    namespace.update(
        pi=math.pi, e=math.e, tau=math.tau, sqrt=math.sqrt, exp=math.exp, abs=abs
    )
    return namespace


_NAMESPACE = _expression_namespace()


def _evaluate_node(node: object, variables: dict[str, object]) -> object:
    """Evaluate one parsed node against ``variables`` and the shared namespace."""
    if isinstance(node, _Number):
        return node.value

    if isinstance(node, _Variable):
        if node.name in variables:
            return variables[node.name]
        if node.name in _NAMESPACE and not callable(_NAMESPACE[node.name]):
            return _NAMESPACE[node.name]
        if node.name in _NAMESPACE:
            raise ValueError(f"{node.name!r} is a function; call it as {node.name}(...)")
        raise ValueError(f"unknown name {node.name!r}")

    if isinstance(node, _Series):
        return [_evaluate_node(item, variables) for item in node.items]

    if isinstance(node, _Unary):
        value = _evaluate_node(node.operand, variables)
        return -value if node.op == "-" else +value

    if isinstance(node, _Binary):
        left = _evaluate_node(node.left, variables)
        right = _evaluate_node(node.right, variables)
        if node.op in ("/", "%") and right == 0:
            raise ValueError("division by zero")
        return _BINARY_OPERATORS[node.op](left, right)

    if isinstance(node, _Invocation):
        function = _NAMESPACE.get(node.name)
        if function is None:
            raise ValueError(f"unknown function {node.name!r}")
        if not callable(function):
            raise ValueError(f"{node.name!r} is a constant, not a function")
        if node.name in _DEFERRED_FIRST_ARGUMENT:
            if not node.arguments:
                raise ValueError(f"{node.name} needs an expression to work on")
            body = node.arguments[0]
            arguments = [lambda value: _evaluate_node(body, {**variables, "x": value})]
            arguments.extend(
                _evaluate_node(argument, variables) for argument in node.arguments[1:]
            )
        else:
            arguments = [
                _evaluate_node(argument, variables) for argument in node.arguments
            ]
        try:
            return function(*arguments)
        except TypeError as exc:
            raise ValueError(f"bad call to {node.name}: {exc}") from None

    raise ValueError(f"cannot evaluate {node!r}")


def evaluate(expression: str, variables: dict[str, object] | None = None) -> object:
    """Evaluate a calculator ``expression`` and return its value.

    Expressions use ``+ - * / % ^`` (``**`` is accepted for ``^``), parentheses,
    ``[1, 2, 3]`` lists for the functions that take a series, and any public
    name in this module::

        >>> evaluate("2 * sin_deg(30) + log(100, 10)")
        3.0
        >>> evaluate("mean([1, 2, 3, 4])")
        2.5
        >>> evaluate("derivative(x^2, 3)")
        6.000000000838668

    ``variables`` is read and written in place, so ``x = 3`` in one call is
    visible to the next. Anything malformed raises ``ValueError``; nothing is
    passed to :func:`eval`, and only the names above are reachable.
    """
    if variables is None:
        variables = {}

    tokens = _tokenize(expression)
    if not tokens:
        raise ValueError("empty expression")

    # An assignment is the only statement form: NAME "=" expression.
    if len(tokens) > 1 and tokens[0].kind == "name" and tokens[1].text == "=":
        name = tokens[0].text
        if name in _NAMESPACE:
            raise ValueError(f"{name!r} is part of the calculator and cannot be reused")
        value = _evaluate_node(_Parser(tokens[2:]).parse(), variables)
        variables[name] = value
        return value

    return _evaluate_node(_Parser(tokens).parse(), variables)


_REPL_HELP = """\
Type an expression, or an assignment such as "radius = 2.5".
"_" holds the previous result, "vars" lists what you have defined,
and "quit" leaves. Lists are written [1, 2, 3]:

  mean([2.5, 3.1, 4.8])        derivative(x^2, 3)
  hypotenuse(3, 4)             integrate(sin_deg(x), 0, 180)
"""


def _prompt_lines() -> Iterable[str]:
    """Yield lines typed at the prompt, stopping at EOF or interrupt."""
    while True:
        try:
            yield input("sci> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return


def repl(lines: Iterable[str] | None = None) -> int:
    """Run the interactive calculator, returning a process exit code.

    ``lines`` exists for testing: pass an iterable of input lines to drive the
    loop without a terminal. When it is ``None`` the lines are read from the
    prompt.
    """
    interactive = lines is None
    if interactive:
        print('Scientific calculator. Type "help" for help, "quit" to leave.')

    variables: dict[str, object] = {}
    for line in _prompt_lines() if interactive else lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line in ("quit", "exit"):
            break
        if line == "help":
            print(_REPL_HELP)
            continue
        if line == "vars":
            for name, value in sorted(variables.items()):
                if name != "_":
                    print(f"{name} = {_format_value(value)}")
            continue

        try:
            result = evaluate(line, variables)
        except (ValueError, OverflowError, ZeroDivisionError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            continue

        variables["_"] = result
        print(_format_value(result))
    return 0


# --------------------------------------------------------------------------
# Command-line interface
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class _Argument:
    """A positional argument of a subcommand.

    ``kind`` is ``"float"``, ``"int"``, ``"floats"`` (one or more numbers,
    written space separated) or ``"vector"`` (one comma-separated group, used
    where a command needs two sequences and spaces would be ambiguous).
    """

    name: str
    kind: str


@dataclass(frozen=True)
class _Option:
    """An optional ``--name`` argument of a subcommand."""

    name: str
    kind: str  # "float" or "flag"
    default: object
    help: str


@dataclass(frozen=True)
class _Command:
    """One subcommand: what to call, and how to parse what it is called with."""

    call: Callable[..., object]
    help: str
    arguments: tuple[_Argument, ...] = ()
    options: tuple[_Option, ...] = field(default_factory=tuple)


def _vector(text: str) -> list[float]:
    """Parse a comma-separated vector such as ``"1,2,3"`` for argparse."""
    try:
        return [float(part) for part in text.split(",")]
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"{text!r} is not a comma-separated list of numbers"
        ) from None


_COMMANDS: dict[str, _Command] = {
    # Elementary
    "power": _Command(
        power,
        "Raise a base to an exponent.",
        (_Argument("base", "float"), _Argument("exponent", "float")),
    ),
    "nth-root": _Command(
        nth_root,
        "Take the real n-th root of a value.",
        (_Argument("value", "float"), _Argument("n", "int")),
    ),
    "log": _Command(
        lambda value, base: log(value, base),
        "Take a logarithm (natural unless --base is given).",
        (_Argument("value", "float"),),
        (_Option("base", "float", math.e, "logarithm base (default: e)"),),
    ),
    "factorial": _Command(
        factorial, "Compute n!.", (_Argument("n", "int"),)
    ),
    "combinations": _Command(
        combinations,
        "Count the ways to choose k items from n.",
        (_Argument("n", "int"), _Argument("k", "int")),
    ),
    "permutations": _Command(
        permutations,
        "Count the ordered arrangements of k items from n.",
        (_Argument("n", "int"), _Argument("k", "int")),
    ),
    "hypotenuse": _Command(
        hypotenuse,
        "Compute sqrt(a^2 + b^2).",
        (_Argument("a", "float"), _Argument("b", "float")),
    ),
    # Trigonometry
    "sin-deg": _Command(sin_deg, "Sine of an angle in degrees.", (_Argument("angle", "float"),)),
    "cos-deg": _Command(cos_deg, "Cosine of an angle in degrees.", (_Argument("angle", "float"),)),
    "tan-deg": _Command(tan_deg, "Tangent of an angle in degrees.", (_Argument("angle", "float"),)),
    "asin-deg": _Command(asin_deg, "Arcsine, in degrees.", (_Argument("value", "float"),)),
    "acos-deg": _Command(acos_deg, "Arccosine, in degrees.", (_Argument("value", "float"),)),
    "atan-deg": _Command(atan_deg, "Arctangent, in degrees.", (_Argument("value", "float"),)),
    "atan2-deg": _Command(
        atan2_deg,
        "Angle of the point (x, y), in degrees, keeping the quadrant.",
        (_Argument("y", "float"), _Argument("x", "float")),
    ),
    # Statistics
    "mean": _Command(mean, "Arithmetic mean.", (_Argument("values", "floats"),)),
    "median": _Command(median, "Median.", (_Argument("values", "floats"),)),
    "mode": _Command(mode, "Most frequent value.", (_Argument("values", "floats"),)),
    "percentile": _Command(
        lambda percent, values: percentile(values, percent),
        "Percentile, interpolated between ranks.",
        (_Argument("percent", "float"), _Argument("values", "floats")),
    ),
    "variance": _Command(
        lambda values, population: variance(values, sample=not population),
        "Variance (sample by default).",
        (_Argument("values", "floats"),),
        (_Option("population", "flag", False, "use the population variance"),),
    ),
    "std-dev": _Command(
        lambda values, population: std_dev(values, sample=not population),
        "Standard deviation (sample by default).",
        (_Argument("values", "floats"),),
        (_Option("population", "flag", False, "use the population deviation"),),
    ),
    "correlation": _Command(
        correlation,
        "Pearson correlation of two comma-separated series.",
        (_Argument("xs", "vector"), _Argument("ys", "vector")),
    ),
    "linear-regression": _Command(
        linear_regression,
        "Least-squares slope and intercept of two comma-separated series.",
        (_Argument("xs", "vector"), _Argument("ys", "vector")),
    ),
    # Vectors
    "dot": _Command(
        dot,
        "Dot product of two comma-separated vectors.",
        (_Argument("u", "vector"), _Argument("v", "vector")),
    ),
    "magnitude": _Command(
        magnitude, "Euclidean length of a vector.", (_Argument("v", "floats"),)
    ),
    "normalize": _Command(
        normalize, "Unit vector in the same direction.", (_Argument("v", "floats"),)
    ),
    "angle-between-deg": _Command(
        angle_between_deg,
        "Angle between two comma-separated vectors, in degrees.",
        (_Argument("u", "vector"), _Argument("v", "vector")),
    ),
    # Numerical methods
    "solve-quadratic": _Command(
        solve_quadratic,
        "Both roots of a*x^2 + b*x + c = 0.",
        (_Argument("a", "float"), _Argument("b", "float"), _Argument("c", "float")),
    ),
    # Conversions
    "celsius-to-fahrenheit": _Command(
        celsius_to_fahrenheit, "Celsius to Fahrenheit.", (_Argument("celsius", "float"),)
    ),
    "fahrenheit-to-celsius": _Command(
        fahrenheit_to_celsius, "Fahrenheit to Celsius.", (_Argument("fahrenheit", "float"),)
    ),
    "celsius-to-kelvin": _Command(
        celsius_to_kelvin, "Celsius to kelvin.", (_Argument("celsius", "float"),)
    ),
    "kelvin-to-celsius": _Command(
        kelvin_to_celsius, "Kelvin to Celsius.", (_Argument("kelvin", "float"),)
    ),
    "fahrenheit-to-kelvin": _Command(
        fahrenheit_to_kelvin, "Fahrenheit to kelvin.", (_Argument("fahrenheit", "float"),)
    ),
    "kelvin-to-fahrenheit": _Command(
        kelvin_to_fahrenheit, "Kelvin to Fahrenheit.", (_Argument("kelvin", "float"),)
    ),
    # Physics
    "gravitational-force": _Command(
        gravitational_force,
        "Newtonian attraction between two masses (kg, kg, m).",
        (
            _Argument("m1", "float"),
            _Argument("m2", "float"),
            _Argument("distance", "float"),
        ),
    ),
    "photon-energy": _Command(
        photon_energy,
        "Energy of a photon of the given wavelength, in metres.",
        (_Argument("wavelength", "float"),),
    ),
    "ideal-gas-pressure": _Command(
        ideal_gas_pressure,
        "Pressure from PV = nRT (mol, K, m^3).",
        (
            _Argument("moles", "float"),
            _Argument("temperature", "float"),
            _Argument("volume", "float"),
        ),
    ),
}

# The constants are the upper-case half of the public API.
_CONSTANTS = {name: globals()[name] for name in __all__ if name.isupper()}

_EPILOG = """\
examples:
  %(prog)s mean 2.5 3.1 4.8            one sequence: space separated
  %(prog)s dot 1,2,3 4,5,6             two sequences: comma separated groups
  %(prog)s std-dev 2 4 4 4 5 5 7 9 --population
  %(prog)s log 1024 --base 2
  %(prog)s photon-energy 500e-9 --json
  %(prog)s eval "2 * sin_deg(30) + log(100, 10)"
  %(prog)s eval -- "-2^2"              -- first when it starts with a minus
  %(prog)s repl                        interactive prompt

The functions that take a function to work on -- derivative, integrate,
find_root and newton_root -- have no subcommand of their own; reach them
through eval, which binds the free variable x:

  %(prog)s eval "integrate(sin_deg(x), 0, 180)"
"""


def _format_number(value: float) -> str:
    """Render a float compactly, switching to exponent form at the extremes."""
    if math.isnan(value) or math.isinf(value):
        return str(value)
    if value == 0:
        return "0"
    if abs(value) < 1e-4 or abs(value) >= 1e7:
        return f"{value:.7e}"
    return f"{value:.6f}".rstrip("0").rstrip(".")


def _format_value(value: object) -> str:
    """Render a result for the terminal, one line per element of a sequence."""
    if isinstance(value, bool) or isinstance(value, int):
        return str(value)
    if isinstance(value, complex):
        real, imag = _format_number(value.real), _format_number(abs(value.imag))
        return f"{real}{'+' if value.imag >= 0 else '-'}{imag}j"
    if isinstance(value, float):
        return _format_number(value)
    if isinstance(value, (list, tuple)):
        return "\n".join(_format_value(item) for item in value)
    return str(value)


def _jsonable(value: object) -> object:
    """Convert a result into something :mod:`json` can encode."""
    if isinstance(value, complex):
        return {"real": value.real, "imag": value.imag}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def _build_parser() -> argparse.ArgumentParser:
    """Build the argument parser, one subparser per entry in ``_COMMANDS``."""
    parser = argparse.ArgumentParser(
        prog="scientific",
        description="Scientific calculator. Run without a command for a demo.",
        epilog=_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument(
        "--json", action="store_true", help="print the result as a JSON object"
    )

    subparsers = parser.add_subparsers(dest="command", metavar="command")
    subparsers.add_parser("demo", help="print a short demonstration of the module")
    subparsers.add_parser(
        "constants", parents=[shared], help="print the physical constants"
    )
    evaluation = subparsers.add_parser(
        "eval", parents=[shared], help="evaluate an expression"
    )
    evaluation.add_argument(
        "expression",
        nargs="+",
        help='for example "2 * sin_deg(30)"; put -- first if it starts with a minus',
    )
    subparsers.add_parser("repl", help="start the interactive calculator")

    types = {"float": float, "int": int, "floats": float, "vector": _vector}
    for name, command in _COMMANDS.items():
        sub = subparsers.add_parser(name, parents=[shared], help=command.help)
        for argument in command.arguments:
            sub.add_argument(
                argument.name,
                type=types[argument.kind],
                nargs="+" if argument.kind == "floats" else None,
            )
        for option in command.options:
            if option.kind == "flag":
                sub.add_argument(
                    f"--{option.name}", action="store_true", help=option.help
                )
            else:
                sub.add_argument(
                    f"--{option.name}",
                    type=float,
                    default=option.default,
                    help=option.help,
                )
    return parser


def _emit(name: str, result: object, as_json: bool) -> None:
    """Print ``result`` as plain text or as a JSON object."""
    if as_json:
        payload = {"function": name.replace("-", "_"), "result": _jsonable(result)}
        print(json.dumps(payload))
    else:
        print(_format_value(result))


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command line interface and return a process exit code."""
    args = _build_parser().parse_args(argv)

    if args.command is None or args.command == "demo":
        _demo()
        return 0

    if args.command == "constants":
        if args.json:
            print(json.dumps(_CONSTANTS))
        else:
            width = max(len(name) for name in _CONSTANTS)
            for name, value in _CONSTANTS.items():
                # repr, not _format_number: these are reference values, so
                # exact round-tripping matters more than compactness.
                print(f"{name:<{width}} = {value!r}")
        return 0

    if args.command == "repl":
        return repl()

    if args.command == "eval":
        expression = " ".join(args.expression)
        try:
            result = evaluate(expression)
        except (ValueError, OverflowError, ZeroDivisionError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        if args.json:
            print(
                json.dumps({"expression": expression, "result": _jsonable(result)})
            )
        else:
            print(_format_value(result))
        return 0

    command = _COMMANDS[args.command]
    positional = [getattr(args, argument.name) for argument in command.arguments]
    keywords = {option.name: getattr(args, option.name) for option in command.options}
    try:
        result = command.call(*positional, **keywords)
    except (ValueError, OverflowError, ZeroDivisionError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    _emit(args.command, result, args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
