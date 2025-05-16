from pathlib import Path
from lark import Lark, exceptions

PARSER_TYPE: str = "earley"
GRAMMAR_PATH: Path = Path(__file__).parent / "rfc3987.lark"
RFC3987_TERMS: list[str] = [
    "iri",
    "scheme",
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


def load_grammar(path: Path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


grammar: str = load_grammar(GRAMMAR_PATH)

general_parser = Lark(grammar, start=["iri"], parser=PARSER_TYPE)


def is_valid(term: str, value: str):
    try:
        general_parser.parse(value, start=term)
        return True
    except exceptions.LarkError:
        return False


def make_validator(rule_name):
    parser = Lark(grammar, start=rule_name, parser=PARSER_TYPE)

    def validator(text):
        try:
            parser.parse(text)
            return True
        except exceptions.LarkError:
            return False

    return validator


is_iri = make_validator("iri")

is_ihier_part = make_validator("ihier_part")

is_iauthority = make_validator("iauthority")

is_iuserinfo = make_validator("iuserinfo")

is_ihost = make_validator("ihost")

is_ireg_name = make_validator("ireg_name")

is_ipath = make_validator("ipath")

is_ipath_abempty = make_validator("ipath_abempty")

is_ipath_absolute = make_validator("ipath_absolute")

is_ipath_noscheme = make_validator("ipath_noscheme")

is_ipath_rootless = make_validator("ipath_rootless")

is_ipath_empty = make_validator("ipath_empty")

is_isegment = make_validator("isegment")

is_isegment_nz = make_validator("isegment_nz")

is_isegment_nz_nc = make_validator("isegment_nz_nc")

is_ipchar = make_validator("ipchar")

is_iquery = make_validator("iquery")

is_ifragment = make_validator("ifragment")

is_iunreserved = make_validator("iunreserved")

is_ucschar = make_validator("ucschar")

is_iprivate = make_validator("iprivate")

is_sub_delims = make_validator("sub_delims")

is_ip_literal = make_validator("ip_literal")

is_ipvfuture = make_validator("ipvfuture")

is_ipv6address = make_validator("ipv6address")

is_h16 = make_validator("h16")

is_ls32 = make_validator("ls32")

is_ipv4address = make_validator("ipv4address")

is_dec_octet = make_validator("dec_octet")

is_unreserved = make_validator("unreserved")

is_alpha = make_validator("alpha")

is_digit = make_validator("digit")

is_hexdig = make_validator("hexdig")

is_port = make_validator("port")
