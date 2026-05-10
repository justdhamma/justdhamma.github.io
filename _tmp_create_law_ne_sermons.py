import os

dir_path = r"c:\Users\NAN\Desktop\Just Dhamma\justdhamma.github.io\_books\bhikkhu-k-nanananda\the-law-of-dependent-origination"

ne_digits = {
    '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
    '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'
}

def to_devanagari(n):
    return ''.join(ne_digits[ch] for ch in str(n))

translators = {
    'gem': {'gem_url': 'gem', 'gpt_url': 'gpt', 'cld_url': 'cld'},
    'gpt': {'gem_url': 'gem', 'gpt_url': 'gpt', 'cld_url': 'cld'},
    'cld': {'gem_url': 'gem', 'gpt_url': 'gpt', 'cld_url': 'cld'},
}

for n in range(1, 21):
    ne_num = to_devanagari(n)
    for suffix, t_name in [('gem', 'gem'), ('gpt', 'gpt'), ('cld', 'cld')]:
        filename = f"sermon-{n}-ne-{suffix}.md"
        filepath = os.path.join(dir_path, filename)

        # Build cross-reference URLs
        gem_url = f"/books/bhikkhu-k-nanananda/the-law-of-dependent-origination/sermon-{n}-ne-gem/"
        gpt_url = f"/books/bhikkhu-k-nanananda/the-law-of-dependent-origination/sermon-{n}-ne-gpt/"
        cld_url = f"/books/bhikkhu-k-nanananda/the-law-of-dependent-origination/sermon-{n}-ne-cld/"

        content = f"""---
lang: ne
layout: post
category: books
book_author: bhikkhu-k-nanananda
book_key: the-law-of-dependent-origination
en_title: Sermon {n}
ne_title: पटिच्चसमुप्पाद उपदेश {ne_num}
en_url: "/books/bhikkhu-k-nanananda/the-law-of-dependent-origination/sermon-{n}-en/"
permalink: /books/bhikkhu-k-nanananda/the-law-of-dependent-origination/sermon-{n}-ne-{suffix}/
gem_url: "{gem_url}"
gpt_url: "{gpt_url}"
cld_url: "{cld_url}"
description: a book
type: translation
translator: {t_name}
# date: 2010-08-01
proofread: unfinished
---
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created {filename}")

print("Done")
