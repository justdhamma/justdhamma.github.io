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
      {% assign nepali_translations = site.essays | where: "lang", "ne" | where: "en_url", post.url %}
      {% assign gpt_translation = nepali_translations | where: "translator", "gpt" | first %}
      {% assign gemini_translation = nepali_translations | where: "translator", "gemini" | first %}
      {% assign claude_translation = nepali_translations | where: "translator", "claude" | first %}
      {% assign perplexity_translation = nepali_translations | where: "translator", "perplexity" | first %}
      <li>
        <a href="{{ post.url }}">{{ post.title }}</a>
        {% if nepali_translations.size > 0 %}
          <span class="essay-translation-links">
          -
          {% assign comma = "" %}
          {% if gemini_translation %}
            {{ comma }}<a href="{{ gemini_translation.url }}">Gemini</a>
            {% assign comma = " · " %}
          {% endif %}
          {% if gpt_translation %}
            {{ comma }}<a href="{{ gpt_translation.url }}">GPT</a>
            {% assign comma = " · " %}
          {% endif %}
          {% if claude_translation %}
            {{ comma }}<a href="{{ claude_translation.url }}">Claude</a>
            {% assign comma = " · " %}
          {% endif %}
          {% if perplexity_translation %}
            {{ comma }}<a href="{{ perplexity_translation.url }}">Perplexity</a>
          {% endif %}
          </span>
        {% endif %}
      </li>
  {% endfor %}
  </ul>
</details>
{% endif %}
{% endfor %}
