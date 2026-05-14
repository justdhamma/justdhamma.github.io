import os
import re
import yaml

# Directory containing the md files
dir_path = r'c:\Users\NAN\Desktop\Just Dhamma\justdhamma.github.io\_transcripts\hillside-hermitage'

# Get all md files
files = [f for f in os.listdir(dir_path) if f.endswith('.md')]

# Extract episodes
episodes = []
for f in files:
    match = re.match(r'(\d+)-', f)
    if match:
        episodes.append(int(match.group(1)))

episodes.sort()

# Map episode to previous
prev_map = {}
for i, ep in enumerate(episodes):
    if i > 0:
        prev_map[ep] = episodes[i-1]

# Function to get pli_tag and eng_tag based on title
def get_tags(title):
    title_lower = title.lower()
    if 'love' in title_lower:
        return 'metta', 'love'
    elif 'celibacy' in title_lower or 'attachments' in title_lower:
        return 'brahmacariya', 'celibacy'
    elif 'live only once' in title_lower or 'death' in title_lower or 'impermanence' in title_lower:
        return 'anicca', 'impermanence'
    elif 'precepts' in title_lower or 'virtue' in title_lower:
        return 'sila', 'virtue'
    elif 'generosity' in title_lower:
        return 'dana', 'generosity'
    elif 'sensuality' in title_lower or 'desire' in title_lower:
        return 'kama', 'sensuality'
    elif 'shame' in title_lower or 'conscience' in title_lower:
        return 'hiri', 'shame'
    elif 'wisdom' in title_lower or 'understanding' in title_lower:
        return 'panna', 'wisdom'
    elif 'noble truths' in title_lower:
        return 'ariya_sacca', 'noble_truths'
    elif 'meditation' in title_lower or 'samadhi' in title_lower:
        return 'samadhi', 'meditation'
    elif 'mindfulness' in title_lower:
        return 'sati', 'mindfulness'
    elif 'pain' in title_lower or 'suffering' in title_lower:
        return 'dukkha', 'suffering'
    elif 'jhana' in title_lower:
        return 'jhana', 'absorption'
    elif 'nibbana' in title_lower:
        return 'nibbana', 'liberation'
    else:
        return 'dhamma', 'dhamma'  # default

# Process each file
for f in files:
    file_path = os.path.join(dir_path, f)
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract frontmatter
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        continue
    frontmatter_str = match.group(1)
    
    # Parse frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_str)
    except:
        continue
    
    # Get episode
    episode_match = re.match(r'(\d+)-', f)
    if not episode_match:
        continue
    episode = int(episode_match.group(1))
    
    # Get title from file name
    title_match = re.match(r'\d+-(.+)-en\.md', f)
    if title_match:
        title_raw = title_match.group(1).replace('-', ' ')
        title = ' '.join(word.capitalize() for word in title_raw.split())
    else:
        title = frontmatter.get('title', 'Unknown')
    
    # Get tags
    pli_tag, eng_tag = get_tags(title)
    
    # Get previous
    previous_ep = prev_map.get(episode)
    if previous_ep:
        # Find the file for previous_ep
        prev_file = None
        for pf in files:
            if pf.startswith(f'{previous_ep:03d}-') or pf.startswith(f'{previous_ep}-'):
                prev_file = pf
                break
        if prev_file:
            prev_title_match = re.match(r'\d+-(.+)-en\.md', prev_file)
            if prev_title_match:
                prev_title_raw = prev_title_match.group(1)
                previous = f'/transcripts/hillside-hermitage/{previous_ep}hh-{prev_title_raw}-en/'
            else:
                previous = ''
        else:
            previous = ''
    else:
        previous = ''
    
    # Build new frontmatter
    new_frontmatter = {
        'lang': 'en',
        'layout': 'post',
        'category': 'transcripts',
        'episode': episode,
        'title': title,
        'pli_tag': pli_tag,
        'eng_tag': eng_tag,
        'description': f'Talk no.{episode:02d}hh - condensed transcript',
        'excerpt': '',
        'youtube_url': frontmatter.get('youtube_url', ''),
        'gem_url': '',
        'gpt_url': '',
        'cld_url': '',
        'permalink': f'/transcripts/hillside-hermitage/{episode:02d}hh-{title_raw}-en/',
        'previous': previous,
        'channel': 'hillside-hermitage',
        'status': 'finished',
        'editor': 'hh'
    }
    
    # Convert to yaml
    new_frontmatter_str = yaml.dump(new_frontmatter, default_flow_style=False, allow_unicode=True)
    
    # Replace in content
    new_content = re.sub(r'^---\n.*?\n---', f'---\n{new_frontmatter_str}---', content, flags=re.DOTALL)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

print("Updated all frontmatters")