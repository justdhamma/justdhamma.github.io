import os
import re

dir_path = r"c:\Users\NAN\Desktop\Just Dhamma\justdhamma.github.io\_books\bhikkhu-k-nanananda\nibbana-the-mind-stilled"

fields = ['gem_url', 'gpt_url', 'permalink', 'cld_url', 'en_url']

for filename in os.listdir(dir_path):
    if not filename.endswith('.md'):
        continue
    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    for field in fields:
        # Match field: "...nibbana-sermon-..." or field: /...nibbana-sermon-...
        pattern = rf"(^\s*{field}:\s*)([\"']?)(.*?)(nibbana-sermon-)(.*?)(\2)\s*$"
        content = re.sub(pattern, rf"\1\2\3sermon-\5\6", content, flags=re.MULTILINE)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filename}")

print("Done")
