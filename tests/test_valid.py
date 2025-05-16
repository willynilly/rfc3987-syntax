from rfc3987_helpers import *


def test_valid_is_iri():
    assert is_iri("http://github.com")
