---
layout: home
title: Blog
permalink: /blog/
---

<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        scroll-behavior: smooth;
    }

    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #f4fff4, #e8f5e9);
        color: #1f2937;
        line-height: 1.6;
    }

    a {
        text-decoration: none;
        color: inherit;
    }

    img {
        max-width: 100%;
        display: block;
    }

    .container {
        width: 90%;
        max-width: 1200px;
        margin: auto;
    }

    .page-header {
        background: linear-gradient(135deg, rgba(22, 101, 52, 0.8), rgba(5, 46, 22, 0.9)),
            url('https://images.unsplash.com/photo-1507843872452-4319c4f8f6af?q=80&w=1600&auto=format&fit=crop') center/cover no-repeat;
        padding: 120px 0;
        text-align: center;
        color: white;
        margin-bottom: 80px;
    }

    .page-header h1 {
        font-size: 3.5rem;
        margin-bottom: 10px;
        font-weight: 800;
    }

    .page-header p {
        font-size: 1.1rem;
        color: #dcfce7;
    }

    .blog-container {
        margin-bottom: 80px;
    }

    .blog-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 30px;
    }

    .blog-post-card {
        background: white;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(34, 197, 94, 0.1);
    }

    .blog-post-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 40px rgba(34, 197, 94, 0.15);
        border-color: rgba(34, 197, 94, 0.3);
    }

    .blog-post-card img {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }

    .blog-post-content {
        padding: 24px;
    }

    .blog-post-date {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.9rem;
        color: #6b7280;
        margin-bottom: 12px;
    }

    .blog-post-date span {
        color: #166534;
        font-weight: 600;
    }

    .blog-post-content h3 {
        font-size: 1.5rem;
        color: #166534;
        margin-bottom: 12px;
        line-height: 1.4;
    }

    .blog-post-content p {
        color: #4b5563;
        line-height: 1.8;
        margin-bottom: 16px;
        font-size: 0.95rem;
    }

    .read-more {
        display: inline-block;
        background: linear-gradient(135deg, #22c55e, #15803d);
        color: white;
        padding: 10px 22px;
        border-radius: 8px;
        font-weight: 600;
        transition: 0.3s ease;
    }

    .read-more:hover {
        transform: translateX(4px);
    }

    .no-posts {
        text-align: center;
        padding: 60px 20px;
        color: #6b7280;
    }

    .no-posts h3 {
        font-size: 1.5rem;
        margin-bottom: 10px;
    }

    @media (max-width: 900px) {
        .page-header h1 {
            font-size: 2.5rem;
        }

        .blog-grid {
            grid-template-columns: 1fr;
        }
    }
</style>

<section class="page-header">
    <div class="container">
        <h1>📰 Blog</h1>
        <p>Stories, Updates & News from Merahi Village</p>
    </div>
</section>

<main class="blog-container">
    <div class="container">
        <div class="blog-grid">
            {% if site.posts.size > 0 %}
                {% for post in site.posts %}
                    <article class="blog-post-card">
                        {% if post.image %}
                            <img src="{{ post.image }}" alt="{{ post.title }}">
                        {% else %}
                            <img src="https://images.unsplash.com/photo-1507843872452-4319c4f8f6af?q=80&w=1200&auto=format&fit=crop" alt="Blog Post">
                        {% endif %}
                        <div class="blog-post-content">
                            <div class="blog-post-date">
                                📅 <span>{{ post.date | date: "%B %d, %Y" }}</span>
                            </div>
                            <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
                            <p>{{ post.excerpt | strip_html | truncatewords: 30 }}</p>
                            <a href="{{ post.url }}" class="read-more">Read More →</a>
                        </div>
                    </article>
                {% endfor %}
            {% else %}
                <div class="no-posts" style="grid-column: 1 / -1;">
                    <h3>🚀 Blog Coming Soon!</h3>
                    <p>Start publishing posts in the blog/_posts folder and they will appear here automatically.</p>
                </div>
            {% endif %}
        </div>
    </div>
</main>
