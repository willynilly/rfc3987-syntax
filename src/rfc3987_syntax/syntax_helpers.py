import sys

from functools import partial
from pathlib import Path

from rfc3987_syntax.utils import load_grammar

RFC3987_SYNTAX_PARSER_TYPE: str = "earley"
RFC3987_SYNTAX_GRAMMAR_PATH: Path = Path(__file__).parent / "syntax_rfc3987.lark"
RFC3987_SYNTAX_TERMS: list[str] = [
    "iri",
    "iri_reference",
    "absolute_iri",
    "scheme",
    "irelative_ref",
    "irelative_part",
    "ihier_part",
    "iauthority",
    "iuserinfo",
    "ihost",
    "ireg_name",
    "ipath_abempty",
    "isegment",
    "isegment_nz",
    "isegment_nz_nc",
    "ipchar",
    "iquery",
    "ifragment",
    "iunreserved",
    "ucschar",
    "iprivate",
    "sub_delims",
    "ip_literal",
    "ipvfuture",
    "ipv6address",
    "h16",
    "ls32",
    "ipv4address",
    "dec_octet",
    "digit",
    "non_zero",
    "unreserved",
    "alpha",
    "hexdig",
    "port",
    "pct_encoded",
]

# All start rules needed by validators
ALL_START_RULES: list[str] = RFC3987_SYNTAX_TERMS.copy()
for term in ("non_zero", "pct_encoded", "scheme"):
    ALL_START_RULES.remove(term)
ALL_START_RULES.extend(
    ["ipath", "ipath_absolute", "ipath_empty", "ipath_noscheme", "ipath_rootless"]
)

grammar: str = load_grammar(RFC3987_SYNTAX_GRAMMAR_PATH)

__all__ = [
    "RFC3987_SYNTAX_PARSER_TYPE",
    "RFC3987_SYNTAX_GRAMMAR_PATH",
    "RFC3987_SYNTAX_TERMS",
    "ALL_START_RULES",
    "SYNTAX_VALIDATOR_PREFIX",
    "grammar",
    "parse",
    "is_valid_syntax",
    "make_syntax_validator",
    "get_syntax_validator",
]


def parse(term: str, value: str) -> sys.modules[__name__].lark.ParseTree:
    return sys.modules[__name__].syntax_parser.parse(value, start=term)


def is_valid_syntax(term: str, value: str):
    try:
        parse(term=term, value=value)
        return True
    except sys.modules[__name__].lark.exceptions.LarkError:
        return False


def make_syntax_validator(rule_name):
    """Create a validator using the shared parser."""
    return partial(is_valid_syntax, term=rule_name)


# Cache for lazily created validators
_attr_cache = {}


SYNTAX_VALIDATOR_PREFIX = "is_valid_syntax_"


def get_syntax_parser():
    # Single shared parser with all start rules
    return sys.modules[__name__].lark.Lark(
        grammar,
        start=ALL_START_RULES,
        parser=RFC3987_SYNTAX_PARSER_TYPE,
    )


def get_syntax_validator(attr_name: str):
    if not attr_name.startswith(SYNTAX_VALIDATOR_PREFIX):
        return None

    term_name = attr_name[len(SYNTAX_VALIDATOR_PREFIX) :]

    if term_name not in ALL_START_RULES:
        return None

    return make_syntax_validator(term_name)


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
        if name == "lark":
            import lark

            _attr_cache[name] = lark
            return lark
        if name == "syntax_parser":
            syntax_parser = get_syntax_parser()
            _attr_cache[name] = syntax_parser
            return syntax_parser
        if validator := get_syntax_validator(name):
            _attr_cache[name] = validator
            return validator

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
