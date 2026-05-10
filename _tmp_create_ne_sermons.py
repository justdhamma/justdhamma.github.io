import os

base = r'c:\Users\NAN\Desktop\Just Dhamma\justdhamma.github.io\_books\bhikkhu-k-nanananda\nibbana-the-mind-stilled'

devanagari = {
    '1': '१', '2': '२', '3': '३', '4': '४', '5': '५',
    '6': '६', '7': '७', '8': '८', '9': '९', '0': '०'
}

def to_dev(n):
    return ''.join(devanagari[ch] for ch in str(n))

suffix_map = {
    '-ne-gpt.md': 'gpt',
    '-ne-gem.md': 'gem',
    '-ne-cld.md': 'cld'
}

for n in range(1, 34):
    s = str(n)
    dev = to_dev(n)
    for suffix, translator in suffix_map.items():
        content = (
            '---\n'
            'lang: ne\n'
            'layout: post\n'
            'category: books\n'
            'book_author: bhikkhu-k-nanananda\n'
            'book_key: nibbana-the-mind-stilled\n'
            'en_title: Nibbana Sermon ' + s + '\n'
            'ne_title: निर्वाण उपदेश ' + dev + '\n'
            'en_url: "/books/bhikkhu-k-nanananda/nibbana-the-mind-stilled/nibbana-sermon-' + s + '-en/"\n'
            'permalink: /books/bhikkhu-k-nanananda/nibbana-the-mind-stilled/nibbana-sermon-' + s + '-en/\n'
            'gem_url: "/books/bhikkhu-k-nanananda/nibbana-the-mind-stilled/nibbana-sermon-' + s + '-ne-gem/"\n'
            'gpt_url: "/books/bhikkhu-k-nanananda/nibbana-the-mind-stilled/nibbana-sermon-' + s + '-ne-gpt/"\n'
            'cld_url: "/books/bhikkhu-k-nanananda/nibbana-the-mind-stilled/nibbana-sermon-' + s + '-ne-cld/"\n'
            'description: a book\n'
            'type: translation\n'
            'translator: ' + translator + '\n'
            '# date: 2010-08-01\n'
            'proofread: unfinished\n'
            '---\n'
        )
        path = os.path.join(base, 'sermon-' + s + suffix)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Created ' + path)
