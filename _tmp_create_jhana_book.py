import os

# Configuration
AUTHOR_KEY = "ajahn-nanamoli"
BOOK_KEY = "the-only-way-to-jhana"
BOOK_TITLE = "The Only Way to Jhana"

# Resolve base directory relative to this script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(SCRIPT_DIR, "_books", AUTHOR_KEY, BOOK_KEY)

# Ensure directory exists
os.makedirs(BASE_DIR, exist_ok=True)

chapters = [
    (1, "Jhāna is a lifestyle"),
    (2, "Lay life does not justify sensuality"),
    (3, "No one wants sensuality"),
    (4, "Desire to end desire"),
    (5, "The simile of the wet sticks"),
    (6, "Discerning the body"),
    (7, "Sensuality versus agreeability"),
    (8, "The pleasure of boredom"),
    (9, "Calming the pain, not avoiding it"),
    (10, "Recollection of breathing and subduing of aversion"),
    (11, "Escape from the body"),
    (12, "Jhāna is virtue"),
]

devanagari = {
    "0": "०", "1": "१", "2": "२", "3": "३", "4": "४",
    "5": "५", "6": "६", "7": "७", "8": "८", "9": "९",
}

def to_devanagari(n):
    return "".join(devanagari[d] for d in str(n))

def slugify(title):
    s = title.lower()
    # Remove diacritics for slug
    replacements = {
        "ā": "a", "ī": "i", "ū": "u", "ṅ": "ng", "ñ": "ny",
        "ṭ": "t", "ḍ": "d", "ṇ": "n", "ṃ": "m", "ḷ": "l",
        "ś": "sh", "ṣ": "sh", "ḥ": "h",
    }
    for k, v in replacements.items():
        s = s.replace(k, v)
    s = s.replace("—", "-")
    s = "".join(c if c.isalnum() or c == " " else " " for c in s)
    s = "-".join(s.split())
    return s

for num, title in chapters:
    slug = slugify(title)
    # Add chapter number prefix to slug
    file_slug = f"{num}-{slug}"
    ne_num = to_devanagari(num)

    permalink_base = f"/books/{AUTHOR_KEY}/{BOOK_KEY}/{file_slug}"

    # English file
    en_path = os.path.join(BASE_DIR, f"{file_slug}-en.md")
    en_fm = f"""---
lang: en
layout: post
category: books
book_author: {AUTHOR_KEY}
book_key: {BOOK_KEY}
title: {title}
permalink: {permalink_base}-en/
gem_url: {permalink_base}-ne-gem/
gpt_url: {permalink_base}-ne-gpt/
cld_url: {permalink_base}-ne-cld/
doc_url: ""
alt_doc_url: 
---
"""
    with open(en_path, "w", encoding="utf-8") as f:
        f.write(en_fm)

    # Nepali placeholders
    for suffix in ["gem", "gpt", "cld"]:
        ne_path = os.path.join(BASE_DIR, f"{file_slug}-ne-{suffix}.md")
        ne_fm = f"""---
lang: ne
layout: post
category: books
book_author: {AUTHOR_KEY}
book_key: {BOOK_KEY}
en_title: {title}
ne_title: {title}
en_url: "{permalink_base}-en/"
permalink: {permalink_base}-ne-{suffix}/
gem_url: "{permalink_base}-ne-gem/"
gpt_url: "{permalink_base}-ne-gpt/"
cld_url: "{permalink_base}-ne-cld/"
description: a book
type: translation
translator: {suffix}
# date: 2026-01-01
proofread: unfinished
---
"""
        with open(ne_path, "w", encoding="utf-8") as f:
            f.write(ne_fm)

    print(f"Created chapter {num}: {file_slug}")

print("All files created successfully.")
