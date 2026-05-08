---
layout: nepali
title: Books
lang: ne
permalink: /ne/books/
---

## सबै पुस्तकहरु

{% assign books = site.books | where: "lang", "ne" | sort_natural: "path" %}
{% assign authors = site.data.authors | sort: "id" %}

{% if books.size > 0 %}
  {% for author in authors %}
    {% assign author_config = site.data.book_order.authors[author.key] %}
    {% assign author_folder = author_config.folder | default: author.key %}
    {% capture author_segment %}/{{ author_folder }}/{% endcapture %}
    {% assign author_books = books | where_exp: "item", "item.path contains author_segment" %}

    {% if author_books.size > 0 %}
<details class="author-section">
  <summary class="author-name">{{ author.name }}</summary>

  {% if author_config %}
    {% for book_config in author_config.books %}
      {% capture book_folder %}/{{ author_folder }}/{{ book_config.key }}/{% endcapture %}
      {% assign book_chapters = author_books | where_exp: "item", "item.path contains book_folder" %}

      {% if book_chapters.size > 0 %}
<details class="book-section">
  <summary>{{ book_config.title }}</summary>
  <ul class="book-chapter-list">
    {% if book_config.chapters %}
      {% for chapter_slug in book_config.chapters %}
        {% assign normalized_chapter_slug = chapter_slug | remove_first: "en-" | remove_first: "ne-" | replace: "-en", "" | replace: "-ne-gem", "" | replace: "-ne-gpt", "" | replace: "-ne-cld", "" | replace: "-ne-ppx", "" | replace: "-ne", "" %}
        {% assign chapter_found = false %}
        {% for chapter in book_chapters %}
          {% assign chapter_filename = chapter.path | split: "/" | last | remove: ".md" %}
          {% assign normalized_chapter_filename = chapter_filename | remove_first: "en-" | remove_first: "ne-" | replace: "-en", "" | replace: "-ne-gem", "" | replace: "-ne-gpt", "" | replace: "-ne-cld", "" | replace: "-ne-ppx", "" | replace: "-ne", "" %}
          {% if normalized_chapter_filename == normalized_chapter_slug and chapter_found == false %}
            {% capture toc_translation_links %}{% include translation-links.html doc=chapter %}{% endcapture %}
            {% assign toc_translation_links = toc_translation_links | strip %}
            <li>
              <a href="{{ chapter.url }}">{{ chapter.title }}</a>
              {% if toc_translation_links != "" %}
                <span class="book-toc-dash"> - </span>
                <span class="book-toc-links">{{ toc_translation_links }}</span>
              {% endif %}
            </li>
            {% assign chapter_found = true %}
          {% endif %}
        {% endfor %}
      {% endfor %}
    {% else %}
      {% for chapter in book_chapters %}
        {% capture toc_translation_links %}{% include translation-links.html doc=chapter %}{% endcapture %}
        {% assign toc_translation_links = toc_translation_links | strip %}
        <li>
          <a href="{{ chapter.url }}">{{ chapter.title }}</a>
          {% if toc_translation_links != "" %}
            <span class="book-toc-dash"> - </span>
            <span class="book-toc-links">{{ toc_translation_links }}</span>
          {% endif %}
        </li>
      {% endfor %}
    {% endif %}
  </ul>
</details>
      {% endif %}
    {% endfor %}
  {% else %}
    {% assign seen_books = "" %}
    {% for chapter in author_books %}
      {% assign parts = chapter.path | split: "/" %}
      {% assign book_key = parts[2] %}
      {% unless seen_books contains book_key %}
        {% assign seen_books = seen_books | append: book_key | append: "," %}
<details class="book-section">
  <summary>{{ book_key | replace: '-', ' ' | capitalize }}</summary>
  <ul class="book-chapter-list">
    {% for subchapter in author_books %}
      {% assign subparts = subchapter.path | split: "/" %}
      {% if subparts[2] == book_key %}
        <li><a href="{{ subchapter.url }}">{{ subchapter.title }}</a></li>
      {% endif %}
    {% endfor %}
  </ul>
</details>
      {% endunless %}
    {% endfor %}
  {% endif %}
</details>
    {% endif %}
  {% endfor %}
{% else %}
<p><em>पुस्तकहरु शिघ्रै आउने छन...</em></p>
{% endif %}
