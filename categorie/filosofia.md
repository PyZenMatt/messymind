---
layout: default
title: Spiritualità
permalink: /categorie/filosofia/
---

<div class="container mt-5">
  <div class="row">
    <div class="col-12">
      <h1 class="display-4 mb-4">Categoria: Filosofia</h1>
      <div class="row">
        {% for post in site.categories.filosofia %}
        <div class="col-lg-6 mb-4">
          <div class="card h-100 shadow-sm">
            <div class="row g-0">
              <div class="col-md-4">
                <img src="{{ post.background | default: '/assets/images/default-post.jpg' }}" 
                     class="img-fluid rounded-start" 
                     alt="{{ post.title }}"
                     style="height: 150px; object-fit: cover;">
              </div>
              <div class="col-md-8">
                <div class="card-body">
                  <a href="{{ post.url }}" class="text-decoration-none text-dark">
                    <h5 class="card-title">{{ post.title }}</h5>
                  </a>
                  <p class="card-text">{{ post.excerpt | strip_html | truncatewords: 20 }}</p>
                  <p class="text-muted small mb-0">
                    <i class="far fa-calendar-alt"></i> {{ post.date | date: "%d/%m/%Y" }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
        {% endfor %}
      </div>
    </div>
  </div>
</div>