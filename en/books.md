---
layout: english
title: Books
lang: en
permalink: /en/books/
---

## All Books

{% assign books = site.books | where: "lang", "en" | sort_natural: "path" %}
{% assign authors = site.data.authors | sort: "id" %}

{% if books.size > 0 %}
  <div class="books-by-author">
  {% for author in authors %}
    {% assign author_config = site.data.book_order.authors[author.key] %}
    {% assign author_folder = author_config.folder | default: author.key %}
    {% capture author_segment %}/{{ author_folder }}/{% endcapture %}
    {% assign author_books = books | where_exp: "item", "item.path contains author_segment" %}

    {% if author_books.size > 0 %}
<section class="book-index-author">
  <h2 class="author-name">{{ author.name }}</h2>
  <div class="book-index-grid">
  {% if author_config %}
    {% for book_config in author_config.books %}
      {% capture book_folder %}/{{ author_folder }}/{{ book_config.key }}/{% endcapture %}
      {% assign book_chapters = author_books | where_exp: "item", "item.path contains book_folder" %}
      {% if book_chapters.size > 0 %}
        <a class="book-index-card" href="/en/books/{{ author.key }}/{{ book_config.key }}/">
          <span class="book-index-card__title">{{ book_config.title }}</span>
          <span class="book-index-card__meta">Open table of contents</span>
        </a>
      {% endif %}
    {% endfor %}
  {% else %}
    {% assign seen_books = "" %}
    {% for chapter in author_books %}
      {% assign parts = chapter.path | split: "/" %}
      {% assign book_key = parts[2] %}
      {% unless seen_books contains book_key %}
        {% assign seen_books = seen_books | append: book_key | append: "," %}
        <a class="book-index-card" href="/en/books/{{ author.key }}/{{ book_key }}/">
          <span class="book-index-card__title">{{ book_key | replace: '-', ' ' | capitalize }}</span>
          <span class="book-index-card__meta">Open table of contents</span>
        </a>
      {% endunless %}
    {% endfor %}
  {% endif %}
  </div>
</section>
    {% endif %}
  {% endfor %}
  </div>
{% else %}
<p><em>Books coming soon...</em></p>
{% endif %}
