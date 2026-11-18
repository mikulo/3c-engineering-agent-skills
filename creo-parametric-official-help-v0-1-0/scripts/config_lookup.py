#!/usr/bin/env python3
"""Search or rebuild the bundled Creo 12 config.pro PDF text index."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PDF = SKILL_ROOT / "references" / "creo-12.4.5.0-config-options.pdf"
DEFAULT_INDEX = SKILL_ROOT / "references" / "creo-12.4.5.0-config-options.txt"
PAGE_RE = re.compile(r"^===== PDF PAGE (\d+) =====$", re.MULTILINE)


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def rebuild_index(pdf_path: Path, index_path: Path) -> int:
    try:
        from pypdf import PdfReader
    except ImportError:
        print("Cannot rebuild: install pypdf first.", file=sys.stderr)
        return 2

    if not pdf_path.is_file():
        print(f"PDF not found: {pdf_path}", file=sys.stderr)
        return 2

    reader = PdfReader(str(pdf_path))
    chunks: list[str] = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        chunks.append(f"===== PDF PAGE {page_number} =====\n{text.rstrip()}\n")
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text("\n".join(chunks), encoding="utf-8", newline="\n")
    print(f"Indexed {len(reader.pages)} pages to {index_path}")
    return 0


def split_pages(index_text: str) -> list[tuple[int, list[str]]]:
    matches = list(PAGE_RE.finditer(index_text))
    pages: list[tuple[int, list[str]]] = []
    for position, match in enumerate(matches):
        start = match.end()
        end = matches[position + 1].start() if position + 1 < len(matches) else len(index_text)
        page_number = int(match.group(1))
        pages.append((page_number, index_text[start:end].strip("\n").splitlines()))
    return pages


def normalized_terms(raw_query: list[str]) -> list[str]:
    terms: list[str] = []
    for value in raw_query:
        terms.extend(part for part in value.split() if part)
    return [term.casefold() for term in terms]


def page_matches(page_text: str, terms: list[str], mode: str) -> bool:
    folded = page_text.casefold()
    if mode == "phrase":
        return " ".join(terms) in folded
    if mode == "all":
        return all(term in folded for term in terms)
    return any(term in folded for term in terms)


def matching_line_numbers(lines: list[str], terms: list[str], mode: str, span: int) -> list[int]:
    if mode == "phrase":
        phrase = " ".join(terms)
        return [i for i, line in enumerate(lines) if phrase in line.casefold()]
    if mode == "all":
        exact = [i for i, line in enumerate(lines) if all(t in line.casefold() for t in terms)]
        if exact:
            return exact
        nearby: list[int] = []
        for start in range(len(lines)):
            end = min(len(lines), start + span)
            block = "\n".join(lines[start:end]).casefold()
            if all(term in block for term in terms):
                nearby.append((start + end - 1) // 2)
        return nearby
    return [i for i, line in enumerate(lines) if any(t in line.casefold() for t in terms)]


def merge_ranges(points: list[int], context: int, line_count: int) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    for point in points:
        start = max(0, point - context)
        end = min(line_count, point + context + 1)
        if ranges and start <= ranges[-1][1]:
            ranges[-1] = (ranges[-1][0], max(ranges[-1][1], end))
        else:
            ranges.append((start, end))
    return ranges


def search_index(
    index_path: Path,
    query: list[str],
    mode: str,
    context: int,
    limit: int,
    span: int,
) -> int:
    if not index_path.is_file():
        print(f"Index not found: {index_path}", file=sys.stderr)
        return 2
    terms = normalized_terms(query)
    if not terms:
        print("Provide at least one non-empty search term.", file=sys.stderr)
        return 2

    pages = split_pages(index_path.read_text(encoding="utf-8"))
    emitted = 0
    for page_number, lines in pages:
        page_text = "\n".join(lines)
        if not page_matches(page_text, terms, mode):
            continue
        points = matching_line_numbers(lines, terms, mode, span)
        if not points:
            continue
        for start, end in merge_ranges(points, context, len(lines)):
            print(f"===== MATCH: PDF PAGE {page_number}, LINES {start + 1}-{end} =====")
            for line_number in range(start, end):
                print(f"{line_number + 1:04d}: {lines[line_number]}")
            print()
            emitted += 1
            if emitted >= limit:
                print(f"Result limit reached ({limit}). Refine the query if needed.")
                return 0

    if emitted == 0:
        print("No matching text found in the bundled index.", file=sys.stderr)
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="*", help="Search terms or a quoted phrase")
    parser.add_argument("--mode", choices=("all", "any", "phrase"), default="all")
    parser.add_argument("--context", type=int, default=6, help="Context lines around each match")
    parser.add_argument("--limit", type=int, default=20, help="Maximum result blocks")
    parser.add_argument("--span", type=int, default=3, help="Maximum adjacent lines for --mode all")
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--rebuild", action="store_true", help="Rebuild the text index from the PDF first")
    return parser


def main() -> int:
    configure_stdout()
    args = build_parser().parse_args()
    if args.context < 0 or args.limit < 1 or args.span < 1:
        print("--context must be >= 0; --limit and --span must be >= 1.", file=sys.stderr)
        return 2
    if args.rebuild:
        status = rebuild_index(args.pdf.resolve(), args.index.resolve())
        if status or not args.query:
            return status
    return search_index(args.index.resolve(), args.query, args.mode, args.context, args.limit, args.span)


if __name__ == "__main__":
    raise SystemExit(main())
