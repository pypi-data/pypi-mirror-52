"""Align polynomials."""
import numpy
import numpoly


def align_polynomials(*polys):
    """
    Align polynomial such that dimensionality, shape, etc. are compatible.

    Args:
        poly1, poly2, ... (numpoly.ndpoly, array_like):
            Polynomial to make adjustment to.

    Returns:
        (Tuple[numpoly, ...]):
            Same as ``polys``, but internal adjustments made to make them
            compatible for further operations.
    """
    polys = align_polynomial_shape(*polys)
    polys = align_polynomial_indeterminants(*polys)
    polys = align_polynomial_exponents(*polys)
    return polys


def align_polynomial_shape(*polys):
    """
    Align polynomial by shape.

    Args:
        poly1, poly2, ... (numpoly.ndpoly, array_like):
            Polynomial to make adjustment to.

    Returns:
        (Tuple[numpoly, ...]):
            Same as ``polys``, but internal adjustments made to make them
            compatible for further operations.

    Examples:
        >>> x, y = numpoly.symbols("x y")
        >>> poly1 = 4*x
        >>> poly2 = numpoly.polynomial([[2*x+1, 3*x-y]])
        >>> print(poly1)
        4*x
        >>> print(poly2)
        [[1+2*x -y+3*x]]
        >>> print(poly1.shape)
        ()
        >>> print(poly2.shape)
        (1, 2)
        >>> poly1, poly2 = numpoly.align_polynomial_shape(poly1, poly2)
        >>> print(poly1)
        [[4*x 4*x]]
        >>> print(poly2)
        [[1+2*x -y+3*x]]
        >>> print(poly1.shape)
        (1, 2)
        >>> print(poly2.shape)
        (1, 2)
    """
    polys = [numpoly.aspolynomial(poly) for poly in polys]
    common = 1
    for poly in polys:
        common = numpy.ones(poly.coefficients[0].shape, dtype=int)*common

    polys = [numpoly.polynomial_from_attributes(
        exponents=poly.exponents,
        coefficients=[coeff*common for coeff in poly.coefficients],
        indeterminants=poly.indeterminants,
    ) for poly in polys]
    assert numpy.all(common.shape == poly.shape for poly in polys)
    return tuple(polys)


def align_polynomial_indeterminants(*polys):
    """
    Align polynomial by indeterminants.

    Args:
        poly1, poly2, ... (numpoly.ndpoly, array_like):
            Polynomial to make adjustment to.

    Returns:
        (Tuple[numpoly, ...]):
            Same as ``polys``, but internal adjustments made to make them
            compatible for further operations.

    Examples:
        >>> x, y = numpoly.symbols("x y")
        >>> poly1, poly2 = numpoly.polynomial([2*x+1, 3*x-y])
        >>> print(poly1)
        1+2*x
        >>> print(poly2)
        -y+3*x
        >>> print(poly1.indeterminants)
        [x]
        >>> print(poly2.indeterminants)
        [x y]
        >>> poly1, poly2 = numpoly.align_polynomial_indeterminants(poly1, poly2)
        >>> print(poly1)
        1+2*x
        >>> print(poly2)
        -y+3*x
        >>> print(poly1.indeterminants)
        [x y]
        >>> print(poly2.indeterminants)
        [x y]
    """
    polys = [numpoly.aspolynomial(poly) for poly in polys]
    common_indeterminates = sorted({
        indeterminant
        for poly in polys
        for indeterminant in poly._indeterminants
    })
    for idx, poly in enumerate(polys):
        indices = numpy.array([
            common_indeterminates.index(indeterminant)
            for indeterminant in poly._indeterminants
        ])
        exponents = numpy.zeros(
            (len(poly._exponents), len(common_indeterminates)), dtype=int)
        exponents[:, indices] = poly.exponents
        polys[idx] = numpoly.polynomial_from_attributes(
            exponents=exponents,
            coefficients=poly.coefficients,
            indeterminants=common_indeterminates,
            trim=False,
        )

    return tuple(polys)


def align_polynomial_exponents(*polys):
    polys = [numpoly.aspolynomial(poly) for poly in polys]
    if not all(
            polys[0]._indeterminants == poly._indeterminants
            for poly in polys
    ):
        polys = list(align_polynomial_indeterminants(*polys))

    global_exponents = sorted({
        tuple(exponent) for poly in polys for exponent in poly.exponents})
    for idx, poly in enumerate(polys):
        lookup = {
            tuple(exponent): coefficient
            for exponent, coefficient in zip(
                poly.exponents, poly.coefficients)
        }
        zeros = numpy.zeros(poly.shape, dtype=poly.dtype)
        coefficients = [lookup.get(exponent, zeros)
                        for exponent in global_exponents]
        polys[idx] = numpoly.polynomial_from_attributes(
            exponents=global_exponents,
            coefficients=coefficients,
            indeterminants=poly._indeterminants,
            trim=False,
        )
    return tuple(polys)
