---
layout: default
summary: Seoul AI Blog&#x3a; Share your knowledge with other AI enthusiasts!
tags: [Seoul,"Artificial Intelligence",meetup,AI,"Machine Learning",NN,"Neural Networks",Korea,Gangnam]
---

# Blog

{% assign postsByYearMonth = site.posts | group_by_exp:"post", "post.date | date: '%Y %b'"  %}
{% for yearMonth in postsByYearMonth %}
  <h3>{{ yearMonth.name }}</h3>
  <div>
    <ul>
      {% for post in yearMonth.items %}
        <li><a href="{{ post.url }}">{{ post.title }}</a></li>
      {% endfor %}
    </ul>
  </div>
{% endfor %}
