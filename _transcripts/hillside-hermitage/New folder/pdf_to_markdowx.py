#!/usr/bin/env python3
"""
PDF to Markdown Converter  (improved)
Preserves: headings, bold, italic, hyperlinks, footnotes, lists, tables, code blocks
Requires: pymupdf  (pip install pymupdf)

Key improvements over v1:
  - Paragraphs within the same block are now joined into a single line (no
    per-PDF-line blank separators inside paragraphs).
  - Bold-only body-size lines are promoted to sub-headings (### / ####).
  - Page-number-only lines (lone integers) are suppressed.
  - Heading markers never contain inner ** / * formatting.
  - Page boundaries emit  ## Page N  +  <page_number>N</page_number>  header.
  - Italic / bold markers are no longer glued to preceding punctuation;
    a space is inserted when needed.
  - Cross-page --- separators are only emitted at page ends, not mid-sentence.
  - All previous Pali-diacritic, adjacent-span, and trailing-space fixes retained.
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
    """Escape only the characters that actively break prose rendering.

    Only escapes: \\  `  *  _
    Leaves alone: - ! [ ] ( ) # + | < >  (harmless in mid-sentence prose)
    """
    return re.sub(r'([\\`*_])', r'\\\1', text)

def _strip_inner_md_markers(text: str) -> str:
    """Remove bold/italic markers from inside a heading or subheading."""
    text = re.sub(r'\*{1,3}(.*?)\*{1,3}', r'\1', text)
    return text.strip()


# ─────────────────────────── post-processing ────────────────────────────────

# Pali / Indic diacritic characters that PDFs often encode in a separate font
# span, causing spurious bold/italic markers around them.
_PALI_DIACRITICS = "āīūṅṃñṭḍṇḷĀĪŪṄṂÑṬḌṆḶ"


def _postprocess_markdown(md: str) -> str:
    """
    Clean up common artefacts produced by span-level PDF extraction.

    Pass 1  – Strip zero-width spaces (U+200B).
    Pass 2a – Collapse adjacent bold spans: **A****B**  ->  **AB**
    Pass 2b – Collapse **DIACRITIC** embedded inside an italic run.
    Pass 3  – Remove any remaining stray **DIACRITIC** wrappers.
    Pass 4a – Strip trailing whitespace before closing **.
    Pass 4b – Strip trailing whitespace before closing * (italic).
    Pass 5  – Fix missing space before inline italic/bold opening marker
              when it is glued to preceding punctuation:
              ask:*"…"* -> ask: *"…"*
    Pass 6  – Remove double-blank lines from heading-adjacent spacing.
    Pass 7  – Collapse 3+ blank lines to 2.
    """
    # 1. Zero-width spaces
    md = md.replace("\u200b", "")

    pali_char_class = "[" + re.escape(_PALI_DIACRITICS) + "]+"

    # 2a. Collapse adjacent bold spans: **A****B** -> **AB**
    for _ in range(8):
        new = re.sub(r'\*\*([^*\n]*?)\*\*\*\*([^*\n]*?)\*\*', r'**\1\2**', md)
        if new == md:
            break
        md = new

    # 2b. Collapse **DIACRITIC** embedded inside *...*
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

    # 4b. Trailing whitespace before closing * (italic only, safe pattern).
    md = re.sub(
        r' \*(?!\*)(?=[\s.,;:!?"\')\]]|$)',
        r'*',
        md,
        flags=re.MULTILINE,
    )

    # 5. Insert space before opening inline marker when glued to punctuation.
    #    e.g.  ask:*"…"*  ->  ask: *"…"*
    #    e.g.  result.*This*  ->  result. *This*
    md = re.sub(
        r'([^\s*(\[])(\*{1,3})(?=[^*\s])',
        lambda m: m.group(1) + (' ' if m.group(1)[-1] in ':.,;!?' else '') + m.group(2),
        md,
    )

    # 6. Tighten heading spacing: remove extra blank line between heading and
    #    the next paragraph (a common PDF artefact).
    md = re.sub(r'(#{1,6} [^\n]+)\n\n\n+', r'\1\n\n', md)

    # 7. Collapse 3+ blank lines to 2
    md = re.sub(r'\n{3,}', '\n\n', md)

    return md


# ─────────────────────────── font-size → heading ────────────────────────────

def _build_heading_map(doc: fitz.Document) -> dict[float, int]:
    """
    Analyse font sizes across the document and map them to heading levels.
    Body text size = most-used size; larger sizes become headings.
    Returns {font_size: heading_level}  (heading_level 1-6; 0 = body).
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

    body_size = max(size_counts, key=lambda s: size_counts[s])
    larger = sorted([s for s in size_counts if s > body_size + 0.5], reverse=True)

    heading_map: dict[float, int] = {}
    for level, size in enumerate(larger[:6], start=1):
        heading_map[size] = level

    return heading_map


# ─────────────────────────── hyperlink lookup ───────────────────────────────

def _get_links(page: fitz.Page) -> list[dict]:
    return page.get_links()

def _find_link_for_rect(links: list[dict], rect: fitz.Rect) -> str | None:
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
    bold   = _is_bold(flags)
    italic = _is_italic(flags)
    mono   = _is_monospace(flags)
    sup    = _is_superscript(flags)

    safe = _escape_md(text)

    if mono:
        result = f"`{text}`"
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


# ─────────────────────────── block analysis helpers ─────────────────────────

def _dominant_size(spans: list[dict]) -> float:
    """Return the character-weighted dominant font size for a list of spans."""
    size_total = sum(len(sp["text"]) * round(sp["size"], 1) for sp in spans)
    char_count = sum(len(sp["text"]) for sp in spans)
    return round(size_total / char_count, 1) if char_count else 0.0


def _all_bold(spans: list[dict]) -> bool:
    """Return True if every non-whitespace span in the list is bold."""
    text_spans = [sp for sp in spans if sp["text"].strip()]
    if not text_spans:
        return False
    return all(_is_bold(sp.get("flags", 0)) for sp in text_spans)


def _is_page_number_line(text: str) -> bool:
    """
    Return True if the line looks like a bare page number (lone integer,
    possibly with surrounding whitespace).  These are page-header artefacts
    in the Hillside Hermitage PDFs and should be suppressed.
    """
    return bool(re.match(r'^\s*\d{1,3}\s*$', text))


# ─────────────────────────── block → md lines ───────────────────────────────

def _block_to_md(
    block: dict,
    heading_map: dict[float, int],
    body_size: float,
    links: list[dict],
    footnote_refs: set[str],
) -> list[str]:
    """
    Convert one text block to a list of Markdown lines.

    Key behaviours:
    • Lines within the same block are joined into a single paragraph string
      (no inter-line blank rows inside a block).
    • Bold-only lines at body size become ### sub-headings.
    • Heading text is stripped of inner ** / * markers.
    • Lone page-number lines are dropped.
    """
    if block.get("type") != 0:
        return []

    lines_out: list[str] = []

    for line in block.get("lines", []):
        spans = line.get("spans", [])
        if not spans:
            continue

        # Collect raw text to check for page-number suppression
        raw_text = "".join(sp["text"] for sp in spans)
        if _is_page_number_line(raw_text):
            continue

        dom_size = _dominant_size(spans)
        heading_level = heading_map.get(dom_size, 0)

        # Build inline content from spans
        inline_parts: list[str] = []
        for span in spans:
            rect = fitz.Rect(span["bbox"])
            uri  = _find_link_for_rect(links, rect)
            inline_parts.append(_span_to_md(span, uri))

        inline = "".join(inline_parts).strip()
        if not inline:
            continue

        # Footnote detection (small font, starts with superscript digit)
        fn_match = re.match(r"^(\d+|[¹²³⁴⁵⁶⁷⁸⁹⁰]+)\s+(.+)", inline)
        if fn_match and dom_size < 9:
            ref_id  = fn_match.group(1)
            fn_text = fn_match.group(2)
            footnote_refs.add(ref_id)
            lines_out.append(f"[^{ref_id}]: {fn_text}")
            continue

        # Named heading (larger font than body)
        if heading_level:
            clean_heading = _strip_inner_md_markers(inline)
            lines_out.append(f"{'#' * heading_level} {clean_heading}")
            continue

        # Bold-only body-size line  →  treat as sub-heading (###)
        # This covers section titles like "The Defilements that Ruin the Practice"
        # that are styled in the same font size as body but in bold.
        if _all_bold(spans):
            clean_heading = _strip_inner_md_markers(inline)
            lines_out.append(f"### {clean_heading}")
            continue

        lines_out.append(inline)

    return lines_out


# ─────────────────────────── paragraph joining ──────────────────────────────

def _join_block_lines(lines: list[str]) -> str:
    """
    Join multiple lines from the same text block into a single paragraph.

    Rules:
    • Lines starting with #, >, -, digits+. are kept separate (they are
      structural elements).
    • Plain prose lines are space-joined into one paragraph.
    """
    if not lines:
        return ""
    if len(lines) == 1:
        return lines[0]

    parts: list[str] = []
    for ln in lines:
        stripped = ln.strip()
        if not stripped:
            continue
        # Structural lines stay separate
        if re.match(r'^(#{1,6} |>|- |\d+[.)]\s|\[\^)', stripped):
            if parts:
                yield " ".join(parts)
                parts = []
            yield stripped
        else:
            parts.append(stripped)

    if parts:
        yield " ".join(parts)


# ─────────────────────────── table detection ────────────────────────────────

def _table_to_md(page: fitz.Page) -> list[str]:
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

        headers = [str(c) for c in df.columns]
        md_lines.append("| " + " | ".join(headers) + " |")
        md_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        for _, row in df.iterrows():
            cells = [str(v).replace("\n", " ").strip() for v in row]
            md_lines.append("| " + " | ".join(cells) + " |")
        md_lines.append("")

    return md_lines


# ─────────────────────────── list detection ─────────────────────────────────

_BULLET_RE   = re.compile(r"^[•·‣⁃◦▪▸➢➤→\-\*]\s+")
_NUMBERED_RE = re.compile(r"^\d+[.)]\s+")

def _normalise_list_items(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        if _BULLET_RE.match(line):
            content = _BULLET_RE.sub("", line)
            out.append(f"- {content}")
        elif _NUMBERED_RE.match(line):
            out.append(line)
        else:
            out.append(line)
    return out


# ─────────────────────────── body size helper ───────────────────────────────

def _get_body_size(doc: fitz.Document) -> float:
    """Return the most-common font size (body text size) across the document."""
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
        return 11.0
    return max(size_counts, key=lambda s: size_counts[s])


# ─────────────────────────── main converter ─────────────────────────────────

def pdf_to_markdown(
    pdf_path: str | Path,
    *,
    include_images: bool = False,
    image_dir: str | Path | None = None,
    page_headers: bool = True,
) -> str:
    """
    Convert a PDF file to Markdown.

    Parameters
    ----------
    pdf_path       : path to the input PDF
    include_images : if True, extract embedded raster images and embed them
    image_dir      : directory to save extracted images
    page_headers   : if True, emit  ## Page N  at the start of every page

    Returns
    -------
    Markdown string
    """
    pdf_path = Path(pdf_path)
    doc = fitz.open(str(pdf_path))

    heading_map = _build_heading_map(doc)
    body_size   = _get_body_size(doc)

    if include_images and image_dir is None:
        image_dir = pdf_path.parent / (pdf_path.stem + "_images")

    md_pages: list[str] = []
    footnote_refs: set[str] = set()

    for page_num, page in enumerate(doc, start=1):
        page_parts: list[str] = []

        # Page header
        if page_headers:
            page_parts.append(f"## Page {page_num}\n")
            page_parts.append(f"<page_number>{page_num}</page_number>\n")

        links      = _get_links(page)
        table_md   = _table_to_md(page)

        raw    = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)
        blocks = raw.get("blocks", [])

        for block in blocks:
            # ── image block ──────────────────────────────────────────────
            if block.get("type") == 1:
                if include_images and image_dir:
                    xref = block.get("image")
                    if xref:
                        img_dir = Path(image_dir)
                        img_dir.mkdir(parents=True, exist_ok=True)
                        pix = fitz.Pixmap(doc, xref)
                        if pix.n - pix.alpha > 3:
                            pix = fitz.Pixmap(fitz.csRGB, pix)
                        img_name = f"page{page_num:03d}_img{xref}.png"
                        img_path = img_dir / img_name
                        pix.save(str(img_path))
                        rel_path = img_path.relative_to(pdf_path.parent)
                        page_parts.append(f"\n![Image]({rel_path})\n")
                continue

            # ── text block ───────────────────────────────────────────────
            raw_lines = _block_to_md(block, heading_map, body_size, links, footnote_refs)
            if not raw_lines:
                continue

            raw_lines = _normalise_list_items(raw_lines)

            # Join prose lines within the block into single paragraph(s)
            joined = list(_join_block_lines(raw_lines))

            for paragraph in joined:
                if paragraph.strip():
                    page_parts.append(paragraph)

        if table_md:
            page_parts.extend(table_md)

        md_pages.append("\n\n".join(p for p in page_parts if p is not None))

    doc.close()

    # Join pages: each page ends with --- (page break rule)
    full_md = "\n\n---\n\n".join(p.strip() for p in md_pages if p.strip())

    full_md = _postprocess_markdown(full_md)

    return full_md


# ─────────────────────────── CLI ────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Convert a PDF to Markdown, preserving headings, bold, italic, "
            "hyperlinks, footnotes, lists, and tables."
        )
    )
    parser.add_argument("input", help="Path to the input PDF file")
    parser.add_argument(
        "-o", "--output",
        help="Path for the output .md file (default: same name as PDF with .md)",
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
    parser.add_argument(
        "--no-page-headers",
        action="store_true",
        help="Omit the  ## Page N  header emitted at the start of each page",
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
        page_headers=not args.no_page_headers,
    )

    output_path.write_text(md, encoding="utf-8")
    print(f"Saved:      {output_path}  ({len(md):,} characters)")


if __name__ == "__main__":
    main()
