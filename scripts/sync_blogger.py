#!/usr/bin/env python3
"""
sync_blogger.py — Pulls every post from the Merahi Village Blogger feed
and generates matching static HTML pages under blog/, styled with the
site's own GoGreen design system (same header/footer/CSS as every other
page). Also regenerates blog/index.html, a card grid of all posts.

Any embedded YouTube video / Instagram post / X (Twitter) post / Facebook
post inside a Blogger post is detected and replaced with a plain link —
the heavy embed/script is stripped, only a clickable link remains.

This script only ever reads/writes inside the blog/ folder. It never
touches any other file on the site.

Run manually:      python3 scripts/sync_blogger.py
Run automatically: see .github/workflows/sync-blog.yml
"""
import json
import os
import re
import urllib.request
import urllib.parse
from datetime import datetime
from html import escape
from bs4 import BeautifulSoup

FEED_URL = "https://merahivillage.blogspot.com/feeds/posts/default?alt=json&max-results=500"
OUT_DIR = "blog"
SITE_ROOT = "https://merahi-village.github.io"

HEADER_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Merahi Village</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:image" content="https://merahi-village.github.io/images/logo_merahi.webp">
<meta property="og:type" content="article">
<meta name="theme-color" content="#014421">
<meta name="robots" content="index, follow">
<meta name="author" content="Merahi Village">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="../assets/css/site.css">
</head>
<body>

<header class="site-header">
  <div class="site-header-inner">
    <a class="brand" href="../index.html">
      <img src="https://merahi-village.github.io/images/logo_merahi.webp" alt="Merahi Village Logo">
      <div class="brand-text"><div class="name">Merahi Village</div><div class="tagline">Our Village, Our Identity</div></div>
    </a>
    <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false" id="navToggle">☰</button>
    <nav class="main-nav" id="mainNav">
      <a href="../index.html">Home</a>
      <a href="../about-village.html">About Village</a>
      <a href="../places.html">Places</a>
      <a href="../gallery.html">Gallery</a>
      <a href="../videos.html">Videos</a>
      <a href="../weather.html">Weather</a>
      <a href="../contact-us.html">Contact</a>
    </nav>
  </div>
</header>
"""

FOOTER_HTML = """
<footer class="site-footer">
  <div class="footer-inner">
    <div>
      <img class="flogo" src="https://merahi-village.github.io/images/merahi_footer_logo.png" alt="Merahi Village Logo">
      <p>Merahi is a medium-sized, rural village located in the Hasanpura block of the Siwan district in
        Bihar, India. Primarily an agricultural community, it spans about 258.8 hectares and is home to
        nearly 1,830 residents.</p>
      <div class="social-row">
        <a href="https://youtube.com/@MerahiVillage" target="_blank" rel="noopener"><img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/youtube.svg" alt="YouTube"></a>
        <a href="https://facebook.com/MerahiVillage" target="_blank" rel="noopener"><img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/facebook.svg" alt="Facebook"></a>
        <a href="https://instagram.com/merahivillage" target="_blank" rel="noopener"><img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/instagram.svg" alt="Instagram"></a>
        <a href="https://x.com/MerahiVillage" target="_blank" rel="noopener"><img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/x.svg" alt="X"></a>
        <a href="https://www.whatsapp.com/channel/0029Va9eb2oHltY80uxqWP1q" target="_blank" rel="noopener"><img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/whatsapp.svg" alt="WhatsApp"></a>
      </div>
    </div>
    <div>
      <h4>Quick Links</h4>
      <ul>
        <li><a href="../index.html">Home</a></li>
        <li><a href="../about-village.html">About Village</a></li>
        <li><a href="../contact-us.html">Contact Us</a></li>
        <li><a href="../sitemap.html">Sitemap</a></li>
      </ul>
    </div>
    <div>
      <h4>Discover</h4>
      <ul>
        <li><a href="../places.html">Explore Places</a></li>
        <li><a href="../gallery.html">Gallery</a></li>
        <li><a href="../videos.html">Videos</a></li>
        <li><a href="../weather.html">Weather</a></li>
        <li><a href="index.html">Blog</a></li>
      </ul>
    </div>
    <div>
      <h4>Information</h4>
      <ul>
        <li><a href="../policies.html#privacy">Privacy Policy</a></li>
        <li><a href="../policies.html#terms">Terms &amp; Conditions</a></li>
        <li><a href="../policies.html#disclaimer">Disclaimer</a></li>
        <li><a href="../faqs.html">FAQs</a></li>
      </ul>
    </div>
    <div>
      <h4>Contact</h4>
      <p>Merahi Village Community<br>Merahi, Hasanpura, Siwan, Bihar, India - 841240<br>merahivillage@gmail.com</p>
    </div>
  </div>
  <div class="footer-divider">
    <span class="fd-line"></span>
<span class="fd-icon" aria-hidden="true">🌾</span>
    <span class="fd-line"></span>
  </div>
  <div class="footer-bottom-text">
    © 2026 Merahi Village, All Rights Reserved. • Managed by <a href="https://gitesh-sharma.github.io/en/org/" target="_blank" rel="noopener">Sharmaji Technology Media</a> • Hosted on <a href="https://pages.github.com/" target="_blank" rel="noopener">GitHub Pages</a>
  </div>
  <p class="footer-disclaimer">This website is an independent, non-governmental informational platform. It is not affiliated with, endorsed by, or operated by any government body, political party, political candidate, or government department. All data is based on Office of the Registrar General &amp; Census Commissioner, Ministry of Home Affairs, Government of India, Open Government Data Platform India, News Sources and other local communities.</p>
</footer>
<script src="../assets/js/site.js"></script>
</body>
</html>
"""


def sanitize_embeds(content_html):
    """
    Finds YouTube / Instagram / X (Twitter) / Facebook embeds inside a
    Blogger post's HTML, removes the actual embed (iframe/blockquote/script),
    and replaces each with a single plain link line instead. Everything else
    in the post (text, images, formatting) is left untouched.
    """
    soup = BeautifulSoup(content_html, 'html.parser')
    replacements = []

    for iframe in soup.find_all('iframe'):
        src = iframe.get('src', '')
        m = re.search(r'(?:youtube\.com/embed/|youtu\.be/)([A-Za-z0-9_-]{6,})', src)
        if m:
            url = f'https://www.youtube.com/watch?v={m.group(1)}'
            link_p = soup.new_tag('p')
            link_p.append('📺 ')
            a = soup.new_tag('a', href=url)
            a.string = 'Watch on YouTube'
            link_p.append(a)
            replacements.append((iframe, link_p))
            continue

        if 'facebook.com/plugins' in src:
            m2 = re.search(r'[?&]href=([^&]+)', src)
            if m2:
                url = urllib.parse.unquote(m2.group(1))
                link_p = soup.new_tag('p')
                link_p.append('👍 ')
                a = soup.new_tag('a', href=url)
                a.string = 'View on Facebook'
                link_p.append(a)
                replacements.append((iframe, link_p))

    for bq in soup.find_all('blockquote', class_='instagram-media'):
        url = bq.get('data-instgrm-permalink', '').split('?')[0]
        if url:
            link_p = soup.new_tag('p')
            link_p.append('📷 ')
            a = soup.new_tag('a', href=url)
            a.string = 'View on Instagram'
            link_p.append(a)
            replacements.append((bq, link_p))

    for bq in soup.find_all('blockquote', class_='twitter-tweet'):
        tweet_url = None
        for a_tag in bq.find_all('a', href=True):
            if re.search(r'(twitter\.com|x\.com)/.+/status/\d+', a_tag['href']):
                tweet_url = a_tag['href'].split('?')[0]
        if tweet_url:
            link_p = soup.new_tag('p')
            link_p.append('🐦 ')
            a = soup.new_tag('a', href=tweet_url)
            a.string = 'View on X'
            link_p.append(a)
            replacements.append((bq, link_p))

    for div in soup.find_all('div', class_='fb-post'):
        url = div.get('data-href', '')
        if url:
            link_p = soup.new_tag('p')
            link_p.append('👍 ')
            a = soup.new_tag('a', href=url)
            a.string = 'View on Facebook'
            link_p.append(a)
            replacements.append((div, link_p))

    for old_tag, new_tag in replacements:
        old_tag.replace_with(new_tag)

    sdk_patterns = ('instagram.com/embed.js', 'platform.twitter.com/widgets.js', 'connect.facebook.net')
    for script in soup.find_all('script'):
        src = script.get('src', '')
        if any(p in src for p in sdk_patterns):
            script.decompose()
    for div in soup.find_all('div', id='fb-root'):
        div.decompose()

    return str(soup)


def slugify_from_url(url):
    path = url.rstrip('/').split('/')[-1]
    slug = path.replace('.html', '')
    slug = re.sub(r'[^a-z0-9\-]', '-', slug.lower())
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug or 'post'


def strip_html_for_description(html_text, length=160):
    text = re.sub('<[^<]+?>', '', html_text)
    text = re.sub(r'\s+', ' ', text).strip()
    return (text[:length].rsplit(' ', 1)[0] + '…') if len(text) > length else text


def fetch_feed():
    req = urllib.request.Request(FEED_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    return data.get('feed', {}).get('entry', [])


def build_post_page(title, content_html, canonical, description, crumb_title, pub_date_str):
    page = HEADER_TMPL.format(title=escape(title), description=escape(description), canonical=canonical)
    page += f'''
<section class="hero" style="background-image:linear-gradient(160deg, rgba(1,68,33,.90), rgba(11,92,51,.82)), url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1600&auto=format&fit=crop');">
  <div class="hero-inner">
    <div class="crumb"><a href="../index.html">Home</a> / <a href="index.html">Blog</a> / {escape(crumb_title)}</div>
    <div class="eyebrow">{escape(pub_date_str)}</div>
    <h1 style="font-size:2rem;">{escape(title)}</h1>
  </div>
</section>

<main class="content" style="padding-top:40px;">
  <section class="block">
    <div class="blog-post-body">
{content_html}
    </div>
    <p style="margin-top:30px;"><a href="index.html" class="btn btn-solid">← Back to Blog</a></p>
  </section>
</main>
'''
    page += FOOTER_HTML
    return page


def write_index(posts):
    cards = ""
    for p in posts:
        cards += f'''
      <a class="place-card" href="{p['slug']}.html">
        <div class="pc-body">
          <div class="pc-tag">{escape(p['date_str'])}</div>
          <h3>{escape(p['title'])}</h3>
          <p>{escape(p['description'])}</p>
        </div>
      </a>'''

    page = HEADER_TMPL.format(
        title="Blog",
        description="Stories and updates from Merahi Village.",
        canonical=f"{SITE_ROOT}/blog/index.html",
    )
    page += f'''
<section class="hero" style="background-image:linear-gradient(160deg, rgba(1,68,33,.90), rgba(11,92,51,.82)), url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1600&auto=format&fit=crop');">
  <div class="hero-inner">
    <div class="crumb"><a href="../index.html">Home</a> / Blog</div>
    <div class="eyebrow">Stories From The Village</div>
    <h1>Blog</h1>
    <p class="lede">Updates, stories and news from Merahi — posted from our Blogger account and mirrored here automatically.</p>
  </div>
</section>

<main class="content" style="padding-top:40px;">
  <section class="block">
    <div class="card-grid">{cards}
    </div>
  </section>
</main>
'''
    page += FOOTER_HTML
    with open(os.path.join(OUT_DIR, "index.html"), 'w', encoding='utf-8') as f:
        f.write(page)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    entries = fetch_feed()
    posts = []

    for entry in entries:
        title = entry.get('title', {}).get('$t', 'Untitled')
        content_html = entry.get('content', {}).get('$t', '')
        published = entry.get('published', {}).get('$t', '')
        try:
            pub_date = datetime.strptime(published[:19], '%Y-%m-%dT%H:%M:%S')
        except Exception:
            pub_date = datetime.now()

        alt_link = next((l['href'] for l in entry.get('link', []) if l.get('rel') == 'alternate'), None)
        if not alt_link:
            continue

        content_html = sanitize_embeds(content_html)
        slug = slugify_from_url(alt_link)
        description = strip_html_for_description(content_html)
        date_str = pub_date.strftime('%d %B %Y')
        canonical = f"{SITE_ROOT}/blog/{slug}.html"

        page = build_post_page(title, content_html, canonical, description, title, date_str)
        with open(os.path.join(OUT_DIR, f"{slug}.html"), 'w', encoding='utf-8') as f:
            f.write(page)

        posts.append({'title': title, 'slug': slug, 'date': pub_date, 'date_str': date_str, 'description': description})

    posts.sort(key=lambda p: p['date'], reverse=True)
    write_index(posts)
    print(f"Synced {len(posts)} post(s) into {OUT_DIR}/")


if __name__ == "__main__":
    main()
