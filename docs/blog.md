---
layout: default
summary: Seoul Artificial Intelligence Meetup (aka Seoul AI) is a group of enthusiasts willing to go the extra mile in becoming one of the best in their field. We are sharing our domain knowledge and working on Machine Learning projects in small groups.
tags: [Seoul,"Artificial Intelligence",meetup,AI,call,presenters,practioners,"Machine Learning",Korea,Gangnam]
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
