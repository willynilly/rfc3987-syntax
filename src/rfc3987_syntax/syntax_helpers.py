__all__ = [
    "is_valid_syntax",
]
import functools
from typing import Any
from lark import Lark, ParseTree, exceptions

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


@functools.lru_cache(maxsize=None)
def get_grammar():
    return load_grammar(RFC3987_SYNTAX_GRAMMAR_PATH)


@functools.lru_cache(maxsize=None)
def get_syntax_parser():
    syntax_parser = Lark(
        get_grammar(),
        start=["iri", "iri_reference", "absolute_iri"],
        parser=RFC3987_SYNTAX_PARSER_TYPE,
    )
    return syntax_parser


def parse(term: str, value: str) -> ParseTree:
    return get_syntax_parser().parse(value, start=term)


def is_valid_syntax(term: str, value: str):
    try:
        parse(term=term, value=value)
        return True
    except exceptions.LarkError:
        return False


@functools.lru_cache(maxsize=None)
def make_syntax_validator(rule_name):
    parser = Lark(get_grammar(), start=rule_name, parser=RFC3987_SYNTAX_PARSER_TYPE)

    def syntax_validator(text):
        try:
            parser.parse(text)
            return True
        except exceptions.LarkError:
            return False

    return syntax_validator


def __getattr__(name: str) -> Any:
    if name == "grammar":
        return get_grammar()
    if name == "syntax_parser":
        return get_syntax_parser()
    if name.startswith("is_valid_syntax_"):
        term = name.removeprefix("is_valid_syntax_")
        return make_syntax_validator(term)
    msg = f"Attribute {name} not found"
    raise AttributeError(msg, name=name)
