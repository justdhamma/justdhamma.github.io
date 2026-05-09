---
layout: english
title: Essays
lang: en
permalink: /en/essays/
---

## All Essays

{% assign essays = site.essays | where: "lang", "en" %}
{% assign authors = site.data.authors | sort: "id" %}

{% for author in authors %}
{% assign author_posts = essays | where_exp: "item", "item.path contains author.key" | sort_natural: "title" %}
{% if author_posts.size > 0 %}
<details class="author-section">
  <summary class="author-name">{{ author.name }}</summary>
  <ul class="essay-translation-list">
  {% for post in author_posts %}
      <li>
        <a href="{{ post.url }}">{{ post.title }}</a>
        {% capture essay_translation_links %}{% include translation-links.html doc=post %}{% endcapture %}
        {% assign essay_translation_links = essay_translation_links | strip %}
        {% if essay_translation_links != "" %}
          <span class="essay-translation-links"> – {{ essay_translation_links }}</span>
        {% endif %}
      </li>
  {% endfor %}
  </ul>
</details>
{% endif %}
{% endfor %}
