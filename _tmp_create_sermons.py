import os
base = r'c:\Users\NAN\Desktop\Just Dhamma\justdhamma.github.io\_books\bhikkhu-k-nanananda\nibbana-the-mind-stilled'
for n in range(6, 33):
    content = (
        '---\n'
        'lang: en\n'
        'layout: post\n'
        'category: books\n'
        'book_author: bhikkhu-k-nanananda\n'
        'book_key: nibbana-the-mind-stilled\n'
        'title: Nibbana Sermon ' + str(n) + '\n'
        'permalink: /books/bhikkhu-k-nanananda/nibbana-the-mind-stilled/nibbana-sermon-' + str(n) + '-en/\n'
        'gem_url: /books/bhikkhu-k-nanananda/nibbana-the-mind-stilled/nibbana-sermon-' + str(n) + '-ne-gem/\n'
        'gpt_url: /books/bhikkhu-k-nanananda/nibbana-the-mind-stilled/nibbana-sermon-' + str(n) + '-ne-gpt/\n'
        'cld_url: /books/bhikkhu-k-nanananda/nibbana-the-mind-stilled/nibbana-sermon-' + str(n) + '-ne-cld/\n'
        'doc_url: "https://seeingthroughthenet.net/wp-content/uploads/2018/03/Mind-Stilled_HTML.htm"\n'
        'alt_doc_url: \n'
        '---\n'
    )
    path = os.path.join(base, 'sermon-' + str(n) + '-en.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Created ' + path)
