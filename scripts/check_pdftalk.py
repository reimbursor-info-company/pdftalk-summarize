#!/usr/bin/env python
"""Verify that a compatible 'pdftalk' install is present.

Run manually or in CI before relying on PDF/audio features (summarize_pdf,
the --audio CLI flag): those require pdftalk even though it is only an
optional dependency of pdftalk-summarize.
"""

import sys

MIN_VERSION = (0, 2, 7)


def _parse_version(version: str) -> tuple[int, ...]:
    parts = []
    for chunk in version.split(".")[:3]:
        digits = ""
        for ch in chunk:
            if ch.isdigit():
                digits += ch
            else:
                break
        parts.append(int(digits) if digits else 0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)


def main() -> None:
    try:
        from importlib.metadata import PackageNotFoundError, version
    except ImportError:
        from importlib_metadata import PackageNotFoundError, version  # type: ignore

    try:
        installed = version("pdftalk")
    except PackageNotFoundError:
        print(
            "ERROR: The 'pdftalk' package is not installed.\n"
            "Install it with: pip install pdftalk-summarize[pdf]",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        import pdftalk.converter  # noqa: F401
        import pdftalk.extractor  # noqa: F401
    except ImportError as exc:
        print(f"ERROR: 'pdftalk' is installed but could not be imported: {exc}", file=sys.stderr)
        sys.exit(1)

    if _parse_version(installed) < MIN_VERSION:
        print(
            f"ERROR: pdftalk {installed} is installed, but "
            f"{'.'.join(map(str, MIN_VERSION))}+ is required.\n"
            "Upgrade it with: pip install --upgrade pdftalk",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"OK: pdftalk {installed} found and compatible.")


if __name__ == "__main__":
    main()
