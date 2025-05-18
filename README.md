# rfc3987-syntax

Helper functions to parse and validate the **syntax** of terms defined in **[RFC 3987](https://www.rfc-editor.org/info/rfc3987)** — the IETF standard for Internationalized Resource Identifiers (IRIs).


## 🎯 Purpose

The goal of `rfc3987-syntax` is to provide a **lightweight, permissively licensed Python module** for validating that strings conform to the **ABNF grammar defined in RFC 3987**. These helpers are:

- ✅ Strictly aligned with the **syntax rules of RFC 3987**
- ✅ Built using a **permissive MIT license**
- ✅ Designed for both **open source and proprietary use**
- ✅ Powered by [Lark](https://github.com/lark-parser/lark), a fast, EBNF-based parser

> 🧠 **Note:** This project focuses on **syntax validation only**. RFC 3987 specifies **additional semantic rules** (e.g., Unicode normalization, BiDi constraints, percent-encoding requirements) that must be enforced separately.


## 📄 License, Attribution, and Citation

**`rfc3987-syntax`** is licensed under the [MIT License](LICENSE), which allows reuse in both open source and commercial software.

This project:

- ❌ Does **not** depend on the `rfc3987` Python package (GPL-licensed)
- ✅ Uses [`lark`](https://github.com/lark-parser/lark), licensed under MIT
- ✅ Implements grammar from **[RFC 3987](https://datatracker.ietf.org/doc/html/rfc3987)**, using **[RFC 3986](https://datatracker.ietf.org/doc/html/rfc3986)** where RFC 3987 delegates syntax

> ⚠️ This project is **not affiliated with or endorsed by** the authors of RFC 3987 or the `rfc3987` Python package.

Please cite this software in accordance with the enclosed CITATION.cff file.


## ⚠️ Limitations

The grammar and parser enforce **only the ABNF syntax** defined in RFC 3987. The following are **not validated** and must be handled separately for full compliance:

- ✅ Unicode **Normalization Form C (NFC)**
- ✅ Bidirectional text (**BiDi**) constraints (RFC 3987 §4.1)
- ✅ **Port number ranges** (must be 0–65535)
- ✅ Valid **IPv6 compression** (only one `::`, max segments)
- ✅ Context-aware **percent-encoding** requirements

ChatGPT 40 was used by the author during the development process. Errors may exist due to this assistance. The author is not an expert in formal grammars or the RFC 3987 or RFC 3986. The grammar, code, and documentation need additional review and testing by experts.


## 📦 Installation

```bash
pip install rfc3987-syntax
```

## 🛠 Usage

### List all supported "terms" (i.e., non-terminals and terminals within ABNF production rules) used to validate the syntax of an IRI according to RFC 3987

```python
from rfc3987_syntax import RFC3987_SYNTAX_TERMS

print("Supported terms:")
for term in RFC3987_SYNTAX_TERMS:
    print(term)
```

### Syntactically validate a string using the general-purpose validator

```python
from rfc3987_syntax import is_valid_syntax

if is_valid_syntax(term='iri', value='http://github.com'):
    print("✓ Valid IRI syntax")

if not is_valid_syntax(term='iri', value='bob'):
    print("✗ Invalid IRI syntax")
```

### Alternatively, use term-specific helpers to validate RFC 3987 syntax.

```python
from rfc3987_syntax import is_valid_syntax_iri

if is_valid_syntax_iri('http://github.com'):
    print("✓ Valid IRI syntax")

if not is_valid_syntax_iri('bob'):
    print("✗ Invalid IRI syntax")
```

### Get the Lark parse tree for a syntax validation (useful for additional semantic validation)

```python
from rfc3987_syntax import parse

ptree: ParseTree = parse(term="iri", value="http://github.com")

print(ptree)
```

## 📚 Sources

This grammar was derived from:

- **[RFC 3987 – Internationalized Resource Identifiers (IRIs)]**  
  → Defines IRI syntax and extensions to URI (e.g. Unicode characters, `ucschar`)  
  → https://datatracker.ietf.org/doc/html/rfc3987

- **[RFC 3986 – Uniform Resource Identifier (URI): Generic Syntax)]**  
  → Provides reusable components like `scheme`, `authority`, `ipv4address`, etc.  
  → https://datatracker.ietf.org/doc/html/rfc3986

> 📝 When `RFC 3986` is listed as the source, it is **used in accordance with RFC 3987**, which explicitly references it for foundational elements.

### Rule-to-Source Mapping

| Rule/Component       | Source     | Notes |
|----------------------|------------|-------|
| `iri`                | RFC 3987   | Top-level IRI rule |
| `scheme`             | RFC 3986   | Referenced by RFC 3987 §2.2 |
| `ihier_part`         | RFC 3987   | IRI-specific hierarchy |
| `iauthority`         | RFC 3986   | Standard URI authority |
| `ipath_abempty`      | RFC 3986   | Path format variant |
| `ipath_absolute`     | RFC 3986   | Absolute path |
| `ipath_noscheme`     | RFC 3986   | Path disallowing scheme prefix |
| `ipath_rootless`     | RFC 3986   | Used in non-scheme contexts |
| `iquery`             | RFC 3987   | Query extension to URI |
| `ifragment`          | RFC 3987   | Fragment extension to URI |
| `ipchar`, `isegment` | RFC 3986   | Path characters and segments |
| `isegment_nz_nc`     | RFC 3987   | IRI-specific path constraint |
| `iunreserved`        | RFC 3987   | Includes `ucschar` |
| `ucschar`, `iprivate`| RFC 3987   | Unicode support |
| `sub_delims`         | RFC 3986   | Reserved characters |
| `ip_literal`         | RFC 3986   | IPv6 or IPvFuture in `[]` |
| `ipv6address`        | RFC 3986   | Expanded forms only |
| `ipvfuture`          | RFC 3986   | Forward-compatible |
| `ipv4address`        | RFC 3986   | Dotted-decimal IPv4 |
| `ls32`               | RFC 3986   | Final 32 bits of IPv6 |
| `h16`, `dec_octet`   | RFC 3986   | Hex and decimal chunks |
| `port`               | RFC 3986   | Optional numeric |
| `pct_encoded`        | RFC 3986   | Percent encoding (e.g. `%20`) |
| `alpha`, `digit`, `hexdig` | RFC 3986 | Character classes |
