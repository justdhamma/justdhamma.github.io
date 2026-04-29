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
    {% assign gemini_post = group.items | where: "translator", "gemini" | first %}
    {% assign gpt_post = group.items | where: "translator", "gpt" | first %}
    {% assign claude_post = group.items | where: "translator", "claude" | first %}
    {% assign perplexity_post = group.items | where: "translator", "perplexity" | first %}
    <li>
      {% if english_post %}
        {{ english_post.title }}
      {% elsif canonical.en_title %}
        {{ canonical.en_title }}
      {% else %}
        {{ canonical.title }}
      {% endif %}

      {% assign separator = " - " %}
      {% if gemini_post %}
        {{ separator }}<a href="{{ gemini_post.url }}">Gemini</a>
        {% assign separator = " · " %}
      {% endif %}
      {% if gpt_post %}
        {{ separator }}<a href="{{ gpt_post.url }}">GPT</a>
        {% assign separator = " · " %}
      {% endif %}
      {% if claude_post %}
        {{ separator }}<a href="{{ claude_post.url }}">Claude</a>
        {% assign separator = " · " %}
      {% endif %}
      {% if perplexity_post %}
        {{ separator }}<a href="{{ perplexity_post.url }}">Perplexity</a>
      {% endif %}
    </li>
{% endfor %}
</ul>
{% endfor %}
