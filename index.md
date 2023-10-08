---
layout: default
title: Home
nav_order: 1
description: "Middlware Home"
permalink: /
---

{% for item in site.app-servers %}
  <h2>PP
    <a href="{{ item.url }}">
      {{ item.title }} - {{ item.parent }}
    </a>
  </h2>
  <p>{{ item.content | markdownify }}</p>
{% endfor %}