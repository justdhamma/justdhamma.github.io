#!/usr/bin/env python3
import os
import shutil

base_dir = r"c:\Users\NAN\Desktop\Just Dhamma\justdhamma.github.io\_transcripts\hillside-hermitage"

files_to_rename = [
    ("01-can-love-be-path-of-happiness-en.md", "1-can-love-be-path-of-happiness-en.md"),
    ("02-why-is-celibacy-important-en.md", "2-why-is-celibacy-important-en.md"),
    ("03-how-to-overcome-attachments-en.md", "3-how-to-overcome-attachments-en.md"),
    ("04-do-we-live-only-once-en.md", "4-do-we-live-only-once-en.md"),
    ("05-purpose-of-the-precepts-en.md", "5-purpose-of-the-precepts-en.md"),
    ("06-why-is-generosity-good-en.md", "6-why-is-generosity-good-en.md"),
]

for old_name, new_name in files_to_rename:
    old_path = os.path.join(base_dir, old_name)
    new_path = os.path.join(base_dir, new_name)
    if os.path.exists(old_path):
        shutil.move(old_path, new_path)
        print(f"Renamed: {old_name} → {new_name}")
    else:
        print(f"File not found: {old_name}")

print("All files renamed successfully!")
