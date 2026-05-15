#!/usr/bin/env python3
import os, re, os.path as p

files = [
    "_transcripts/hillside-hermitage/01-can-love-be-path-of-happiness-ne-gem.md",
    "_transcripts/hillside-hermitage/104hh-right-meditation-is-not-observation-en.md",
    "_transcripts/hillside-hermitage/169hh-the-context-of-your-suffering-en.md",
    "_transcripts/hillside-hermitage/2018-10-22-transcript-On_Nanavira_Theras_Notes_on_Dhamma_Anicca.md",
    "_transcripts/hillside-hermitage/235hh-escape-from-the-body.md",
    "_transcripts/hillside-hermitage/236hh-desire-to-end-desire.md",
    "_transcripts/hillside-hermitage/255hh-no-joy-no-misery.md",
    "_transcripts/hillside-hermitage/284hh-the-meaning-of-samadhi-en.md",
    "_transcripts/hillside-hermitage/287hh-how-to-abandon-self-view-en.md",
    "_transcripts/hillside-hermitage/310hh-confined-within-this-body.md",
    "_transcripts/hillside-hermitage/337hh-a-peaceful-death.md",
    "_transcripts/hillside-hermitage/341hh-abortion-of-samsara.md",
    "_transcripts/hillside-hermitage/364hh-ascetic-vs-aesthetic-en.md",
    "_transcripts/hillside-hermitage/48-do-you-see-what-is-present-ne-gem.md",
    "_transcripts/hillside-hermitage/48-do-you-see-what-is-present-ne-gpt.md",
    "_transcripts/hillside-hermitage/53-the-right-kind-of-questioning-ne-cld.md",
    "_transcripts/hillside-hermitage/53-the-right-kind-of-questioning-ne-gem.md",
    "_transcripts/hillside-hermitage/53-the-right-kind-of-questioning-ne-gpt.md",
    "_transcripts/hillside-hermitage/54hh-dfsfs.md",
    "_transcripts/samanadipa-hermitage/1sh-early-buddhism-approaching-the-buddhas-teaching-en.md"
]

pat = re.compile(r'^(episode:\s*)(\d+)(\s*)$', re.MULTILINE)
cwd = os.getcwd()

for rel in files:
    path = p.join(cwd, rel)
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    new_text, n = pat.subn(lambda m: f"{m.group(1)}'{m.group(2)}'{m.group(3)}", text)
    if n == 0:
        raise SystemExit(f'No episode line changed in {rel}')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print(f'Updated {rel}: {n}')

print("All episodes normalized to strings!")
