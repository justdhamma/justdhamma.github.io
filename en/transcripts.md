---
layout: english
title: Transcripts
lang: en
permalink: /en/transcripts/
---

## All Transcripts

{% assign transcripts = site.transcripts | sort: "episode" %}

<!-- <ul>
{% for post in transcripts %}
  <li>
    <a href="{{ post.url }}">{{ post.title }}</a><br>
    <small>{{ post.video_id }}</small>
  </li>
{% endfor %}
</ul> -->


<ul>
{% for post in transcripts %}
  <li>
    <a href="{{ post.url }}">
      <!-- {{post.episode}}hh - {{ post.title }} - {{post.editor}} -->
       {{ post.episode | plus: 0}}hh - {{ post.title }} - <em>{{ post.editor | default: 'Unknown' }}</em>
    </a>
  </li>
{% endfor %}
</ul>