---
layout: nepali
title: निबन्धहरू
lang: ne
---

## सबै निबन्धहरू

{% assign ne_posts = site.posts | where: "lang", "ne" %}

<ul> 
{% for post in ne_posts %} 
    <li> <a href="{{ post.url }}">{{ post.title }}</a><br>
    <small>{{ post.date | date: "%Y-%m-%d" }}</small> </li>

    <p>{{ post.excerpt }}</p>
{% endfor %} 
</ul>

👉 नयाँ पाठक हुनुहुन्छ? सुरु गर्न केही निबन्ध छान्नुहोस्।