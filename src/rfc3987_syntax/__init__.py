from . import syntax_helpers as _syntax_helpers

from .syntax_helpers import *


def __dir__():
    result = _syntax_helpers.__all__.copy()
    for start_rule in ALL_START_RULES:
        result.append(SYNTAX_VALIDATOR_PREFIX + start_rule)
    return result


# Cache for lazily created validators
_attr_cache = {}


def __getattr__(name):
    """
    Lazily create attributes, in particular syntax validators, when accessed.

    When an attribute like 'is_valid_syntax_iri' is accessed, this function
    will create and cache the corresponding validator function.

    We also create the syntax parser lazily.
    """
    try:
        return _attr_cache[name]
    except KeyError:
        if name == "syntax_parser":
            parser = _syntax_helpers.syntax_parser
            _attr_cache[name] = parser
            return parser
        if validator := get_syntax_validator(name):
            _attr_cache[name] = validator
            return validator

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
