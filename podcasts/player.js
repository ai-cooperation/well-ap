/**
 * WELL AP 通勤 Podcast — global bottom player.
 * Ported from sustainability-100 podcast-player.js (vanilla, no deps).
 *
 * - Reads a global PLAYLIST array: [{ n, id, title, dur, url, zh, en }]
 * - Fixed bottom bar: play/pause, prev/next, seek, speed, close
 * - Auto-play next, resume position (localStorage), Media Session (lock screen)
 * - Syncs episode cards (.ep-card[data-ep]) highlight + play/pause icon
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'wellap-pod';
  var SAVE_INTERVAL = 5;

  var el = {};
  var audio;
  var state = { idx: -1, pos: 0, rate: 1, ts: 0 };
  var lastSaveTime = 0;
  var resumeBanner = null;

  function init() {
    if (typeof PLAYLIST === 'undefined' || !PLAYLIST.length) return;
    el.gp = document.getElementById('gp');
    audio = document.getElementById('gp-audio');
    el.play = document.getElementById('gp-play');
    el.prev = document.getElementById('gp-prev');
    el.next = document.getElementById('gp-next');
    el.title = document.getElementById('gp-title');
    el.cur = document.getElementById('gp-cur');
    el.dur = document.getElementById('gp-dur');
    el.progress = document.getElementById('gp-progress');
    el.fill = document.getElementById('gp-progress-fill');
    el.speed = document.getElementById('gp-speed');
    el.close = document.getElementById('gp-close');
    if (!audio || !el.gp) return;
    bindEvents();
    restoreState();
  }

  function bindEvents() {
    el.play.addEventListener('click', togglePlay);
    el.prev.addEventListener('click', prevEpisode);
    el.next.addEventListener('click', nextEpisode);
    el.close.addEventListener('click', closePlayer);

    el.speed.addEventListener('change', function () {
      state.rate = parseFloat(this.value);
      audio.playbackRate = state.rate;
      saveState();
    });

    el.progress.addEventListener('click', function (e) {
      if (!audio.duration) return;
      var rect = el.progress.getBoundingClientRect();
      var pct = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
      audio.currentTime = pct * audio.duration;
    });

    audio.addEventListener('timeupdate', onTimeUpdate);
    audio.addEventListener('loadedmetadata', function () {
      el.dur.textContent = fmtTime(audio.duration);
      updateMediaPosition();
    });
    audio.addEventListener('ended', onEnded);
    audio.addEventListener('play', function () {
      showPlayIcon(false); updateCards(); updateMediaSession();
    });
    audio.addEventListener('pause', function () {
      showPlayIcon(true); updateCards(); saveState();
    });

    window.addEventListener('beforeunload', saveState);
  }

  function srcFor(ep) { return ep.zh || ep.en || ep.url; }

  function loadEpisode(idx, startPos) {
    if (idx < 0 || idx >= PLAYLIST.length) return;
    var ep = PLAYLIST[idx];
    var src = srcFor(ep);
    if (!src) return;
    state.idx = idx;
    state.pos = startPos || 0;
    audio.src = src;
    audio.playbackRate = state.rate;
    if (startPos) audio.currentTime = startPos;
    el.title.textContent = ep.id + '  ' + ep.title;
    el.title.href = '#' + ep.id;
    el.cur.textContent = fmtTime(state.pos);
    el.dur.textContent = ep.dur || '0:00';
    el.fill.style.width = '0%';
    showPlayer();
    updateCards();
    updateMediaSession();
    saveState();
  }

  function playEpisode(idx) {
    loadEpisode(idx, 0);
    audio.play().catch(function () {});
  }

  function togglePlay() {
    if (state.idx < 0) { playEpisode(0); return; }
    if (audio.paused) audio.play().catch(function () {});
    else audio.pause();
  }

  function nextEpisode() {
    if (state.idx + 1 < PLAYLIST.length) playEpisode(state.idx + 1);
  }

  function prevEpisode() {
    if (audio.currentTime > 3) { audio.currentTime = 0; return; }
    if (state.idx - 1 >= 0) playEpisode(state.idx - 1);
  }

  function onEnded() {
    if (state.idx + 1 < PLAYLIST.length) playEpisode(state.idx + 1);
    else { showPlayIcon(true); updateCards(); saveState(); }
  }

  function onTimeUpdate() {
    if (!audio.duration) return;
    el.fill.style.width = (audio.currentTime / audio.duration) * 100 + '%';
    el.cur.textContent = fmtTime(audio.currentTime);
    state.pos = audio.currentTime;
    var now = Date.now() / 1000;
    if (now - lastSaveTime > SAVE_INTERVAL) {
      lastSaveTime = now; saveState(); updateMediaPosition();
    }
  }

  function showPlayer() {
    el.gp.classList.remove('gp--hidden');
    document.body.classList.add('gp-active');
    if (resumeBanner) { resumeBanner.remove(); resumeBanner = null; }
  }

  function closePlayer() {
    audio.pause();
    el.gp.classList.add('gp--hidden');
    document.body.classList.remove('gp-active');
    saveState();
  }

  function showPlayIcon(showPlay) {
    el.play.querySelector('.gp-icon-play').style.display = showPlay ? '' : 'none';
    el.play.querySelector('.gp-icon-pause').style.display = showPlay ? 'none' : '';
  }

  /* Sync episode cards: highlight current + toggle its play/pause icon */
  function updateCards() {
    var curId = state.idx >= 0 ? PLAYLIST[state.idx].id : null;
    var playing = curId && audio && !audio.paused;
    document.querySelectorAll('.ep-card').forEach(function (card) {
      var isCur = card.dataset.ep === curId;
      card.classList.toggle('playing', !!(isCur && playing));
    });
  }

  function updateMediaSession() {
    if (!('mediaSession' in navigator)) return;
    var ep = PLAYLIST[state.idx];
    if (!ep) return;
    navigator.mediaSession.metadata = new MediaMetadata({
      title: ep.id + ' ' + ep.title,
      artist: 'WELL AP 通勤複習',
      album: 'WELL AP 健康建築認證'
    });
    navigator.mediaSession.setActionHandler('play', function () { audio.play(); });
    navigator.mediaSession.setActionHandler('pause', function () { audio.pause(); });
    navigator.mediaSession.setActionHandler('previoustrack', prevEpisode);
    navigator.mediaSession.setActionHandler('nexttrack', nextEpisode);
    navigator.mediaSession.setActionHandler('seekbackward', function (d) {
      audio.currentTime = Math.max(audio.currentTime - (d.seekOffset || 10), 0);
    });
    navigator.mediaSession.setActionHandler('seekforward', function (d) {
      audio.currentTime = Math.min(audio.currentTime + (d.seekOffset || 30), audio.duration || 0);
    });
  }

  function updateMediaPosition() {
    if (!('mediaSession' in navigator) || !audio.duration) return;
    try {
      navigator.mediaSession.setPositionState({
        duration: audio.duration, playbackRate: audio.playbackRate, position: audio.currentTime
      });
    } catch (e) {}
  }

  function saveState() {
    if (state.idx < 0) return;
    try {
      state.ts = Math.floor(Date.now() / 1000);
      state.pos = audio.currentTime || state.pos;
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (e) {}
  }

  function restoreState() {
    try {
      var saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
      if (!saved || saved.idx == null || saved.idx < 0 || saved.idx >= PLAYLIST.length) return;
      state.idx = saved.idx; state.pos = saved.pos || 0; state.rate = saved.rate || 1;
      el.speed.value = String(state.rate);
      var ep = PLAYLIST[state.idx];
      if (!ep) return;
      showResumeBanner(ep, timeSince(saved.ts));
    } catch (e) {}
  }

  function showResumeBanner(ep, ago) {
    resumeBanner = document.createElement('div');
    resumeBanner.className = 'gp-resume';
    resumeBanner.innerHTML = '<strong>繼續收聽</strong> ' + ep.id + ' ' + ep.title +
      (ago ? ' <span style="opacity:.7">(' + ago + ')</span>' : '') + ' <span style="opacity:.7">▶</span>';
    resumeBanner.addEventListener('click', function () {
      loadEpisode(state.idx, state.pos);
      audio.play().catch(function () {});
      resumeBanner.remove(); resumeBanner = null;
    });
    document.body.appendChild(resumeBanner);
    document.body.classList.add('gp-active');
  }

  function fmtTime(s) {
    if (!s || isNaN(s)) return '0:00';
    var m = Math.floor(s / 60), sec = Math.floor(s % 60);
    return m + ':' + (sec < 10 ? '0' : '') + sec;
  }
  function timeSince(ts) {
    if (!ts) return '';
    var d = Math.floor(Date.now() / 1000) - ts;
    if (d < 60) return '剛才';
    if (d < 3600) return Math.floor(d / 60) + ' 分鐘前';
    if (d < 86400) return Math.floor(d / 3600) + ' 小時前';
    return Math.floor(d / 86400) + ' 天前';
  }

  /* Public API — episode cards call PodcastPlayer.play('M01') */
  window.PodcastPlayer = {
    play: function (epId) {
      for (var i = 0; i < PLAYLIST.length; i++) {
        if (PLAYLIST[i].id === epId) {
          if (state.idx === i) togglePlay();   // same card → toggle
          else playEpisode(i);
          return;
        }
      }
    },
    toggle: togglePlay
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
