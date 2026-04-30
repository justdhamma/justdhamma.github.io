---
layout: english
title: Transcript Tags
lang: en
permalink: /en/transcript-tags/
---

## Transcript Tags

{% assign transcripts = site.transcripts | sort: "episode" %}
{% capture all_pli_tags %}
{% for post in transcripts %}
  {% if post.pli_tag %}
    {% assign split_tags = post.pli_tag | split: "," %}
    {% for raw_tag in split_tags %}
      {% assign tag = raw_tag | strip | downcase %}
      {% if tag != "" %}
{{ tag }}|||
      {% endif %}
    {% endfor %}
  {% endif %}
{% endfor %}
{% endcapture %}

{% assign unique_pli_tags = all_pli_tags | strip | split: "|||" | uniq | sort_natural %}

{% capture all_english_tags %}
{% for raw_tag in unique_pli_tags %}
  {% assign tag = raw_tag | strip %}
  {% assign english_tag = site.data.pli_tags[tag] %}
  {% if english_tag and english_tag != "" %}
{{ english_tag | strip | downcase }}|||
  {% endif %}
{% endfor %}
{% endcapture %}

{% assign unique_english_tags = all_english_tags | strip | split: "|||" | uniq | sort_natural %}

<h3>Pali Tags</h3>
<p class="transcript-tag-index">
{% assign separator = "" %}
{% for raw_tag in unique_pli_tags %}
  {% assign tag = raw_tag | strip %}
  {% if tag != "" %}
    {{ separator }}<a href="#tag-{{ tag | slugify }}">{{ tag }}</a>
    {% assign separator = " · " %}
  {% endif %}
{% endfor %}
</p>

<hr class="transcript-tag-divider">

<h3>English Tags</h3>
<p class="transcript-tag-index">
{% assign separator = "" %}
{% for raw_tag in unique_english_tags %}
  {% assign english_tag = raw_tag | strip %}
  {% if english_tag != "" %}
    {% assign linked_pali_tag = "" %}
    {% for raw_pali_tag in unique_pli_tags %}
      {% assign pali_tag = raw_pali_tag | strip %}
      {% if site.data.pli_tags[pali_tag] == english_tag %}
        {% assign linked_pali_tag = pali_tag %}
        {% break %}
      {% endif %}
    {% endfor %}
    {{ separator }}<a href="#tag-{{ linked_pali_tag | slugify }}">{{ english_tag }}</a>
    {% assign separator = " · " %}
  {% endif %}
{% endfor %}
</p>

<hr class="transcript-tag-divider">

{% for raw_tag in unique_pli_tags %}
  {% assign tag = raw_tag | strip %}
  {% assign english_tag = site.data.pli_tags[tag] %}
  {% if tag != "" %}
<section class="transcript-tag-section" id="tag-{{ tag | slugify }}">
  <h3>{% if english_tag and english_tag != "" %}{{ tag }} ({{ english_tag }}){% else %}{{ tag }}{% endif %}</h3>

<ul class="transcript-list">
{% for post in transcripts %}
  {% if post.pli_tag %}
    {% assign split_tags = post.pli_tag | split: "," %}
    {% for candidate in split_tags %}
      {% assign normalized_candidate = candidate | strip | downcase %}
      {% if normalized_candidate == tag %}
  <li><a href="{{ post.url }}">{{ post.episode }}{{ post.editor | default: "" }} - {{ post.title }}</a></li>
        {% break %}
      {% endif %}
    {% endfor %}
  {% endif %}
{% endfor %}
</ul>
</section>
  {% endif %}
{% endfor %}
