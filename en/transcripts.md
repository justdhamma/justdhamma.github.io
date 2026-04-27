---
layout: english
title: Transcripts
lang: en
---
<!--
## All Transcripts -->

<!-- {% assign transcripts = site.posts | where: "category", "transcript" %} -->
<!-- {% assign transcripts = site.posts | where: "category", "transcript" | sort: "video_id" %} -->

<!-- <ul> 
{% for post in transcripts %} 
    <li> <a href="{{ post.url }}">{{ post.title }}</a><br>
    <small>{{ post.date | date: "%Y-%m-%d" }}</small> </li>

    <p>{{ post.excerpt }}</p>
{% endfor %} 
</ul>

👉 New here? Start with any transcript. -->

## All Transcripts

<!-- {% assign transcripts = site.posts | where: "category", "transcript" | sort: "video_id" %} -->
{% assign transcripts = site.posts | where: "category", "transcript" | sort: "video_id" | reverse %}

<ul> 
{% for post in transcripts %} 
    <li>
        <a href="{{ post.url }}">{{ post.title }}</a><br>
        <!-- <small>Video ID: {{ post.video_id }}</small> -->
    </li>

    <!-- <p>{{ post.excerpt }}</p> -->
{% endfor %} 
</ul>

👉 New here? Start with any transcript.