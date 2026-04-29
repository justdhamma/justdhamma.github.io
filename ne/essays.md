---
layout: nepali
title: निबन्धहरू
lang: ne
permalink: /ne/essays/
---

## सबै निबन्धहरू

{% assign essays = site.essays | where: "lang", "ne" | sort: "date" | reverse %}
{% assign authors = essays | group_by: "author" | sort_natural: "name" %}

{% for author in authors %}
<h3 class="author-name">{{ author.name }}</h3>
<ul class="essay-translation-list">
{% assign grouped_essays = author.items | group_by: "en_url" %}
{% for group in grouped_essays %}
    {% assign canonical = group.items.first %}
    {% assign english_post = site.essays | where: "lang", "en" | where: "url", canonical.en_url | first %}
    {% assign gpt_post = group.items | where: "translator", "gpt" | first %}
    {% assign gemini_post = group.items | where: "translator", "gemini" | first %}
    {% assign claude_post = group.items | where: "translator", "claude" | first %}
    <li>
      {% if english_post %}
        {{ english_post.title }}
      {% elsif canonical.en_title %}
        {{ canonical.en_title }}
      {% else %}
        {{ canonical.title }}
      {% endif %}

      {% if gpt_post %}
        - <a href="{{ gpt_post.url }}">GPT</a>
      {% endif %}
      {% if gemini_post %}
        - <a href="{{ gemini_post.url }}">Gemini</a>
      {% endif %}
      {% if claude_post %}
        - <a href="{{ claude_post.url }}">Claude</a>
      {% endif %}
    </li>
{% endfor %}
</ul>
{% endfor %}
