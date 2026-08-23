/* ==========================================================================
   Merahi Village — Shared Site Script
   One file, included on every page. Every block below checks that its
   elements exist before running, so the same file is safe everywhere.
   ========================================================================== */
document.addEventListener('DOMContentLoaded', function () {

  /* ---------- Nav toggle (every page) ---------- */
  var navToggle = document.getElementById('navToggle');
  var mainNav = document.getElementById('mainNav');
  if (navToggle && mainNav) {
    navToggle.addEventListener('click', function () {
      var expanded = mainNav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', expanded);
    });
  }

  /* ---------- Photo gallery carousel (index.html) ---------- */
  var track = document.getElementById('carouselTrack');
  if (track) {
    var slides = track.children;
    var dotsWrap = document.getElementById('carouselDots');
    var idx = 0;
    for (var i = 0; i < slides.length; i++) {
      var d = document.createElement('button');
      if (i === 0) d.className = 'active';
      d.setAttribute('aria-label', 'Go to photo ' + (i + 1));
      d.addEventListener('click', (function (n) { return function () { go(n); }; })(i));
      dotsWrap.appendChild(d);
    }
    function go(n) {
      idx = (n + slides.length) % slides.length;
      track.style.transform = 'translateX(-' + (idx * 100) + '%)';
      var dots = dotsWrap.children;
      for (var j = 0; j < dots.length; j++) { dots[j].className = (j === idx) ? 'active' : ''; }
    }
    document.getElementById('carPrev').addEventListener('click', function () { go(idx - 1); });
    document.getElementById('carNext').addEventListener('click', function () { go(idx + 1); });
    var timer = setInterval(function () { go(idx + 1); }, 4500);
    var car = document.getElementById('galleryCarousel');
    car.addEventListener('mouseenter', function () { clearInterval(timer); });
    car.addEventListener('mouseleave', function () { timer = setInterval(function () { go(idx + 1); }, 4500); });
  }

  /* ---------- Places card slider (index.html) ---------- */
  var placesRow = document.getElementById('placesSlider');
  if (placesRow) {
    var slidePrev = document.getElementById('slidePrev');
    var slideNext = document.getElementById('slideNext');
    if (slidePrev) slidePrev.addEventListener('click', function () { placesRow.scrollBy({ left: -290, behavior: 'smooth' }); });
    if (slideNext) slideNext.addEventListener('click', function () { placesRow.scrollBy({ left: 290, behavior: 'smooth' }); });
  }

  /* ---------- Weather dashboard (weather.html) ---------- */
  var weatherNow = document.getElementById('weatherNow');
  if (weatherNow) {
    var LAT = 26.422, LON = 84.241;
    var WMO = {
      0: ['☀️', 'Clear sky'], 1: ['🌤️', 'Mainly clear'], 2: ['⛅', 'Partly cloudy'], 3: ['☁️', 'Overcast'],
      45: ['🌫️', 'Fog'], 48: ['🌫️', 'Rime fog'],
      51: ['🌦️', 'Light drizzle'], 53: ['🌦️', 'Moderate drizzle'], 55: ['🌧️', 'Dense drizzle'],
      56: ['🌧️', 'Light freezing drizzle'], 57: ['🌧️', 'Dense freezing drizzle'],
      61: ['🌧️', 'Slight rain'], 63: ['🌧️', 'Moderate rain'], 65: ['🌧️', 'Heavy rain'],
      66: ['🌧️', 'Light freezing rain'], 67: ['🌧️', 'Heavy freezing rain'],
      71: ['🌨️', 'Slight snow'], 73: ['🌨️', 'Moderate snow'], 75: ['❄️', 'Heavy snow'], 77: ['❄️', 'Snow grains'],
      80: ['🌦️', 'Slight showers'], 81: ['🌧️', 'Moderate showers'], 82: ['⛈️', 'Violent showers'],
      85: ['🌨️', 'Slight snow showers'], 86: ['❄️', 'Heavy snow showers'],
      95: ['⛈️', 'Thunderstorm'], 96: ['⛈️', 'Thunderstorm, hail'], 99: ['⛈️', 'Thunderstorm, heavy hail']
    };
    function wInfo(code) { return WMO[code] || ['🌡️', '—']; }
    function fmtDay(dateStr, i, todayIdx) {
      if (i === todayIdx) return 'Today';
      var d = new Date(dateStr + 'T00:00:00');
      var day = d.toLocaleDateString('en-IN', { weekday: 'short' });
      var date = d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short' });
      return day + '<br>' + date;
    }
    function renderCurrent(cur) {
      var info = wInfo(cur.weather_code);
      document.getElementById('wIcon').textContent = info[0];
      document.getElementById('wTemp').textContent = Math.round(cur.temperature_2m) + '°C';
      document.getElementById('wDesc').textContent = info[1];
      document.getElementById('wFeels').textContent = Math.round(cur.apparent_temperature) + '°C';
      document.getElementById('wHumidity').textContent = Math.round(cur.relative_humidity_2m) + '%';
      document.getElementById('wWind').textContent = Math.round(cur.wind_speed_10m) + ' km/h';
      document.getElementById('wPressure').textContent = Math.round(cur.surface_pressure) + ' hPa';
      var t = new Date(cur.time);
      document.getElementById('wUpdated').textContent = 'Updated ' + t.toLocaleString('en-IN', { hour: '2-digit', minute: '2-digit', day: 'numeric', month: 'short' });
    }
    function renderDaily(daily) {
      var n = daily.time.length;
      var todayIdx = n - 7;
      var pastStrip = document.getElementById('pastStrip');
      var futureStrip = document.getElementById('futureStrip');
      pastStrip.innerHTML = '';
      futureStrip.innerHTML = '';
      for (var i = 0; i < n; i++) {
        var info = wInfo(daily.weather_code[i]);
        var card = document.createElement('div');
        card.className = 'fcard';
        card.innerHTML =
          '<div class="day">' + fmtDay(daily.time[i], i, todayIdx) + '</div>' +
          '<div class="ic">' + info[0] + '</div>' +
          '<div class="hi">' + Math.round(daily.temperature_2m_max[i]) + '°</div>' +
          '<div class="lo">' + Math.round(daily.temperature_2m_min[i]) + '°</div>';
        if (i < todayIdx) { pastStrip.appendChild(card); } else { futureStrip.appendChild(card); }
      }
    }
    (async function loadWeather() {
      var statusEl = document.getElementById('wStatus');
      try {
        var url = 'https://api.open-meteo.com/v1/forecast?latitude=' + LAT + '&longitude=' + LON +
          '&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m,surface_pressure' +
          '&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max' +
          '&past_days=7&forecast_days=7&timezone=Asia%2FKolkata';
        var res = await fetch(url);
        if (!res.ok) throw new Error('Weather service returned ' + res.status);
        var data = await res.json();
        renderCurrent(data.current);
        renderDaily(data.daily);
        statusEl.style.display = 'none';
      } catch (err) {
        statusEl.textContent = 'Could not load live weather right now — please refresh this page in a moment.';
        statusEl.classList.add('err');
        statusEl.style.display = 'block';
        document.getElementById('wDesc').textContent = 'Live data unavailable';
        console.error(err);
      }
    })();
  }

  /* ---------- Contact form → Google Form (contact-us.html) ---------- */
  var contactForm = document.getElementById('contactForm');
  var hiddenIframe = document.getElementById('hidden_iframe');
  var formCard = document.getElementById('formCard');
  var formSuccess = document.getElementById('formSuccess');
  if (contactForm && hiddenIframe && formSuccess) {
    var submitted = false;
    contactForm.addEventListener('submit', function () {
      submitted = true; // native submission proceeds, targeting the hidden iframe
    });
    hiddenIframe.addEventListener('load', function () {
      if (submitted) {
        submitted = false;
        if (formCard) formCard.style.display = 'none';
        formSuccess.style.display = 'block';
      }
    });
  }

});

  /* ---------- Video shelves — Shorts & Playlists (videos.html) ---------- */
  function wireShelf(rowId, prevId, nextId, amount) {
    var row = document.getElementById(rowId);
    if (!row) return;
    var prevBtn = document.getElementById(prevId), nextBtn = document.getElementById(nextId);
    if (prevBtn) prevBtn.addEventListener('click', function () { row.scrollBy({ left: -amount, behavior: 'smooth' }); });
    if (nextBtn) nextBtn.addEventListener('click', function () { row.scrollBy({ left: amount, behavior: 'smooth' }); });
  }
  wireShelf('shortsRow', 'shortsPrev', 'shortsNext', 190);
  wireShelf('playlistRow', 'playlistPrev', 'playlistNext', 340);
