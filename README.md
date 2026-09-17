<div align="center">

<img src="https://merahi-village.github.io/images/logo_merahi.webp" alt="Merahi Village Logo" width="110" />

# 🌾 Merahi Village

**Our Village, Our Identity**

The official community website of Merahi — a farming village in the Hasanpura block of Siwan district, Bihar, India.

[**🌐 Visit Live Site**](https://merahi-village.github.io) · [Places](https://merahi-village.github.io/places.html) · [Weather](https://merahi-village.github.io/weather.html) · [FAQs](https://merahi-village.github.io/faqs.html) · [Contact](https://merahi-village.github.io/contact-us.html)

![Website](https://img.shields.io/website?url=https%3A%2F%2Fmerahi-village.github.io&label=live%20site)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)
![GitHub Pages](https://img.shields.io/badge/Hosted%20on-GitHub%20Pages-222?logo=github)
![No Build Step](https://img.shields.io/badge/build%20step-none-brightgreen)

</div>

---

## 📖 About

Merahi is a village of roughly **1,829 residents** in the Hasanpura block of Siwan district, Bihar, on the Gangetic plains of northern India. This repository is the source for its community website — a place for residents, families and visitors to learn about the village's people, places, governance, culture and everyday life.

It's an **independent, non-governmental, community-run project** — not affiliated with any government body — built and maintained by [Sharmaji Technology Media](https://gitesh-sharma.github.io/en/org/).

## ✨ Features

| | |
|---|---|
| 🏡 **Home** | Hero, village highlights, real-photo gallery carousel, places & videos preview sliders |
| 📖 **About Village** | Geography, demographics, governance, economy, education & culture — Wikipedia-depth, original writing |
| 📍 **8 Place Pages** | Chhath Ghat, Shiv Mandir, Ram Janki Durga Shiv Mandir, Brahma Baba, Maa Kali Mandir, Primary School, Primary Health Centre (Jalalpur), Pakari Panchayat — each with photos, video, and an embedded Google Map |
| 📸 **Gallery** | Every real photo of the village in one browsable grid |
| 🎬 **Videos** | YouTube-channel-style header, live "recently uploaded" feed, scrollable Shorts & Playlists shelves |
| 🌦️ **Weather** | Live dashboard — today's conditions, past 7 days, 7-day forecast (via [Open-Meteo](https://open-meteo.com), no API key) |
| ❓ **FAQs** | 34-question accordion covering everything from population to how to apply for a caste certificate |
| ✉️ **Contact** | Styled form submitting directly to a Google Form — no backend required |
| 📜 **Policies** | Full privacy, data-collection & third-party services disclosure |
| 🗺️ **Sitemap** | Human-readable `sitemap.html` + machine-readable `sitemap.xml` for search engines |
| 🚧 **404 Page** | On-brand "Lost in the Fields?" error page with quick links back |

## 🛠️ Tech Stack

Deliberately simple — **no framework, no bundler, no build step.** Just HTML, CSS and vanilla JS, deployed straight to GitHub Pages.

- **Structure:** Semantic HTML5, one `.html` file per page
- **Styling:** Single shared stylesheet (`assets/css/site.css`) — custom design system, no CSS framework
- **Scripting:** Single shared script (`assets/js/site.js`) — vanilla JS, every feature block guarded so one file is safe across every page
- **Fonts:** [Fraunces](https://fonts.google.com/specimen/Fraunces) (headings) + [Work Sans](https://fonts.google.com/specimen/Work+Sans) (body) + Noto Sans Devanagari, via Google Fonts
- **Live data:** [Open-Meteo](https://open-meteo.com) (weather, free/no-key), YouTube `iframe` embeds, Google Maps embeds
- **Forms:** Google Forms, submitted client-side via a hidden-iframe POST (no backend)
- **SEO:** JSON-LD structured data (`Organization`, `WebSite`, `BreadcrumbList`, `FAQPage`, `HinduTemple`, `School`, `Hospital`, `GovernmentOffice`, `ImageGallery`, `VideoObject`) on every page, plus `sitemap.xml` and `robots.txt`

## 📁 Project Structure

```
merahi-village.github.io/
├── index.html                  # Home
├── about-village.html          # About the village
├── places.html                 # Places index
├── places/
│   ├── chhath-ghat.html
│   ├── shiv-mandir.html
│   ├── ram-janki-durga-shiv-mandir.html
│   ├── brahma-baba.html
│   ├── maa-kali-mandir.html
│   ├── primary-school.html
│   ├── primary-health-center-jalalpur.html
│   └── pakari-panchayat.html
├── gallery.html
├── videos.html
├── weather.html
├── contact-us.html
├── faqs.html
├── policies.html
├── sitemap.html
├── sitemap.xml
├── robots.txt
├── 404.html
└── assets/
    ├── css/
    │   └── site.css            # Shared "GoGreen" design system
    └── js/
        └── site.js              # Shared, feature-guarded vanilla JS
```

## 🎨 Design System — "GoGreen"

A warm, farming-inspired green-and-gold theme, used consistently across every page.

| Token | Value | Use |
|---|---|---|
| `--green` | `#014421` | Header, footer, primary brand color |
| `--green-mid` | `#0b5c33` | Secondary green, hover states |
| `--gold` | `#c99a2e` | Accents, highlights, CTAs |
| `--cream` | `#faf6ee` | Page background |
| Headings | Fraunces (serif) | Warm, editorial feel |
| Body | Work Sans (sans-serif) | Clean, readable |

## 🚀 Getting Started

No build tools needed — this is a static site.

```bash
git clone https://github.com/merahi-village/merahi-village.github.io.git
cd merahi-village.github.io
```

Open `index.html` directly in a browser, or serve it locally so relative links and live embeds behave exactly as they will in production:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## ☁️ Deployment

Hosted on **GitHub Pages**, served automatically from this repository. Push to the default branch and the live site updates within a few minutes — no build step, no CI required for the core site.

## 🔍 SEO & Structured Data

- `sitemap.xml` — submitted to Google Search Console & Bing Webmaster Tools
- `robots.txt` — points crawlers to the sitemap
- Every page carries appropriate [Schema.org](https://schema.org) JSON-LD (Organization/WebSite on the home page, BreadcrumbList everywhere, and content-specific types like `HinduTemple`, `School`, `Hospital`, `GovernmentOffice`, `FAQPage`, `VideoObject` and `ImageGallery` where relevant)
- Open Graph & Twitter Card meta tags on every page for clean social sharing previews

## 🙏 Acknowledgements

- Data sourced from the Office of the Registrar General & Census Commissioner (Government of India), the Open Government Data Platform India, and the local community
- Village photography and video from the [Merahi Village YouTube channel](https://www.youtube.com/@MerahiVillage) and community contributors
- Designed & managed by [Sharmaji Technology Media](https://gitesh-sharma.github.io/en/org/)

## 📬 Contact

- **Email:** merahivillage@gmail.com
- **Merahi Village Blog:** [merahivillage.blogspot.com](https://merahivillage.blogspot.com)
- **YouTube:** [@MerahiVillage](https://www.youtube.com/@MerahiVillage)
- **Instagram:** [@merahivillage](https://instagram.com/merahivillage)
- **Facebook:** [Merahi Village](https://facebook.com/MerahiVillage)
- **X:** [@MerahiVillage](https://x.com/MerahiVillage)

## 📄 License

© 2026 Merahi Village. All rights reserved.

This is an independent, non-governmental informational platform — not affiliated with, endorsed by, or operated by any government body, political party, or political candidate.

---

<div align="center">

Made with 🌾 for Merahi, Hasanpura, Siwan, Bihar — 841240

</div>
