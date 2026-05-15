#!/usr/bin/env python3
import os
import re
import yaml

# Find all transcript markdown files
transcript_dir = '_transcripts'
files_to_fix = []

for dirpath, _, filenames in os.walk(transcript_dir):
    for filename in filenames:
        if filename.endswith('.md'):
            filepath = os.path.join(dirpath, filename)
            files_to_fix.append(filepath)

print(f'Found {len(files_to_fix)} transcript files')

# Convert episode strings to integers
converted = 0
errors = 0

for filepath in files_to_fix:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.startswith('---'):
            continue
        
        parts = content.split('---', 2)
        if len(parts) < 3:
            continue
        
        # Replace quoted episode numbers with unquoted integers
        # Pattern: episode: '123' or episode: "123" → episode: 123
        front_matter = parts[1]
        new_front_matter = re.sub(
            r"episode:\s*['\"](\d+)['\"]",
            r'episode: \1',
            front_matter
        )
        
        if new_front_matter != front_matter:
            new_content = '---' + new_front_matter + '---' + parts[2]
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            converted += 1
            print(f'Updated: {filepath}')
    except Exception as e:
        errors += 1
        print(f'Error in {filepath}: {e}')

print(f'\nResult: {converted} files converted, {errors} errors')
print('All episodes are now integers!')
