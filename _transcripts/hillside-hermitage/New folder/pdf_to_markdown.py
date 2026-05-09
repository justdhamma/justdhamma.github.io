#!/usr/bin/env python3
"""
PDF to Markdown Converter
Preserves: headings, bold, italic, hyperlinks, footnotes, lists, tables, code blocks
Requires: pymupdf (pip install pymupdf)
"""

import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Missing dependency. Install with:  pip install pymupdf")
    sys.exit(1)


# ─────────────────────────── helpers ────────────────────────────────────────

def _flag(flags: int, bit: int) -> bool:
    return bool(flags & bit)

def _is_bold(flags: int) -> bool:
    return _flag(flags, 2 ** 4)   # fitz TEXT_FONT_BOLD = 16

def _is_italic(flags: int) -> bool:
    return _flag(flags, 2 ** 1)   # fitz TEXT_FONT_ITALIC = 2

def _is_monospace(flags: int) -> bool:
    return _flag(flags, 2 ** 3)   # fitz TEXT_FONT_MONOSPACE = 8

def _is_superscript(flags: int) -> bool:
    return _flag(flags, 2 ** 0)   # fitz TEXT_FONT_SUPERSCRIPT = 1

def _clean(text: str) -> str:
    """Normalise whitespace and strip trailing spaces per line."""
    text = text.replace("\u00a0", " ")   # non-breaking space → regular space
    text = re.sub(r" {2,}", " ", text)
    return text.strip()

def _escape_md(text: str) -> str:
    """Escape characters that are special in Markdown (outside formatting spans).

    We intentionally escape only the characters that *actively break prose
    rendering* when unescaped:
      \\  – starts an escape sequence
      `   – opens inline code
      *   – bold / italic
      _   – bold / italic
    Characters like -, !, [, ], (, ), #, +, |, <, > are left unescaped because
    they are harmless in mid-sentence prose and escaping them produces ugly
    noise in the output (e.g. "ill\\-will", "birth\\!").
    """
    return re.sub(r'([\\`*_])', r'\\\1', text)


# ─────────────────────────── post-processing ────────────────────────────────

# Pali / Indic diacritic characters that PDFs often encode in a separate font
# span, causing spurious bold/italic markers around them.
_PALI_DIACRITICS = "āīūṅṃñṭḍṇḷĀĪŪṄṂÑṬḌṆḶ"


def _postprocess_markdown(md: str) -> str:
    """
    Clean up common artefacts produced by span-level PDF extraction:

    1. Strip zero-width spaces (U+200B) left over from PDF layout.
    2. Collapse adjacent identical inline markers caused by diacritics being
       in a separate font span:
           **word****ṇ****word**  ->  **wordṇword**
           *word**ṇ**word*        ->  *wordṇword*
    3. Remove any remaining stray **...** wrappers that contain only Pali
       diacritic characters (they were never meant to be bold).
    4. Strip trailing whitespace that crept inside closing markers:
           **Heading **  ->  **Heading**
           *phrase *     ->  *phrase*
    """
    # 1. Zero-width spaces
    md = md.replace("\u200b", "")

    pali_char_class = "[" + re.escape(_PALI_DIACRITICS) + "]+"

    # 2a. Collapse adjacent bold spans: **A****B** -> **AB**
    #     Run repeatedly to handle chains like **A****x****B****y****C**
    for _ in range(8):
        new = re.sub(r'\*\*([^*\n]*?)\*\*\*\*([^*\n]*?)\*\*', r'**\1\2**', md)
        if new == md:
            break
        md = new

    # 2b. Collapse adjacent italic spans: **DIACRITIC** embedded inside *...*
    #     *text**ṇ**text* -> *textṇtext*
    md = re.sub(
        r'(\*(?!\*)(?:[^*\n]*?))' +
        r'\*\*(' + pali_char_class + r')\*\*' +
        r'((?:[^*\n]*?)\*(?!\*))',
        r'\1\2\3',
        md,
    )

    # 3. Remove isolated **DIACRITIC** markers that survived anywhere
    md = re.sub(r'\*\*(' + pali_char_class + r')\*\*', r'\1', md)

    # 4a. Trailing whitespace before closing **: **text ** -> **text**
    md = re.sub(r'\*\*([^*\n]+?)\s+\*\*', r'**\1**', md)

    # 4b. Trailing whitespace before closing * (italic only).
    #
    #     The naive regex (?<!\*)\*([^*\n]+?)\s+\*(?!\*) has a subtle bug: it can
    #     match the closing * of one span as the opening * of a new pseudo-span
    #     (e.g. turning "*anicca*. … *Sabbe …, *" into a false match that
    #     removes the space before *Sabbe but ignores the real trailing space).
    #
    #     Safer approach: target only " *" (literal space + asterisk) where the
    #     asterisk is a CLOSING marker, i.e. followed by end-of-line, whitespace,
    #     or common punctuation — never by a word character that would indicate
    #     it is an opening marker.
    md = re.sub(
        r' \*(?!\*)(?=[\s.,;:!?"\')\]]|$)',
        r'*',
        md,
        flags=re.MULTILINE,
    )

    # 5. Safety: collapse 3+ blank lines to 2
    md = re.sub(r'\n{3,}', '\n\n', md)

    return md


# ─────────────────────────── font-size → heading ────────────────────────────

def _build_heading_map(doc: fitz.Document) -> dict[float, int]:
    """
    Analyse font sizes across the document and map them to heading levels.
    The body text size is treated as the baseline; larger sizes become headings.
    Returns {font_size: heading_level} where heading_level is 1-6 (or 0 = body).
    """
    size_counts: dict[float, int] = defaultdict(int)

    for page in doc:
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
        for block in blocks:
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    size = round(span["size"], 1)
                    size_counts[size] += len(span["text"].strip())

    if not size_counts:
        return {}

    # Body size = the size with the most characters
    body_size = max(size_counts, key=lambda s: size_counts[s])

    # Unique sizes larger than body, sorted descending
    larger = sorted([s for s in size_counts if s > body_size + 0.5], reverse=True)

    heading_map: dict[float, int] = {}
    for level, size in enumerate(larger[:6], start=1):
        heading_map[size] = level

    return heading_map


# ─────────────────────────── hyperlink lookup ───────────────────────────────

def _get_links(page: fitz.Page) -> list[dict]:
    """Return all links on the page with their bounding rects."""
    return page.get_links()   # list of dicts: {kind, from (rect), uri/page/…}


def _find_link_for_rect(links: list[dict], rect: fitz.Rect) -> str | None:
    """Return the URI if the rect overlaps a hyperlink annotation, else None."""
    for lnk in links:
        if lnk.get("kind") == fitz.LINK_URI:
            if fitz.Rect(lnk["from"]).intersects(rect):
                return lnk.get("uri")
    return None


# ─────────────────────────── span → inline md ───────────────────────────────

def _span_to_md(span: dict, uri: str | None) -> str:
    """Convert a single text span to its inline Markdown representation."""
    text = span["text"]
    if not text.strip():
        return text   # preserve whitespace spans as-is

    flags = span.get("flags", 0)
    bold    = _is_bold(flags)
    italic  = _is_italic(flags)
    mono    = _is_monospace(flags)
    sup     = _is_superscript(flags)

    # Escape special MD chars in the raw text before wrapping
    safe = _escape_md(text)

    if mono:
        result = f"`{text}`"   # don't escape inside backticks
    elif sup:
        result = f"<sup>{safe}</sup>"
    else:
        result = safe
        if bold and italic:
            result = f"***{result}***"
        elif bold:
            result = f"**{result}**"
        elif italic:
            result = f"*{result}*"

    if uri:
        result = f"[{result}]({uri})"

    return result


# ─────────────────────────── block → md lines ───────────────────────────────

def _block_to_md(
    block: dict,
    heading_map: dict[float, int],
    links: list[dict],
    footnote_refs: set[str],
) -> list[str]:
    """
    Convert one text block (a paragraph / heading / list item)
    into a list of Markdown lines.
    """
    if block.get("type") != 0:
        return []   # image blocks handled separately

    lines_out: list[str] = []

    for line in block.get("lines", []):
        spans = line.get("spans", [])
        if not spans:
            continue

        # Dominant font size for the line (weighted by char count)
        size_total = sum(len(sp["text"]) * round(sp["size"], 1) for sp in spans)
        char_count = sum(len(sp["text"]) for sp in spans)
        dominant_size = round(size_total / char_count, 1) if char_count else 0

        heading_level = heading_map.get(dominant_size, 0)

        # Build inline content
        inline_parts: list[str] = []
        for span in spans:
            rect  = fitz.Rect(span["bbox"])
            uri   = _find_link_for_rect(links, rect)
            inline_parts.append(_span_to_md(span, uri))

        inline = "".join(inline_parts).strip()
        if not inline:
            continue

        # Detect footnote definitions: a line that starts with a superscript
        # number followed by text (e.g. "¹ See Smith et al.")
        fn_match = re.match(r"^(\d+|[¹²³⁴⁵⁶⁷⁸⁹⁰]+)\s+(.+)", inline)
        if fn_match and dominant_size < 9:   # footnotes are usually small text
            ref_id = fn_match.group(1)
            fn_text = fn_match.group(2)
            footnote_refs.add(ref_id)
            lines_out.append(f"[^{ref_id}]: {fn_text}")
            continue

        if heading_level:
            lines_out.append(f"{'#' * heading_level} {inline}")
        else:
            lines_out.append(inline)

    return lines_out


# ─────────────────────────── table detection ────────────────────────────────

def _table_to_md(page: fitz.Page) -> list[str]:
    """
    Detect and render tables found on the page using PyMuPDF's table finder.
    Returns Markdown table lines.
    """
    md_lines: list[str] = []
    try:
        tabs = page.find_tables()
    except Exception:
        return md_lines

    for tab in tabs.tables:
        try:
            df = tab.to_pandas()
        except Exception:
            continue

        if df.empty:
            continue

        # Header row
        headers = [str(c) for c in df.columns]
        md_lines.append("| " + " | ".join(headers) + " |")
        md_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

        # Data rows
        for _, row in df.iterrows():
            cells = [str(v).replace("\n", " ").strip() for v in row]
            md_lines.append("| " + " | ".join(cells) + " |")

        md_lines.append("")  # blank line after table

    return md_lines


# ─────────────────────────── list detection ─────────────────────────────────

_BULLET_RE    = re.compile(r"^[•·‣⁃◦▪▸➢➤→\-\*]\s+")
_NUMBERED_RE  = re.compile(r"^\d+[.)]\s+")

def _normalise_list_items(lines: list[str]) -> list[str]:
    """Convert detected bullet / numbered lines to proper Markdown list syntax."""
    out: list[str] = []
    for line in lines:
        if _BULLET_RE.match(line):
            content = _BULLET_RE.sub("", line)
            out.append(f"- {content}")
        elif _NUMBERED_RE.match(line):
            # Keep as-is; already valid Markdown ordered list syntax
            out.append(line)
        else:
            out.append(line)
    return out


# ─────────────────────────── main converter ─────────────────────────────────

def pdf_to_markdown(
    pdf_path: str | Path,
    *,
    include_images: bool = False,
    image_dir: str | Path | None = None,
) -> str:
    """
    Convert a PDF file to Markdown.

    Parameters
    ----------
    pdf_path     : path to the input PDF
    include_images : if True, extract embedded raster images and embed them
    image_dir    : directory to save extracted images (defaults to pdf_path parent)

    Returns
    -------
    Markdown string
    """
    pdf_path = Path(pdf_path)
    doc = fitz.open(str(pdf_path))

    heading_map = _build_heading_map(doc)

    if include_images and image_dir is None:
        image_dir = pdf_path.parent / (pdf_path.stem + "_images")

    md_pages: list[str] = []
    footnote_refs: set[str] = set()

    for page_num, page in enumerate(doc, start=1):
        page_lines: list[str] = []

        links = _get_links(page)

        # ── tables first (so we can skip overlapping text blocks) ──────────
        table_md = _table_to_md(page)

        # ── text blocks ────────────────────────────────────────────────────
        raw = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)
        blocks = raw.get("blocks", [])

        prev_was_blank = False
        for block in blocks:
            if block.get("type") == 1 and include_images:
                # Raster image block
                xref = block.get("image")
                if xref and image_dir:
                    img_dir = Path(image_dir)
                    img_dir.mkdir(parents=True, exist_ok=True)
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n - pix.alpha > 3:
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    img_name = f"page{page_num:03d}_img{xref}.png"
                    img_path = img_dir / img_name
                    pix.save(str(img_path))
                    rel_path = img_path.relative_to(pdf_path.parent)
                    page_lines.append(f"\n![Image]({rel_path})\n")
                continue

            block_lines = _block_to_md(block, heading_map, links, footnote_refs)
            if not block_lines:
                if not prev_was_blank:
                    page_lines.append("")
                prev_was_blank = True
                continue

            prev_was_blank = False
            page_lines.extend(_normalise_list_items(block_lines))
            page_lines.append("")   # paragraph separator

        if table_md:
            page_lines.append("")
            page_lines.extend(table_md)

        md_pages.append("\n".join(page_lines))

    doc.close()

    # Join pages with a horizontal rule
    full_md = "\n\n---\n\n".join(p.strip() for p in md_pages if p.strip())

    full_md = _postprocess_markdown(full_md)

    return full_md


# ─────────────────────────── CLI ────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Convert a PDF to Markdown, preserving headings, bold, italic, "
                    "hyperlinks, footnotes, lists, and tables."
    )
    parser.add_argument("input",  help="Path to the input PDF file")
    parser.add_argument(
        "-o", "--output",
        help="Path for the output .md file (default: same name as PDF with .md extension)",
    )
    parser.add_argument(
        "--images",
        action="store_true",
        help="Extract and embed raster images found in the PDF",
    )
    parser.add_argument(
        "--image-dir",
        default=None,
        help="Directory to save extracted images (default: <pdf_stem>_images/)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output) if args.output else input_path.with_suffix(".md")

    print(f"Converting: {input_path}")
    md = pdf_to_markdown(
        input_path,
        include_images=args.images,
        image_dir=args.image_dir,
    )

    output_path.write_text(md, encoding="utf-8")
    print(f"Saved:      {output_path}  ({len(md):,} characters)")


if __name__ == "__main__":
    main()
