---
description: How to add a new book with English chapters and Nepali translation placeholders
---

# Add a New Book with Chapters

Use this workflow when adding a new book that has multiple chapters (e.g., sermons, essays) to the Jekyll site.

## Prerequisites

You need to know:
- `book_author_key` — the author's key in `_data/book_order.yml` (e.g., `bhikkhu-k-nanananda`, `ajahn-nanamoli`)
- `book_key` — the book's slug (e.g., `nibbana-the-mind-stilled`, `the-law-of-dependent-origination`)
- `book_title` — display title (e.g., `Nibbana - The Mind Stilled`)
- `chapter_prefix` — filename prefix (e.g., `sermon`, `chapter`, `essay`)
- `chapter_count` — number of chapters (e.g., `10`, `33`)
- `doc_url` — external source document URL (PDF/HTML)
- `en_title_template` — English title pattern (e.g., `Nibbana Sermon {n}`, `Sermon {n}`)
- `ne_title_template` — Nepali title pattern with Devanagari numeral (e.g., `निर्वाण उपदेश {ne_num}`, `पटिच्चसमुप्पाद उपदेश {ne_num}`)
- Author folder name under `_books/` (usually same as `book_author_key`)

Base directory for the book:
```
_books/{author_folder}/{book_key}/
```

## Step 1: Create English Chapter Files

For each chapter `n` from `1` to `chapter_count`, create:
```
{chapter_prefix}-{n}-en.md
```

**Front matter template:**
```yaml
---
lang: en
layout: post
category: books
book_author: {book_author_key}
book_key: {book_key}
title: {en_title}
permalink: /books/{book_author_key}/{book_key}/{chapter_prefix}-{n}-en/
gem_url: /books/{book_author_key}/{book_key}/{chapter_prefix}-{n}-ne-gem/
gpt_url: /books/{book_author_key}/{book_key}/{chapter_prefix}-{n}-ne-gpt/
cld_url: /books/{book_author_key}/{book_key}/{chapter_prefix}-{n}-ne-cld/
doc_url: "{doc_url}"
alt_doc_url: 
---
```

**Rules:**
- Replace `{n}` with the chapter number.
- `title` should use `{en_title_template}` (e.g., `Nibbana Sermon 1`, `Sermon 1`).
- `permalink` must end with `/{chapter_prefix}-{n}-en/`.
- `gem_url`, `gpt_url`, `cld_url` must end with `/{chapter_prefix}-{n}-ne-{suffix}/` (note the `ne-` prefix, **not** `en-`).
- All URLs must be **unique** per file to avoid Jekyll conflicts.

## Step 2: Create Nepali Translation Placeholders

For each chapter `n` from `1` to `chapter_count`, create **3 files**:
```
{chapter_prefix}-{n}-ne-gem.md
{chapter_prefix}-{n}-ne-gpt.md
{chapter_prefix}-{n}-ne-cld.md
```

**Front matter template:**
```yaml
---
lang: ne
layout: post
category: books
book_author: {book_author_key}
book_key: {book_key}
en_title: {en_title}
ne_title: {ne_title}
en_url: "/books/{book_author_key}/{book_key}/{chapter_prefix}-{n}-en/"
permalink: /books/{book_author_key}/{book_key}/{chapter_prefix}-{n}-ne-{suffix}/
gem_url: "/books/{book_author_key}/{book_key}/{chapter_prefix}-{n}-ne-gem/"
gpt_url: "/books/{book_author_key}/{book_key}/{chapter_prefix}-{n}-ne-gpt/"
cld_url: "/books/{book_author_key}/{book_key}/{chapter_prefix}-{n}-ne-cld/"
description: a book
type: translation
translator: {suffix}
# date: 2010-08-01
proofread: unfinished
---
```

**Rules:**
- `lang: ne` (Nepali).
- `en_title` matches the English chapter's `title`.
- `ne_title` uses `{ne_title_template}` with Devanagari numerals.
- `permalink` must be **unique** and match the file's suffix:
  - `-ne-gem.md` → permalink ends with `-ne-gem/`
  - `-ne-gpt.md` → permalink ends with `-ne-gpt/`
  - `-ne-cld.md` → permalink ends with `-ne-cld/`
- `translator` field matches suffix: `gem`, `gpt`, or `cld`.
- `gem_url`, `gpt_url`, `cld_url` are **quoted** strings pointing to all three translation permalinks.
- All three Nepali files + the English file must have **distinct permalinks**.

## Step 3: Update `_data/book_order.yml`

Add the book to the correct author's `books` list:

```yaml
authors:
  {book_author_key}:
    folder: {author_folder}
    books:
      - key: {book_key}
        title: {book_title}
        chapters:
          - {chapter_prefix}-1-en
          - {chapter_prefix}-2-en
          - {chapter_prefix}-3-en
          # ... continue for all chapters
```

**Rules:**
- `chapters` list uses **English filenames without `.md`** (e.g., `sermon-1-en`, `chapter-5-en`).
- The `book-toc.html` layout normalizes filenames to match chapters across languages.
- Order in `chapters` list determines TOC display order.

## Step 4: Verify No Conflicts

Before building, check:
1. No two files share the same `permalink`.
2. All `gem_url`/`gpt_url`/`cld_url` values in English files point to existing Nepali file permalinks.
3. All Nepali files have unique permalinks matching their filename suffix.
4. `book_author` and `book_key` match values in `_data/book_order.yml`.

## Devanagari Numerals Reference

```
0: ०, 1: १, 2: २, 3: ३, 4: ४,
5: ५, 6: ६, 7: ७, 8: ८, 9: ९
```

Examples: `१` = 1, `१०` = 10, `३३` = 33

## File Naming Convention

| Language | Filename Pattern | Example |
|----------|-----------------|---------|
| English | `{prefix}-{n}-en.md` | `sermon-1-en.md` |
| Nepali (Gemini) | `{prefix}-{n}-ne-gem.md` | `sermon-1-ne-gem.md` |
| Nepali (GPT) | `{prefix}-{n}-ne-gpt.md` | `sermon-1-ne-gpt.md` |
| Nepali (Claude) | `{prefix}-{n}-ne-cld.md` | `sermon-1-ne-cld.md` |

**Never** use `en-{prefix}-{n}.md` naming — always put the language suffix **last**.

## TOC Translation Links

The `book-toc.html` layout uses `translation-links.html` to show:
- **Gemini** · **GPT** · **Claude** links next to each chapter title
- Links are discovered via:
  1. Explicit `gem_url`/`gpt_url`/`cld_url` in the English file
  2. Auto-discovery by normalized filename matching sibling translations

For links to appear, the English chapter file **must** include `gem_url`, `gpt_url`, and `cld_url`.
