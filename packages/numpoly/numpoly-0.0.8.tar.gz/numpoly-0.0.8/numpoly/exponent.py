"""Mapping between polynomial exponents and their string counterpart."""
from __future__ import unicode_literals
from string import printable  # pylint: disable=no-name-in-module

import numpy

FORWARD_DICT = dict(enumerate(numpy.array(list(printable), dtype="U1")))
FORWARD_MAP = numpy.vectorize(FORWARD_DICT.get)
INVERSE_DICT = {value: key for key, value in FORWARD_DICT.items()}
INVERSE_MAP = numpy.vectorize(INVERSE_DICT.get)


def keys_to_exponents(keys):
    """
    >>> keys_to_exponents("0P")
    array([ 0, 51])
    >>> keys_to_exponents(["12", "21", "0P"])
    array([[ 1,  2],
           [ 2,  1],
           [ 0, 51]])
    """
    keys = numpy.asarray(keys, dtype="U")
    if not keys.shape:
        return numpy.array([INVERSE_DICT[key] for key in keys.item()])
    keys = keys.view("U1").reshape(len(keys), -1)
    assert "" not in keys, "all keys have to be the same length"
    exponents = INVERSE_MAP(keys)
    return exponents


def exponents_to_keys(exponents):
    """
    >>> exponents_to_keys([0, 1, 2]) == u"012"
    True
    >>> exponents_to_keys([[0, 0], [0, 1], [9, 44]]) == [u"00", u"01", u"9I"]
    array([ True,  True,  True])
    """
    exponents = numpy.asarray(exponents, dtype=int)
    assert 0 < len(exponents.shape) < 3, "invalid exponent input"
    if len(exponents.shape) == 1:
        return exponents_to_keys(exponents.reshape(1, -1))[0]
    keys = FORWARD_MAP(exponents).flatten()
    keys = numpy.array(keys.view("U%d" % exponents.shape[-1]))
    return keys
