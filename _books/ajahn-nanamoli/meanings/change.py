import os
import re
 
dir_path = r"c:\Users\NAN\Desktop\Just Dhamma\justdhamma.github.io\_books\ajahn-nanamoli\meanings"
 
for filename in os.listdir(dir_path):
    if not filename.startswith('en-') or not filename.endswith('.md'):
        continue
    # en-appearance-and-existence.md -> appearance-and-existence-en.md
    stem = filename[3:-3]  # remove 'en-' and '.md'
    new_filename = f"{stem}-en.md"
    old_path = os.path.join(dir_path, filename)
    new_path = os.path.join(dir_path, new_filename)
 
    with open(old_path, 'r', encoding='utf-8') as f:
        content = f.read()
 
    # Update permalink if present: en-appearance-and-existence -> appearance-and-existence-en
    content = re.sub(
        r'^(permalink:\s*/books/ajahn-nanamoli/meanings/)en-(.+?)(-?)(/?\s*)$',
        rf'\1\2-en\4',
        content,
        flags=re.MULTILINE
    )
 
    # Update ne_url if present
    content = re.sub(
        r'^(ne_url:\s*"?/?essays/)ne-(.+?)("?\s*)$',
        rf'\1\2-ne\3',
        content,
        flags=re.MULTILINE
    )
 
    with open(new_path, 'w', encoding='utf-8') as f:
        f.write(content)
 
    os.remove(old_path)
    print(f"Renamed {filename} -> {new_filename}")
 
print("Done")