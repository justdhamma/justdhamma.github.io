---
layout: english
title: Essays
lang: en
permalink: /en/essays/
---

## All Essays

{% assign essays = site.essays | where: "lang", "en" | sort: "date" | reverse %}
{% assign authors = essays | group_by: "author" | sort_natural: "name" %}

{% for author in authors %}
<h3>{{ author.name }}</h3>
<ul class="essay-translation-list">
{% for post in author.items %}
    {% assign nepali_translations = site.essays | where: "lang", "ne" | where: "en_url", post.url %}
    {% assign gpt_translation = nepali_translations | where: "translator", "gpt" | first %}
    {% assign gemini_translation = nepali_translations | where: "translator", "gemini" | first %}
    {% assign claude_translation = nepali_translations | where: "translator", "claude" | first %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
      {% if nepali_translations.size > 0 %}
        <span class="essay-translation-links">
        -
        {% assign comma = "" %}
        {% if gemini_translation %}
          {{ comma }}<a href="{{ gemini_translation.url }}">Gemini</a>
          {% assign comma = ", " %}
        {% endif %}
        {% if gpt_translation %}
          {{ comma }}<a href="{{ gpt_translation.url }}">GPT</a>
          {% assign comma = ", " %}
        {% endif %}
        {% if claude_translation %}
          {{ comma }}<a href="{{ claude_translation.url }}">Claude</a>
        {% endif %}
        </span>
      {% endif %}
    </li>
{% endfor %}
</ul>
{% endfor %}
