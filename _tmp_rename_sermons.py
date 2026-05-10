import os
import re

dir_path = r"c:\Users\NAN\Desktop\Just Dhamma\justdhamma.github.io\_books\bhikkhu-k-nanananda\the-law-of-dependent-origination"

for filename in os.listdir(dir_path):
    m = re.match(r'^en-sermon-(\d+)\.md$', filename)
    if not m:
        continue
    n = m.group(1)
    old_path = os.path.join(dir_path, filename)
    new_filename = f"sermon-{n}-en.md"
    new_path = os.path.join(dir_path, new_filename)

    with open(old_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update permalink if present
    content = re.sub(
        r'^(permalink:\s*/books/bhikkhu-k-nanananda/the-law-of-dependent-origination/)en-sermon-(\d+)(/?.*)$',
        rf'\1sermon-\2-en\3',
        content,
        flags=re.MULTILINE
    )

    with open(new_path, 'w', encoding='utf-8') as f:
        f.write(content)

    os.remove(old_path)
    print(f"Renamed {filename} -> {new_filename}")

print("Done")
