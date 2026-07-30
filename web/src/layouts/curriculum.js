/* Curriculum widget.
 *
 * Loads /curriculum/curriculum.json (built by
 * pipeline/scripts/build_curriculum.py) and renders a 6-column grid of
 * subjects -> sections -> topics. Clicking a topic drills into a single
 * view that fetches the raw markdown files for that topic's tables from
 * GitHub raw, renders them with marked + KaTeX, and provides breadcrumb
 * and prev/next navigation within the same section.
 *
 * Row highlighting is applied at runtime from each table entry's
 * `highlighted_rows` array (data-row indices, skipping the header row)
 * rather than being baked into the curriculum markdown.
 */
(function () {
  var widget = document.getElementById('curriculum-widget');
  if (!widget) return;

  var RAW_BASE = 'https://vivianweidai.com/curriculum/source/';
  var MANIFEST_URL = '/curriculum/curriculum.json';

  // Short slug for chip styling (.chip.bio, .chip.math, …). Folder names
  // and hash slugs use the full word; chips need the abbreviated tone.
  var SHORT_SLUGS = {
    mathematics: 'math', computing: 'comp', physics: 'phys',
    chemistry: 'chem', biology: 'bio', astronomy: 'astro',
  };
  // Canonical subject order for cross-topic navigation. Matches the
  // research and curriculum chip palette order; lets prev/next on the last
  // topic of (e.g.) Astronomy cycle into the first topic of Mathematics.
  var SUBJECT_ORDER = ['mathematics', 'computing', 'physics', 'chemistry', 'biology', 'astronomy'];

  // Find the topic immediately before/after (subject, sectionIdx, topicIdx)
  // in the canonical subject → section → topic walk. Returns null if at
  // the very start / end of the curriculum (no further wrap).
  function findAdjacent(subject, sectionIdx, topicIdx, direction) {
    var subj = manifest[subject];
    if (!subj) return null;
    var sec = subj.sections[sectionIdx];
    var newTopicIdx = topicIdx + direction;
    if (newTopicIdx >= 0 && newTopicIdx < sec.topics.length) {
      return { subject: subject, sectionIdx: sectionIdx, topicIdx: newTopicIdx };
    }
    var newSectionIdx = sectionIdx + direction;
    if (newSectionIdx >= 0 && newSectionIdx < subj.sections.length) {
      var newSec = subj.sections[newSectionIdx];
      return {
        subject: subject,
        sectionIdx: newSectionIdx,
        topicIdx: direction > 0 ? 0 : newSec.topics.length - 1,
      };
    }
    // Cross subject boundary, wrapping the curriculum so prev on the very
    // first topic loops to the last topic, and next on the very last
    // topic loops to the first.
    var subjectIdx = SUBJECT_ORDER.indexOf(subject);
    var N = SUBJECT_ORDER.length;
    for (var step = 1; step <= N; step++) {
      var nextIdx = ((subjectIdx + direction * step) % N + N) % N;
      var newSubject = SUBJECT_ORDER[nextIdx];
      var newSubj = manifest[newSubject];
      if (newSubj && newSubj.sections.length) {
        if (direction > 0) {
          return { subject: newSubject, sectionIdx: 0, topicIdx: 0 };
        }
        var lastSec = newSubj.sections[newSubj.sections.length - 1];
        return {
          subject: newSubject,
          sectionIdx: newSubj.sections.length - 1,
          topicIdx: lastSec.topics.length - 1,
        };
      }
    }
    return null;
  }

  var manifest = null;
  var pendingHash = parseHash();
  var state = { view: 'grid' };
  // Fade-in only fires on the first render after a hard load. All
  // in-page transitions (grid ↔ topic, topic ↔ topic) skip the
  // animation per user feedback — animated reflow on every click was
  // distracting once you were already on the page.
  var hasRendered = false;
  // Topic body cache + render token. Topic→topic navigation defers the
  // visual swap until new tables have been fetched, so the user never
  // sees a "Loading…" placeholder followed by a shrink-grow as tables
  // arrive — they see the old card, then atomically the new card. The
  // token lets a fast second arrow press cancel a stale fetch handler
  // before it overwrites the (newer) target topic.
  var topicBodyCache = {};
  var topicRenderToken = 0;

  widget.classList.add('curr-widget');
  widget.innerHTML = '<div class="curr-loading">Loading curriculum…</div>';

  // Keyboard shortcuts on the topic view: ← → cycle through adjacent
  // topics, Esc returns to the grid (with the originating section
  // highlighted). No effect on the grid view, and no effect when the
  // user is typing in an input or holding a modifier key.
  document.addEventListener('keydown', function (e) {
    if (state.view !== 'topic' || !manifest) return;
    if (e.metaKey || e.ctrlKey || e.altKey || e.shiftKey) return;
    var t = e.target;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
    if (e.key === 'Escape') {
      e.preventDefault();
      state = {
        view: 'grid',
        highlightSubject: state.subject,
        highlightSectionIdx: state.sectionIdx,
      };
      render();
      return;
    }
    var direction = 0;
    if (e.key === 'ArrowLeft') direction = -1;
    else if (e.key === 'ArrowRight') direction = 1;
    else return;
    var adj = findAdjacent(state.subject, state.sectionIdx, state.topicIdx, direction);
    if (!adj) return;
    e.preventDefault();
    state = {
      view: 'topic',
      subject: adj.subject,
      sectionIdx: adj.sectionIdx,
      topicIdx: adj.topicIdx,
    };
    render();
  });

  fetch(MANIFEST_URL)
    .then(function (r) { return r.json(); })
    .then(function (m) {
      manifest = m;
      if (pendingHash) state = resolveState(pendingHash);
      pendingHash = null;
      render();
    })
    .catch(function (e) {
      widget.innerHTML = '<div class="curr-loading">Failed to load curriculum: ' + e + '</div>';
    });

  window.addEventListener('popstate', function () {
    var raw = parseHash();
    state = raw && manifest ? resolveState(raw) : (raw || { view: 'grid' });
    if (manifest) render();
  });

  function pushState() {
    var hash = '#';
    if (state.view === 'grid' && state.highlightSubject) {
      hash += state.highlightSubject;
      if (state.highlightSectionIdx != null) {
        var hsec = manifest[state.highlightSubject].sections[state.highlightSectionIdx];
        hash += '/' + slugify(hsec.name);
      }
    } else if (state.view === 'topic') {
      var sec2 = manifest[state.subject].sections[state.sectionIdx];
      var topic = sec2.topics[state.topicIdx];
      hash += state.subject + '/' + slugify(sec2.name) + '/' + slugify(topic.name);
    } else hash = '#';
    if (location.hash !== hash) history.pushState(null, '', hash);
  }

  /* parseHash returns RAW slug-or-number tokens. Numeric → index lookup;
     slug → name match. Resolved into actual indices by resolveState once
     the manifest has loaded.
     - 1 part:  grid view with that subject's column highlighted.
     - 2 parts: grid view with that subject's section highlighted (clicked
                section names land here — same yellow block treatment as
                a single topic, but without leaving the 6-column grid).
     - 3 parts: topic table view (clicked leaf topics land here). */
  function parseHash() {
    var h = location.hash.replace(/^#/, '');
    if (!h) return null;
    var parts = h.split('/').map(decodeURIComponent);
    if (parts.length === 1) return { view: 'grid', subject: parts[0] };
    if (parts.length === 2) return { view: 'grid', subject: parts[0], section: parts[1] };
    if (parts.length === 3) return { view: 'topic', subject: parts[0], section: parts[1], topic: parts[2] };
    return null;
  }

  function resolveState(raw) {
    if (raw.view === 'grid') {
      if (!raw.subject) return { view: 'grid' };
      var subj0 = manifest[raw.subject];
      if (!subj0) return { view: 'grid' };
      if (!raw.section) return { view: 'grid', highlightSubject: raw.subject };
      var hIdx = lookupIdx(subj0.sections, raw.section);
      if (hIdx < 0) return { view: 'grid', highlightSubject: raw.subject };
      return { view: 'grid', highlightSubject: raw.subject, highlightSectionIdx: hIdx };
    }
    var subj = manifest[raw.subject];
    if (!subj) return { view: 'grid' };
    var sectionIdx = lookupIdx(subj.sections, raw.section);
    if (sectionIdx < 0) return { view: 'grid' };
    var topicIdx = lookupIdx(subj.sections[sectionIdx].topics, raw.topic);
    if (topicIdx < 0) return { view: 'grid' };
    return { view: 'topic', subject: raw.subject, sectionIdx: sectionIdx, topicIdx: topicIdx };
  }

  /* Resolve a raw URL token to an index in the given list of {name} objects.
     Pure digits → numeric index (legacy URLs); otherwise slug match. */
  function lookupIdx(list, key) {
    if (/^\d+$/.test(key)) {
      var n = parseInt(key, 10);
      return n >= 0 && n < list.length ? n : -1;
    }
    for (var i = 0; i < list.length; i++) {
      if (slugify(list[i].name) === key) return i;
    }
    return -1;
  }

  function slugify(s) {
    return String(s).toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');
  }

  function render() {
    pushState();
    if (state.view === 'topic') renderTopic();
    else renderGrid();
    hasRendered = true;
  }

  function renderGrid() {
    // If a grid is already mounted, just adjust highlight classes in place
    // — no DOM rebuild, no fade-in replay, listeners stay attached. This
    // covers all in-page navigation between sciences/sections. A full
    // rebuild only happens on first paint or when returning from a topic.
    if (widget.querySelector('.curr-grid')) {
      applyGridHighlights();
      return;
    }

    var subjects = ['mathematics', 'computing', 'physics', 'chemistry', 'biology', 'astronomy'];
    /* `fade-in` is only added on the very first paint. Once each column
       finishes its fadeUp animation we strip the class (see animationend
       listener at the end of this function). Otherwise later class
       toggles like add/remove curr-pulse would force the animation
       cascade to re-evaluate, restarting fadeUp from t=0 — which the
       user sees as the column fading out and back in. */
    var fade = hasRendered ? '' : ' fade-in';
    var html = '<div class="curr-grid">';
    subjects.forEach(function (subjSlug, i) {
      var subj = manifest[subjSlug];
      if (!subj) return;
      // pulse only on click-driven re-renders (after the first paint)
      // so the URL-hash entry doesn't ride two animations at once.
      var pulse = hasRendered ? ' curr-pulse' : '';
      var colHl = state.highlightSubject === subjSlug && state.highlightSectionIdx == null
        ? ' curr-col-highlighted' + pulse : '';
      // Inline animation-delay is only meaningful for the first-render
      // staggered fade-in. On click re-renders (hasRendered = true) we
      // omit it so it doesn't delay the click-pulse animation.
      var delayAttr = hasRendered ? '' : ' style="animation-delay:' + (i * 0.06).toFixed(2) + 's"';
      html += '<div class="curr-col' + fade + colHl + '" data-subj="' + subjSlug + '"' + delayAttr + '>';
      html += '<div class="curr-col-head" data-subj="' + subjSlug + '">' + escapeHtml(subj.name) + '</div>';
      subj.sections.forEach(function (sec, secIdx) {
        var secHl = state.highlightSubject === subjSlug && state.highlightSectionIdx === secIdx
          ? ' curr-section-highlighted' + pulse : '';
        html += '<div class="curr-section' + secHl + '" data-secidx="' + secIdx + '">';
        html += '<div class="curr-section-name" data-subj="' + subjSlug + '" data-sec="' + secIdx + '">' + escapeHtml(sec.name) + '</div>';
        html += '<ul>';
        sec.topics.forEach(function (topic, topicIdx) {
          html += '<li><a href="#" data-subj="' + subjSlug
               + '" data-sec="' + secIdx
               + '" data-topic="' + topicIdx + '">'
               + escapeHtml(topic.name.toLowerCase()) + '</a></li>';
        });
        html += '</ul></div>';
      });
      html += '</div>';
    });
    html += '</div>';
    widget.innerHTML = html;

    widget.querySelectorAll('.curr-section a').forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        state = {
          view: 'topic',
          subject: a.dataset.subj,
          sectionIdx: parseInt(a.dataset.sec, 10),
          topicIdx: parseInt(a.dataset.topic, 10),
        };
        render();
      });
    });

    widget.querySelectorAll('.curr-col-head').forEach(function (h) {
      h.addEventListener('click', function () {
        state = { view: 'grid', highlightSubject: h.dataset.subj };
        render();
      });
    });

    widget.querySelectorAll('.curr-section-name').forEach(function (s) {
      s.addEventListener('click', function () {
        state = {
          view: 'grid',
          highlightSubject: s.dataset.subj,
          highlightSectionIdx: parseInt(s.dataset.sec, 10),
        };
        render();
      });
    });

    /* Strip fade-in (and its inline stagger delay) once the first-paint
       animation finishes on each column. Without this, removing curr-pulse
       later forces the animation cascade to re-evaluate and fadeUp restarts
       from t=0 — visible as a column fade-out-and-in. */
    widget.querySelectorAll('.curr-col.fade-in').forEach(function (el) {
      el.addEventListener('animationend', function done(e) {
        if (e.animationName !== 'fadeUp') return;
        el.classList.remove('fade-in');
        el.style.animationDelay = '';
        el.removeEventListener('animationend', done);
      });
    });

    maybeScrollToHighlight();
  }

  /* In-place highlight swap on an already-mounted grid. Toggles the two
     highlight classes and triggers the section-into-view scroll without
     replacing any nodes — preserves listeners and skips the fade-in.
     Always retrigger the pulse for elements that are in the highlighted
     state (not just on transitions in) so a second click on the same
     header/section gives the same pop-and-down feedback as the first. */
  function applyGridHighlights() {
    widget.querySelectorAll('.curr-col').forEach(function (col) {
      var subjSlug = col.dataset.subj;
      var isCol = state.highlightSubject === subjSlug && state.highlightSectionIdx == null;
      col.classList.toggle('curr-col-highlighted', isCol);
      if (isCol) retriggerPulse(col);
      else col.classList.remove('curr-pulse');
      col.querySelectorAll('.curr-section').forEach(function (sec) {
        var secIdx = parseInt(sec.dataset.secidx, 10);
        var isSec = state.highlightSubject === subjSlug && state.highlightSectionIdx === secIdx;
        sec.classList.toggle('curr-section-highlighted', isSec);
        if (isSec) retriggerPulse(sec);
        else sec.classList.remove('curr-pulse');
      });
    });
    maybeScrollToHighlight();
  }

  /* Remove → force reflow → re-add. The reflow is what makes the browser
     restart the keyframes; without it the no-op toggle gets coalesced and
     the animation doesn't replay. The fade-in cleanup at the end of
     renderGrid has already stripped the inline stagger delay before any
     click can reach this function, so we don't need to clear it here. */
  function retriggerPulse(el) {
    el.classList.remove('curr-pulse');
    void el.offsetWidth;
    el.classList.add('curr-pulse');
  }

  /* Section-level highlight scrolls the yellow block into view so a
     mid-page section isn't off-screen. Column-level highlight does NOT
     auto-scroll — the column already starts at the page top, and
     centering a tall column would push the viewport halfway down.

     Only for in-page clicks. Arriving from an external link (the home
     page's curriculum row) lands on the first render, where hasRendered is
     still false: there we stay at the top of the page so the header and
     the six column titles are visible and the highlight has context. The
     yellow block is easy to spot on the way down. */
  function maybeScrollToHighlight() {
    if (!hasRendered) return;
    if (state.highlightSubject == null || state.highlightSectionIdx == null) return;
    var target = widget.querySelector('.curr-section-highlighted');
    if (!target) return;
    requestAnimationFrame(function () {
      target.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  }

  /* Renders the topic view. The visual swap is split into two phases so
     topic→topic navigation never shows an empty Loading placeholder
     followed by a shrink-grow as tables stream in:

     1. Coming from grid (or first paint with no card yet): build the
        shell immediately with a Loading placeholder, kick off fetches,
        and populate the body once they resolve. Acceptable here because
        the user is transitioning view types, so a brief load state is
        expected.

     2. Topic → topic (a card already exists): keep the OLD card on
        screen, fetch the new tables, then atomically rebuild the whole
        topic with full content. The card-pop-in animation plays exactly
        once on the new card; the prev/next nav and breadcrumb update in
        the same frame as the body. No Loading placeholder, no shrink-
        grow — matches the smoothness of the tech nav's full-page reload.

     A render token guards against a stale fetch from an earlier press
     overwriting the user's latest target after a fast double-tap. */
  function renderTopic() {
    var token = ++topicRenderToken;
    var subj = manifest[state.subject];
    var sec = subj.sections[state.sectionIdx];
    var topic = sec.topics[state.topicIdx];
    var snap = {
      subject: state.subject,
      sectionIdx: state.sectionIdx,
      topicIdx: state.topicIdx,
    };

    var hadCard = !!widget.querySelector('.curr-topic');
    var bodiesPromise = fetchTopicBodies(topic);

    if (!hadCard) {
      mountTopicShell(snap, null);
      bodiesPromise.then(function (bodies) {
        if (token !== topicRenderToken) return;
        populateTopicBody(bodies, topic);
      }).catch(function (e) {
        if (token !== topicRenderToken) return;
        var body = widget.querySelector('.curr-topic-body');
        if (body) body.innerHTML = '<div class="curr-loading">Failed to load topic: ' + e + '</div>';
      });
    } else {
      bodiesPromise.then(function (bodies) {
        if (token !== topicRenderToken) return;
        mountTopicShell(snap, bodies);
      }).catch(function (e) {
        if (token !== topicRenderToken) return;
        mountTopicShell(snap, null);
        var body = widget.querySelector('.curr-topic-body');
        if (body) body.innerHTML = '<div class="curr-loading">Failed to load topic: ' + e + '</div>';
      });
    }
  }

  function fetchTopicBodies(topic) {
    var key = topic.tables.map(function (t) { return t.path; }).join('|');
    if (topicBodyCache[key]) return Promise.resolve(topicBodyCache[key]);
    return Promise.all(topic.tables.map(function (t) {
      return fetch(RAW_BASE + t.path)
        .then(function (r) { return r.text(); })
        .then(stripFrontMatter);
    })).then(function (bodies) {
      topicBodyCache[key] = bodies;
      return bodies;
    });
  }

  /* Build the topic shell (prev/next nav + card with breadcrumb + body)
     and mount it. If `bodies` is provided, the body is populated with
     rendered tables in the same DOM mutation — atomic swap, no Loading
     state. If null, a Loading placeholder is shown instead. */
  function mountTopicShell(snap, bodies) {
    var subj = manifest[snap.subject];
    var sec = subj.sections[snap.sectionIdx];
    var topic = sec.topics[snap.topicIdx];

    var html = '<div class="curr-topic-wrap">';
    html += '<div class="curr-topic card-pop-in" data-subj="' + snap.subject + '">';
    html += '<div class="curr-breadcrumb" data-subj="' + snap.subject + '">'
         + '<span class="curr-breadcrumb-title">' + escapeHtml(topic.name) + '</span>'
         + '<span class="curr-breadcrumb-meta">'
         +   '<a class="chip ' + SHORT_SLUGS[snap.subject] + '" data-action="subject" href="/curriculum/#' + snap.subject + '">' + escapeHtml(subj.name) + '</a>'
         + '</span>'
         + '</div>';
    html += '<div class="curr-topic-body">';
    html += bodies ? '' : '<div class="curr-loading">Loading…</div>';
    html += '</div>';
    html += '</div></div>';
    widget.innerHTML = html;

    if (bodies) populateTopicBody(bodies, topic);
    wireTopicHandlers(snap);
  }

  function populateTopicBody(bodies, topic) {
    var body = widget.querySelector('.curr-topic-body');
    if (!body) return;
    body.innerHTML = '';
    bodies.forEach(function (md, i) {
      var wrap = document.createElement('div');
      wrap.className = 'curr-table-wrap';
      wrap.innerHTML = marked.parse(md);
      applyHighlights(wrap, topic.tables[i].highlighted_rows || []);
      mergeHeaders(wrap);
      mergeFirstColumn(wrap);
      body.appendChild(wrap);
    });
    whenKatexReady(function () {
      window.renderMathInElement(body, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '$',  right: '$',  display: false }
        ],
        throwOnError: false
      });
    });
  }

  function wireTopicHandlers(snap) {
    // Breadcrumb clicks
    widget.querySelector('[data-action="subject"]').addEventListener('click', function (e) {
      e.preventDefault();
      state = { view: 'grid', highlightSubject: snap.subject };
      render();
    });
  }

  function whenKatexReady(cb) {
    if (window.renderMathInElement) return cb();
    var tries = 0;
    var id = setInterval(function () {
      tries += 1;
      if (window.renderMathInElement || tries > 100) {
        clearInterval(id);
        if (window.renderMathInElement) cb();
      }
    }, 50);
  }

  function applyHighlights(container, rowIndices) {
    if (!rowIndices || !rowIndices.length) return;
    var set = {};
    rowIndices.forEach(function (i) { set[i] = true; });
    // The curriculum markdown uses a single <table> per file. Walk its
    // data rows (rows with <td>, i.e. skipping <th> header rows) and
    // add `highlight` to the ones whose data index is in the set.
    var tables = container.querySelectorAll('table');
    tables.forEach(function (table) {
      var rows = table.querySelectorAll('tr');
      var dataIdx = 0;
      rows.forEach(function (tr) {
        if (tr.querySelector('td')) {
          if (set[dataIdx]) tr.classList.add('highlight');
          dataIdx += 1;
        }
      });
    });
  }

  function mergeHeaders(container) {
    // Replace the 3-column header row with a single merged cell
    // using the table name from the h1 above the table.
    var h1 = container.querySelector('h1');
    var table = container.querySelector('table');
    if (!h1 || !table) return;
    var name = h1.textContent.trim();
    var headerRow = table.querySelector('tr');
    if (headerRow && headerRow.querySelector('th')) {
      headerRow.innerHTML = '<th colspan="3">' + escapeHtml(name) + '</th>';
    }
  }

  function mergeFirstColumn(container) {
    var tables = container.querySelectorAll('table');
    tables.forEach(function (table) {
      var rows = table.querySelectorAll('tr');
      var dataRows = [];
      rows.forEach(function (tr) {
        if (tr.querySelector('td')) dataRows.push(tr);
      });
      var i = 0;
      while (i < dataRows.length) {
        var cell = dataRows[i].querySelector('td');
        var label = cell.textContent.trim();
        var span = 1;
        for (var j = i + 1; j < dataRows.length; j++) {
          var next = dataRows[j].querySelector('td');
          if (next.textContent.trim() === label) span++;
          else break;
        }
        if (span > 1) {
          cell.rowSpan = span;
          cell.style.verticalAlign = 'middle';
          if (i + span < dataRows.length) {
            cell.classList.add('curr-group-cell');
          }
          for (var k = i; k < i + span; k++) {
            var row = dataRows[k];
            if (k > i) row.querySelector('td').style.display = 'none';
            (function (groupCell) {
              row.addEventListener('mouseenter', function () { groupCell.classList.add('curr-group-hover'); });
              row.addEventListener('mouseleave', function () { groupCell.classList.remove('curr-group-hover'); });
            })(cell);
          }
        }
        i += span;
      }
    });
  }

  function stripFrontMatter(text) {
    return text.replace(/^---\n[\s\S]*?\n---\n?/, '');
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

})();
