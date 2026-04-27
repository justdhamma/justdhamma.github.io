---
layout: english
title: Essays
lang: en
---

## All Articles

<!-- {% assign en_posts = site.posts | where: "lang", "en" %} -->
{% assign en_posts = en_posts | where: "category", "articles" %}

<ul> 
{% for post in en_posts %} 
    <li> <a href="{{ post.url }}">{{ post.title }}</a><br>
    <small>{{ post.date | date: "%Y-%m-%d" }}</small> </li>

    <p>{{ post.excerpt }}</p>
{% endfor %} 
</ul>

👉 New here? Start with any essay.