import os
import re

dir_path = r"c:\Users\NAN\Desktop\Just Dhamma\justdhamma.github.io\_books\bhikkhu-k-nanananda\the-law-of-dependent-origination"

for filename in os.listdir(dir_path):
    if not filename.endswith('-en.md'):
        continue
    m = re.match(r'^sermon-(\d+)-en\.md$', filename)
    if not m:
        continue
    n = m.group(1)
    filepath = os.path.join(dir_path, filename)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract body after existing front matter (if any)
    body = ''
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            body = parts[2]

    new_front = f"""---
lang: en
layout: post
category: books
book_author: bhikkhu-k-nanananda
book_key: the-law-of-dependent-origination
title: Sermon {n}
permalink: /books/bhikkhu-k-nanananda/the-law-of-dependent-origination/sermon-{n}-en/
gem_url: /books/bhikkhu-k-nanananda/the-law-of-dependent-origination/sermon-{n}-ne-gem/
gpt_url: /books/bhikkhu-k-nanananda/the-law-of-dependent-origination/sermon-{n}-ne-gpt/
cld_url: /books/bhikkhu-k-nanananda/the-law-of-dependent-origination/sermon-{n}-ne-cld/
doc_url: "https://seeingthroughthenet.net/wp-content/uploads/2016/12/The-Law-of-Dependent-Arising_LE_Rev_1.0.pdf"
alt_doc_url: 
---"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_front + body)

    print(f"Updated {filename}")

print("Done")
