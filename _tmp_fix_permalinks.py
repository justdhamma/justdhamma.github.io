import os, re

base = r'c:\Users\NAN\Desktop\Just Dhamma\justdhamma.github.io\_books\bhikkhu-k-nanananda\nibbana-the-mind-stilled'

for n in range(1, 34):
    for suffix in ['-ne-gpt.md', '-ne-gem.md', '-ne-cld.md']:
        fname = f'sermon-{n}{suffix}'
        path = os.path.join(base, fname)
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        # Extract translator from suffix, e.g. -ne-gpt -> ne-gpt
        trans = suffix[1:-3]  # ne-gpt etc
        old = f'permalink: /books/bhikkhu-k-nanananda/nibbana-the-mind-stilled/nibbana-sermon-{n}-en/'
        new = f'permalink: /books/bhikkhu-k-nanananda/nibbana-the-mind-stilled/nibbana-sermon-{n}-{trans}/'
        if old in text:
            text = text.replace(old, new, 1)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f'Updated {fname}')
        else:
            print(f'Skip {fname} (pattern not found)')
