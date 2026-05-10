import os
import re

dir_path = r"c:\Users\NAN\Desktop\Just Dhamma\justdhamma.github.io\_books\bhikkhu-k-nanananda\nibbana-the-mind-stilled"

for filename in os.listdir(dir_path):
    if not filename.endswith('-en.md'):
        continue
    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'cld_url' in content:
        continue

    # Extract sermon number from filename like sermon-1-en.md
    match = re.search(r'sermon-(\d+)-en\.md', filename)
    if not match:
        continue
    n = match.group(1)

    cld_line = f'cld_url: /books/bhikkhu-k-nanananda/nibbana-the-mind-stilled/sermon-{n}-ne-cld/'

    # Insert cld_url after gpt_url line
    content = re.sub(
        r'(gpt_url: .*?)\n',
        r'\1\n' + cld_line + '\n',
        content,
        count=1
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filename}")

print("Done")
