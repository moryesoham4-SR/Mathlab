"""
MathMate Input Validation Module
"""

def validate_gcd_input(a: int, b: int):
    """Validates GCD inputs."""
    if a == 0 and b == 0:
        return False, "gcd(0, 0) is undefined."
    return True, None


def validate_permcomb_input(n: int, r: int):
    """Validates Permutation and Combination inputs."""
    if n < 0 or r < 0:
        return False, "Inputs n and r must be non-negative integers."
    if r > n:
        return False, f"Invalid input: r ({r}) cannot be greater than n ({n})."
    if n > 1000:
        return False, "Input n is too large (maximum supported is 1000)."
    return True, None


def validate_complex_division(z2_real: float, z2_imag: float):
    """Validates complex division denominator."""
    if abs(z2_real) < 1e-9 and abs(z2_imag) < 1e-9:
        return False, "Division by zero complex number (0 + 0i) is undefined."
    return True, None
