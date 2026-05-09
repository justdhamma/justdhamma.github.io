---
layout: english
title: Transcripts
lang: en
permalink: /en/transcripts/
---

## All Transcripts

{% assign transcripts = site.transcripts | where: "lang", "en" | sort: "episode" %}
{% assign channels = transcripts | map: "channel" | uniq %}

{% for channel_name in channels %}
  {% assign channel_transcripts = transcripts | where: "channel", channel_name | sort: "episode" %}
  
<details class="author-section">
  <summary class="author-name">{{ channel_name | split: '-' | first | capitalize }} {{ channel_name | split: '-' | last | capitalize }}</summary>
  <ul class="transcript-list">
  {% for post in channel_transcripts %}
    <li>
      <a href="{{ post.url }}">
        {{ post.episode | plus: 0}}hh - {{ post.en_title | default: post.title }}
      </a>
      {% capture tlinks %}{% include translation-links.html doc=post %}{% endcapture %}{% assign tlinks_stripped = tlinks | strip %}{% if tlinks_stripped != "" %} – <span class="transcript-translation-links">{{ tlinks_stripped }}</span>{% endif %}
    </li>
  {% endfor %}
  </ul>
</details>
{% endfor %}
