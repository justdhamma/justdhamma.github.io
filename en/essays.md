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
<ul>
{% for post in author.items %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a><br>
      <small>{{ post.date | date: "%Y-%m-%d" }}</small>
    </li>
{% endfor %}
</ul>
{% endfor %}
