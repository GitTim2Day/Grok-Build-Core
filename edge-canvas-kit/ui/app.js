// app.js -- edge-canvas-kit UI. No external assets, no CDN. Talks only to the server that served it.
// All server/converted text is placed with textContent (never innerHTML).
"use strict";
(function () {
  var $ = function (id) { return document.getElementById(id); };
  var TOKEN = "";
  (function readToken() {
    var m = /(?:^|[#&])token=([A-Za-z0-9_\-]+)/.exec(location.hash || "");
    if (m) { TOKEN = m[1]; try { sessionStorage.setItem("kitToken", TOKEN); } catch (e) {} history.replaceState(null, "", location.pathname + location.search); }
    else { try { TOKEN = sessionStorage.getItem("kitToken") || ""; } catch (e) {} }
  })();

  function api(method, path, body, extraHeaders) {
    var h = { "X-Kit-Client": "1" };
    if (TOKEN) h["X-Kit-Token"] = TOKEN;
    var opt = { method: method, headers: h, cache: "no-store", credentials: "same-origin" };
    if (body !== undefined) {
      if (body instanceof Blob || body instanceof ArrayBuffer) { opt.body = body; h["Content-Type"] = "application/octet-stream"; }
      else { opt.body = JSON.stringify(body); h["Content-Type"] = "application/json"; }
    }
    if (extraHeaders) for (var k in extraHeaders) h[k] = extraHeaders[k];
    return fetch(path, opt).then(function (r) {
      return r.json().catch(function () { return { error: "bad JSON from server" }; }).then(function (j) {
        if (!r.ok) { var e = new Error(j.error || ("HTTP " + r.status)); e.status = r.status; throw e; }
        return j;
      });
    });
  }
  function el(tag, text, cls) { var e = document.createElement(tag); if (text !== undefined && text !== null) e.textContent = String(text); if (cls) e.className = cls; return e; }
  function show(id, v) { $(id).textContent = typeof v === "string" ? v : JSON.stringify(v, null, 1); }

  // ---------------------------------------------------------------- tabs
  Array.prototype.forEach.call(document.querySelectorAll("#tabs button"), function (b) {
    b.addEventListener("click", function () {
      Array.prototype.forEach.call(document.querySelectorAll("#tabs button"), function (x) { x.classList.toggle("on", x === b); });
      Array.prototype.forEach.call(document.querySelectorAll(".tab"), function (t) { t.classList.toggle("on", t.id === "tab-" + b.dataset.tab); });
      if (b.dataset.tab === "files") listDir(cwd);
      if (b.dataset.tab === "status") refreshStatus();
    });
  });

  // ---------------------------------------------------------------- boot + status
  function boot() {
    return api("GET", "/api/boot").then(function (r) {
      $("bootline").textContent = "boot " + (r.ok ? "OK " + r.expect : "NOT OK") + " via " + r.via;
      return r;
    }).catch(function (e) { $("bootline").textContent = "boot: " + e.message; throw e; });
  }
  function refreshStatus() {
    return api("GET", "/api/status").then(function (s) {
      show("stat", s);
      $("badge").textContent = s.mode === "lan" ? "home network" : "offline / this device";
      return s;
    }).catch(function (e) { show("stat", "status error: " + e.message); });
  }
  $("sref").addEventListener("click", refreshStatus);
  $("dgo").addEventListener("click", function () {
    api("POST", "/api/descend", { m: $("dm").value, n: Number($("dn").value), B: $("dB").value, x0: $("dx0").value, dx: $("ddx").value, steps: Number($("dsteps").value) })
      .then(function (r) { $("dres").textContent = " " + r.final; }).catch(function (e) { $("dres").textContent = " " + e.message; });
  });

  // ---------------------------------------------------------------- frame player (hold only while built; show or drop)
  var player = { data: null, run: false, t0: 0, next: 0, shown: 0, dropped: 0, buildMs: 0 };
  var off = document.createElement("canvas");
  function loadFrames() {
    var q = new URLSearchParams({ fps: $("fps").value, frames: $("nframes").value, w: $("fsize").value, h: $("fsize").value,
      m: $("pm").value, n: $("pn").value, B: $("pB").value, x0: $("px0").value, dx: $("pdx").value });
    $("fstats").textContent = "loading...";
    return api("GET", "/api/frames?" + q.toString()).then(function (d) {
      player.data = d; off.width = d.shape[2]; off.height = d.shape[1];
      $("fstats").textContent = d.shape.join("x") + " @ " + d.fps + " fps (dt " + d.dt + "), synthetic";
      return d;
    }).catch(function (e) { $("fstats").textContent = e.message; throw e; });
  }
  function buildFrame(k) {  // the only frame held in memory is the one being built
    var d = player.data, w = d.shape[2], h = d.shape[1];
    var bin = atob(d.frames[k]), img = new ImageData(w, h), px = img.data;
    for (var i = 0, j = 0; i < w * h; i++, j += 3) { px[i * 4] = bin.charCodeAt(j); px[i * 4 + 1] = bin.charCodeAt(j + 1); px[i * 4 + 2] = bin.charCodeAt(j + 2); px[i * 4 + 3] = 255; }
    return img;
  }
  function paint(img) {
    var c = $("player"), ctx = c.getContext("2d");
    off.getContext("2d").putImageData(img, 0, 0);
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(off, 0, 0, c.width, c.height);
  }
  function tick(now) {
    if (!player.run || !player.data) return;
    var d = player.data, period = 1000 / d.fps, n = d.frames.length;
    var due = Math.floor((now - player.t0) / period);
    if (due >= n) {
      if ($("loop").checked) { player.t0 = now; player.next = 0; due = 0; } else { player.run = false; stats(); return; }
    }
    if (due > player.next) { player.dropped += due - player.next; player.next = due; }   // never built in time: dropped
    if (due === player.next) {
      var t = performance.now(), img = buildFrame(due), b = performance.now() - t;
      player.buildMs = player.buildMs * 0.9 + b * 0.1;
      if (performance.now() <= player.t0 + (due + 1) * period) { paint(img); player.shown++; } else { player.dropped++; }
      img = null; player.next = due + 1;
    }
    stats();
    requestAnimationFrame(tick);
  }
  function stats() { $("fstats").textContent = "shown " + player.shown + "  dropped " + player.dropped + "  build " + player.buildMs.toFixed(2) + " ms" + (player.data ? "  @" + player.data.fps + " fps" : ""); }
  $("fload").addEventListener("click", function () { loadFrames(); });
  $("fplay").addEventListener("click", function () {
    var go = function () { player.run = true; player.shown = player.dropped = 0; player.next = 0; player.t0 = performance.now(); requestAnimationFrame(tick); };
    if (!player.data) loadFrames().then(go); else go();
  });
  $("fstop").addEventListener("click", function () { player.run = false; });

  // ---------------------------------------------------------------- drawing pad
  (function pad() {
    var c = $("pad"), ctx = c.getContext("2d"), down = false, last = null;
    ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, c.width, c.height);
    function pos(e) { var r = c.getBoundingClientRect(); return [(e.clientX - r.left) * c.width / r.width, (e.clientY - r.top) * c.height / r.height]; }
    c.addEventListener("pointerdown", function (e) { down = true; last = pos(e); c.setPointerCapture(e.pointerId); });
    c.addEventListener("pointermove", function (e) {
      if (!down) return; var p = pos(e);
      ctx.strokeStyle = $("pcolor").value; ctx.lineWidth = Number($("psize").value); ctx.lineCap = "round";
      ctx.beginPath(); ctx.moveTo(last[0], last[1]); ctx.lineTo(p[0], p[1]); ctx.stroke(); last = p;
    });
    ["pointerup", "pointercancel", "pointerleave"].forEach(function (t) { c.addEventListener(t, function () { down = false; }); });
    $("pclear").addEventListener("click", function () { ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, c.width, c.height); });
    $("psave").addEventListener("click", function () {
      var b64 = c.toDataURL("image/png").split(",")[1];
      var name = "drawings/pad-" + new Date().toISOString().replace(/[:.]/g, "-") + ".png";
      api("POST", "/api/files/write", { path: name, content: b64, encoding: "base64" })
        .then(function (r) { $("pmsg").textContent = "saved workspace/" + r.path; }).catch(function (e) { $("pmsg").textContent = e.message; });
    });
  })();

  // ---------------------------------------------------------------- code editor
  var code = $("code"), gutter = $("gutter");
  function gut() { var n = code.value.split("\n").length, s = []; for (var i = 1; i <= n; i++) s.push(i); gutter.textContent = s.join("\n"); gutter.scrollTop = code.scrollTop; }
  code.addEventListener("input", gut); code.addEventListener("scroll", function () { gutter.scrollTop = code.scrollTop; });
  code.addEventListener("keydown", function (e) { if (e.key === "Tab") { e.preventDefault(); var s = code.selectionStart; code.setRangeText("    ", s, code.selectionEnd, "end"); gut(); } });
  gut();
  function langClass() { document.body.classList.toggle("lang-cpp", $("lang").value === "cpp"); }
  $("lang").addEventListener("change", langClass);
  api("GET", "/api/examples").then(function (r) {
    r.examples.forEach(function (n) { var o = el("option", n); o.value = n; $("example").appendChild(o); });
  }).catch(function () {});
  $("example").addEventListener("change", function () {
    var n = $("example").value; if (!n) return;
    api("GET", "/api/examples/read?name=" + encodeURIComponent(n)).then(function (r) {
      code.value = r.content; gut(); $("lang").value = n.slice(-4) === ".cpp" ? "cpp" : "basic"; langClass();
    });
  });
  var jsPending = {}, jsSeq = 0, boxReady = false, boxWaiters = [];
  function markReady() { boxReady = true; var w = boxWaiters; boxWaiters = []; w.forEach(function (f) { f(); }); }
  $("jsbox").addEventListener("load", markReady);
  window.addEventListener("message", function (ev) {
    if (ev.source !== $("jsbox").contentWindow) return;   // only our sandbox
    var m = ev.data || {};
    if (m.type === "ready") { markReady(); return; }
    var cb = jsPending[m.id]; if (!cb) return; delete jsPending[m.id]; cb(m);
  });
  function whenBoxReady() {   // never post into the sandbox before it has loaded (or after a reload)
    return new Promise(function (resolve) {
      if (boxReady) return resolve();
      boxWaiters.push(resolve);
      setTimeout(resolve, 8000);
    });
  }
  function pingBox() {
    return whenBoxReady().then(function () { return new Promise(function (resolve) {
      var id = ++jsSeq; jsPending[id] = resolve;
      $("jsbox").contentWindow.postMessage({ type: "ping", id: id }, "*");
      setTimeout(function () { if (jsPending[id]) { delete jsPending[id]; resolve({ type: "no-pong" }); } }, 6000);
    }); });
  }
  function runJS(src, noWorker) {
    return whenBoxReady().then(function () { return new Promise(function (resolve) {
      var id = ++jsSeq; jsPending[id] = resolve;
      $("jsbox").contentWindow.postMessage({ type: "run", id: id, code: src, noWorker: !!noWorker }, "*");
      setTimeout(function () { if (jsPending[id]) { delete jsPending[id]; resolve({ out: [], error: "no reply from sandbox (reloaded)", via: "none" }); boxReady = false; $("jsbox").src = "/ui/sandbox.html"; } }, 6000);
    }); });
  }
  function fmtRun(r) {
    if (r.refused) return "REFUSED: " + r.refused;
    if (r.missing) return "OPTIONAL EXTRA MISSING: " + r.missing + "\n" + (r.note || "");
    var s = "";
    if (r.compile_out) s += "[compile " + (r.compile_rc === 0 ? "ok" : "rc " + r.compile_rc) + "]\n" + r.compile_out + "\n";
    s += r.out || "";
    if (r.timed_out) s += "\n[timeout]";
    return s;
  }
  $("run").addEventListener("click", function () {
    var lang = $("lang").value; show("out", "running...");
    if (lang === "js") { runJS(code.value).then(function (r) { show("out", (r.out || []).join("\n") + (r.error ? "\nERROR: " + r.error : "") + "\n[" + r.via + "]"); }); return; }
    var body = lang === "cpp" ? { code: code.value, stdin: $("cstdin").value || null } : { code: code.value };
    api("POST", lang === "cpp" ? "/api/cpp" : "/api/basic", body).then(function (r) { show("out", fmtRun(r)); }).catch(function (e) { show("out", e.message); });
  });
  $("eopen").addEventListener("click", function () {
    api("GET", "/api/files/read?path=" + encodeURIComponent($("epath").value)).then(function (r) {
      if (r.encoding !== "utf-8") { $("emsg").textContent = "not UTF-8; not opened"; return; }
      code.value = r.content; gut(); $("emsg").textContent = "opened " + r.path;
      var p = r.path.toLowerCase(); $("lang").value = /\.cpp$/.test(p) ? "cpp" : /\.js$/.test(p) ? "js" : "basic"; langClass();
    }).catch(function (e) { $("emsg").textContent = e.message; });
  });
  $("esave").addEventListener("click", function () {
    api("POST", "/api/files/write", { path: $("epath").value, content: code.value }).then(function (r) {
      $("emsg").textContent = "saved " + r.path + (r.archived ? " (old copy archived: " + r.archived + ")" : "") + (r.unchanged ? " (unchanged)" : "");
    }).catch(function (e) { $("emsg").textContent = e.message; });
  });

  // ---------------------------------------------------------------- file browser
  var cwd = "";
  function listDir(p) {
    return api("GET", "/api/files?path=" + encodeURIComponent(p)).then(function (r) {
      cwd = r.path; $("crumbs").textContent = cwd;
      var tb = $("flist").querySelector("tbody"); tb.textContent = "";
      r.items.forEach(function (it) {
        var tr = el("tr", null, "click"); tr.appendChild(el("td", it.name)); tr.appendChild(el("td", it.type)); tr.appendChild(el("td", it.size));
        tr.addEventListener("click", function () {
          var full = (cwd ? cwd + "/" : "") + it.name;
          if (it.type === "dir") listDir(full);
          else if (it.type === "file") api("GET", "/api/files/read?path=" + encodeURIComponent(full)).then(function (f) {
            show("fview", f.encoding === "utf-8" ? f.content : "[" + f.size + " bytes, not UTF-8: " + (f.note || "") + "]");
            $("epath").value = full;
          }).catch(function (e) { show("fview", e.message); });
        });
        tb.appendChild(tr);
      });
      return r;
    }).catch(function (e) { show("fview", e.message); });
  }
  $("frefresh").addEventListener("click", function () { listDir(cwd); });
  $("fup").addEventListener("click", function () { listDir(cwd.split("/").slice(0, -1).join("/")); });
  $("fnew").addEventListener("click", function () {
    var p = $("newname").value; if (!p) return;
    api("POST", "/api/files/write", { path: p, content: "" }).then(function () { listDir(cwd); }).catch(function (e) { show("fview", e.message); });
  });

  // ---------------------------------------------------------------- converter
  function convert(file) {
    $("cmsg").textContent = "converting " + file.name + " (" + file.size + " bytes)...";
    return api("POST", "/api/convert", file, { "X-Filename": encodeURIComponent(file.name) }).then(function (r) {
      $("cmsg").textContent = "run " + r.run_dir + "  counts " + JSON.stringify(r.json_preview.meta.counts) + "  JSON round-trip " + (r.json_roundtrip_equal ? "equal" : "NOT equal");
      var tb = $("citems").querySelector("tbody"); tb.textContent = "";
      r.items.forEach(function (it) { var tr = el("tr"); [it.i, it.name, it.type, it.status, it.notes].forEach(function (v) { tr.appendChild(el("td", v)); }); tb.appendChild(tr); });
      show("cflags", r.flags.length ? r.flags.join("\n") + "\n\nreject/flag log:\n" + r.reject_log.map(function (x) { return x.reason + "  " + x.category + "  " + x.context; }).join("\n") : "(none)");
      show("ctxt", r.txt_preview.map(function (t) { return "== " + t.txt + "\n" + t.text; }).join("\n"));
      show("ccsv", r.csv_preview); show("cjson", r.json_preview);
      return r;
    }).catch(function (e) { $("cmsg").textContent = e.message; throw e; });
  }
  var drop = $("drop");
  ["dragenter", "dragover"].forEach(function (t) { drop.addEventListener(t, function (e) { e.preventDefault(); drop.classList.add("over"); }); });
  ["dragleave", "drop"].forEach(function (t) { drop.addEventListener(t, function (e) { e.preventDefault(); drop.classList.remove("over"); }); });
  drop.addEventListener("drop", function (e) { if (e.dataTransfer.files[0]) convert(e.dataTransfer.files[0]); });
  $("cfile").addEventListener("change", function () { if ($("cfile").files[0]) convert($("cfile").files[0]); });

  // ---------------------------------------------------------------- agent
  function say(text, who, cites) {
    var d = el("div", null, "msg" + (who === "me" ? " me" : "")); d.appendChild(el("div", text));
    (cites || []).forEach(function (c) { d.appendChild(el("div", "[" + c.n + "] " + c.path + ":" + c.lines + "  score " + c.score, "cite")); });
    $("chat").appendChild(d); $("chat").scrollTop = $("chat").scrollHeight;
  }
  function ask(q) {
    if (!q) return Promise.resolve();
    say(q, "me");
    return api("POST", "/api/agent", { q: q, mode: $("amode").value }).then(function (r) { say(r.answer + (r.mode ? "\n(" + r.mode + ")" : ""), "bot", r.citations); return r; })
      .catch(function (e) { say("error: " + e.message, "bot"); });
  }
  $("send").addEventListener("click", function () { var q = $("ask").value.trim(); $("ask").value = ""; ask(q); });
  $("ask").addEventListener("keydown", function (e) { if (e.key === "Enter") $("send").click(); });
  Array.prototype.forEach.call(document.querySelectorAll(".aq"), function (b) { b.addEventListener("click", function () { ask(b.dataset.q); }); });
  $("sgo").addEventListener("click", function () { ask("/scaffold " + $("stpl").value + " " + $("slang").value + " " + ($("sname").value || "my_check")); });


  // ---------------------------------------------------------------- spectrum sweep (representation only)
  // Server computes the samples (/api/sweep); this draws them: log10(f) axis ascending, Latin band labels,
  // ghost = emitted, solid = observed (redshifted), one unbroken overlay line. Audio is off by default.
  var sweep = { d: null, AX: null };
  var sweepAudio = { ctx: null };
  function sanitizeOverlay(t) {   // one unbroken line: control chars / line breaks become spaces
    return String(t || "").replace(/[\u0000-\u001f\u007f\u2028\u2029]+/g, " ").replace(/\s+/g, " ").trim().slice(0, 200);
  }
  function swMode() { var m = $("swmode").value; document.body.classList.remove("sw-mode-octave", "sw-mode-decay", "sw-mode-sampler"); document.body.classList.add("sw-mode-" + m); return m; }
  $("swmode").addEventListener("change", function () { swMode(); drawSweepFromServer(); });
  $("swzr").addEventListener("input", function () { $("swz").value = $("swzr").value; });
  $("swzr").addEventListener("change", function () { drawSweepFromServer(); });
  $("swkr").addEventListener("input", function () { $("swk").value = $("swkr").value; });
  $("swkr").addEventListener("change", function () { drawSweepFromServer(); });
  $("swaudio").addEventListener("change", function () { $("swplay").disabled = !$("swaudio").checked; });
  function sweepQuery() {
    var m = swMode(), p = { mode: m, fps: $("swfps").value, z: $("swz").value.trim(), overlay: sanitizeOverlay($("swover").value) };
    if (m === "octave") { p.samples = $("swn").value; p.f_start = $("swfs").value.trim(); p.f_end = $("swfe").value.trim(); }
    else if (m === "decay") { p.samples = $("swn").value; p.A = $("swA").value.trim(); p.B = $("swB").value.trim(); p.k = $("swk").value.trim(); p.xmax = $("swxmax").value.trim(); p.lift = $("swlift").value.trim(); }
    else { p.m = $("swm").value.trim(); p.n = $("swsn").value.trim(); p.c = $("swc").value.trim(); p.x0 = $("swx0").value.trim(); p.dx = $("swdx").value.trim(); p.steps = $("swsteps").value.trim(); }
    return new URLSearchParams(p).toString();
  }
  function loadSweep() {
    $("swmsg").textContent = "computing...";
    return api("GET", "/api/sweep?" + sweepQuery()).then(function (d) { sweep.d = d; $("swmsg").textContent = d.samples.length + " samples @ " + d.fps + " fps"; return d; })
      .catch(function (e) { $("swmsg").textContent = e.message; throw e; });
  }
  function axisFrom(d) {   // vertical axis = log10(f / Hz); lo at the bottom, hi at the top
    var ex = d.axis.map(function (a) { return a.exp; });
    return { lo: Math.min.apply(null, ex), hi: Math.max.apply(null, ex), L: 134, R: 160, T: 18, B: 62 };
  }
  function swPy(AX, h, L) { return AX.T + (AX.hi - L) / (AX.hi - AX.lo) * (h - AX.T - AX.B); }
  function swPx(AX, w, i, n) { return AX.L + (n > 1 ? i / (n - 1) : 0) * (w - AX.L - AX.R); }
  var SUP = { "0": "\u2070", "1": "\u00b9", "2": "\u00b2", "3": "\u00b3", "4": "\u2074", "5": "\u2075", "6": "\u2076", "7": "\u2077", "8": "\u2078", "9": "\u2079" };
  function sup(n) { return String(n).split("").map(function (c) { return SUP[c] || c; }).join(""); }
  function drawSweep(d) {
    var c = $("sweep"), ctx = c.getContext("2d"), w = c.width, h = c.height, AX = axisFrom(d), n = d.samples.length;
    sweep.AX = AX;
    ctx.fillStyle = "#05070a"; ctx.fillRect(0, 0, w, h);
    var x0 = AX.L, x1 = w - AX.R;
    d.bands.forEach(function (b, k) {   // band strips + Latin labels
      var yTop = swPy(AX, h, Math.min(b.hi_log10, AX.hi)), yBot = swPy(AX, h, Math.max(b.lo_log10, AX.lo));
      if (b.highlight) {
        var g = ctx.createLinearGradient(0, yBot, 0, yTop);
        g.addColorStop(0, "rgba(255,0,0,0.55)"); g.addColorStop(0.3, "rgba(255,200,0,0.55)"); g.addColorStop(0.5, "rgba(0,255,0,0.55)");
        g.addColorStop(0.7, "rgba(0,160,255,0.55)"); g.addColorStop(1, "rgba(130,0,255,0.55)");
        ctx.fillStyle = g;
      } else ctx.fillStyle = k % 2 ? "rgba(255,255,255,0.045)" : "rgba(255,255,255,0.09)";
      ctx.fillRect(x0, yTop, x1 - x0, yBot - yTop);
      ctx.fillStyle = b.highlight ? "#ffffff" : "#b9c6d0"; ctx.font = (b.highlight ? "bold " : "") + "13px serif";
      ctx.textAlign = "left"; ctx.textBaseline = "middle";
      ctx.fillText(b.name, x1 + 8, (yTop + yBot) / 2);
    });
    ctx.strokeStyle = "#3a4650"; ctx.fillStyle = "#c8d3dc"; ctx.font = "12px sans-serif"; ctx.textAlign = "right"; ctx.lineWidth = 1;
    d.axis.forEach(function (a) {   // decade ticks, ascending upward
      var y = swPy(AX, h, a.exp);
      ctx.beginPath(); ctx.moveTo(x0 - 4, y); ctx.lineTo(x1, y); ctx.stroke();
      ctx.fillText("10" + sup(a.exp) + " Hz  " + a.label, x0 - 8, y);
    });
    ctx.save(); ctx.translate(11, (AX.T + h - AX.B) / 2); ctx.rotate(-Math.PI / 2); ctx.textAlign = "center"; ctx.fillText("log\u2081\u2080(f / Hz)", 0, 0); ctx.restore();
    function curve(key, style, width, dash, colored) {
      ctx.lineWidth = width; ctx.setLineDash(dash);
      for (var i = 1; i < n; i++) {
        var a = d.samples[i - 1], b = d.samples[i];
        ctx.strokeStyle = colored ? "rgb(" + b.rgb_obs.join(",") + ")" : style;
        ctx.beginPath(); ctx.moveTo(swPx(AX, w, i - 1, n), swPy(AX, h, a[key])); ctx.lineTo(swPx(AX, w, i, n), swPy(AX, h, b[key])); ctx.stroke();
      }
      ctx.setLineDash([]);
    }
    ctx.save(); ctx.beginPath(); ctx.rect(x0, AX.T - 6, x1 - x0, h - AX.T - AX.B + 12); ctx.clip();
    curve("log10_f_emit", "rgba(230,236,242,0.35)", 2, [6, 4], false);   // ghost: emitted
    curve("log10_f_obs", "#fff", 3, [], true);                           // solid: observed, frame colours
    ctx.restore();
    ctx.fillStyle = "#93a1ad"; ctx.font = "12px sans-serif"; ctx.textAlign = "left"; ctx.textBaseline = "alphabetic";
    ctx.fillText("x = " + d.samples[0].x + " \u2192 " + d.samples[n - 1].x + "    ghost = emitted, solid = observed (z = " + d.key_values.z + ", shift " + d.key_values.z_shift_octaves_trunc8 + " oct)", x0, h - AX.B + 18);
    ctx.fillStyle = "#f3e9c6"; ctx.font = "italic 17px serif"; ctx.textAlign = "center";
    ctx.fillText(sanitizeOverlay($("swover").value), (x0 + x1) / 2, h - 14);   // one unbroken line
    $("swformula").textContent = "drawn: " + d.formula;
    var kv = d.key_values;
    $("swkeys").textContent = "y(100 MHz) = " + kv.y_at_100MHz_trunc8 + "   y(500 THz) = " + kv.y_at_500THz_trunc8 + "   1+z = " + kv.one_plus_z + "   shift log\u2082(1+z) = " + kv.z_shift_octaves_trunc8 + " octaves   (truncated, 8 places)";
    $("swfinal").textContent = d.final ? "final value: y = " + d.final.y + "  (f_emit " + d.final.f_emit_hz_trunc3 + " Hz, truncated)" : "";
  }
  function drawSweepFromServer() { return loadSweep().then(function (d) { drawSweep(d); return d; }); }
  function sweepToPlayer(d) {   // one solid 8x8 frame per sample, played by the existing player (built, then shown or dropped)
    var frames = d.samples.map(function (s) { var px = "", ch = String.fromCharCode(s.rgb_obs[0], s.rgb_obs[1], s.rgb_obs[2]); for (var i = 0; i < 64; i++) px += ch; return btoa(px); });
    var pd = { fps: d.fps, dt: d.dt, shape: [frames.length, 8, 8, 3], frames: frames, synthetic: true, source: "spectrum sweep (representation only)" };
    player.data = pd; off.width = 8; off.height = 8;
    return pd;
  }
  $("swdraw").addEventListener("click", function () { drawSweepFromServer().catch(function () {}); });
  $("swframes").addEventListener("click", function () {
    var go = function (d) { drawSweep(d); sweepToPlayer(d); player.run = true; player.shown = player.dropped = 0; player.next = 0; player.t0 = performance.now(); requestAnimationFrame(tick); };
    loadSweep().then(go).catch(function () {});
  });
  $("swplay").addEventListener("click", function () {
    if (!$("swaudio").checked || !sweep.d) return;
    var AC = window.AudioContext || window.webkitAudioContext; if (!AC) { $("swmsg").textContent = "no Web Audio in this browser"; return; }
    if (sweepAudio.ctx) { try { sweepAudio.ctx.close(); } catch (e) {} }
    var d = sweep.d, ac = new AC(), T = d.audio.transpose_octaves, dt = 1 / d.fps, t0 = ac.currentTime + 0.05, n = d.samples.length;
    sweepAudio.ctx = ac;
    var merge = ac.createChannelMerger(2); merge.connect(ac.destination);
    [["y_obs", 0], ["y_emit", 1]].forEach(function (pair) {   // left = observed, right = emitted
      var o = ac.createOscillator(), g = ac.createGain(); o.type = "sine"; o.connect(g); g.connect(merge, 0, pair[1]);
      d.samples.forEach(function (s, i) {
        var f = 130.8 * Math.pow(2, s[pair[0]] - T), ok = f >= 20 && f <= 20000;   // whole-octave transpose: shape kept
        o.frequency.setValueAtTime(Math.min(Math.max(f, 1), 22000), t0 + i * dt); g.gain.setValueAtTime(ok ? 0.12 : 0, t0 + i * dt);
      });
      o.start(t0); o.stop(t0 + n * dt);
    });
    setTimeout(function () { try { ac.close(); } catch (e) {} if (sweepAudio.ctx === ac) sweepAudio.ctx = null; }, (n * dt + 0.5) * 1000);
    $("swmsg").textContent = "audio: transposed down " + T + " octaves (representation only); left = observed, right = emitted";
  });
  swMode();
  drawSweepFromServer().catch(function () {});

  // ---------------------------------------------------------------- start + smoke mode (?smoke=1, used by ui_smoke.py)
  boot().catch(function () {});
  refreshStatus();
  if (/[?&]smoke=1/.test(location.search)) {
    var res = {}, step = function (name, p) { return p.then(function (v) { res[name] = v; }, function (e) { res[name] = "ERR " + e.message; }); };
    Promise.resolve()
      .then(function () { return step("boot", boot().then(function (r) { return r.ok; })); })
      .then(function () { return step("descend", api("POST", "/api/descend", { m: 5, n: 3, B: 7, x0: 0, dx: 3, steps: 4 }).then(function (r) { return r.final; })); })
      .then(function () { $("fps").value = "64"; $("nframes").value = "4"; $("fsize").value = "32"; return step("frames", loadFrames().then(function (d) { paint(buildFrame(0)); return d.shape.join("x"); })); })
      .then(function () { return step("pixel0", Promise.resolve(Array.prototype.slice.call(off.getContext("2d").getImageData(0, 0, 1, 1).data, 0, 3).join(","))); })
      .then(function () { return step("files", api("GET", "/api/files?path=").then(function (r) { return Array.isArray(r.items); })); })
      .then(function () { return step("agent", api("POST", "/api/agent", { q: "personal data masked DM-5", mode: "rules" }).then(function (r) { return r.known && r.citations.length > 0; })); })
      .then(function () { return step("js_ping", pingBox().then(function (r) { return r.type + "/" + r.worker; })); })
      .then(function () { return step("js_iframe", runJS("console.log(6*7)", true).then(function (r) { return (r.out || []).join("|") + "/" + r.via; })); })
      .then(function () { return step("js_sandbox", runJS("console.log(6*7)").then(function (r) { return (r.out || []).join("|") + "/" + r.via; })); })
      .then(function () { return step("js_no_network", runJS("console.log(typeof fetch)").then(function (r) { return (r.out || []).join("|"); })); })
      .then(function () { return step("sweep_keys", drawSweepFromServer().then(function (d) { return d.key_values.y_at_100MHz_trunc8 + "/" + d.key_values.y_at_500THz_trunc8; })); })
      .then(function () { return step("sweep_axis_up", Promise.resolve(swPy(sweep.AX, $("sweep").height, 8) > swPy(sweep.AX, $("sweep").height, 15))); })
      .then(function () { return step("sweep_latin", Promise.resolve(sweep.d.bands.map(function (b) { return b.name; }).join("|"))); })
      .then(function () { return step("sweep_overlay", Promise.resolve(sanitizeOverlay("Lux orta\nest") === "Lux orta est" && sanitizeOverlay($("swover").value) === sweep.d.overlay_default && sweep.d.overlay === sweep.d.overlay_default)); })
      .then(function () { return step("sweep_vis_painted", Promise.resolve((function () { var c = $("sweep"), y = Math.round(swPy(sweep.AX, c.height, 14.75)), p = c.getContext("2d").getImageData(sweep.AX.L + 3, y, 1, 1).data; return p[0] + p[1] + p[2] > 60; })())); })
      .then(function () { return step("sweep_frame0", Promise.resolve((function () { var d = sweepToPlayer(sweep.d); paint(buildFrame(0)); var p = off.getContext("2d").getImageData(0, 0, 1, 1).data; return [p[0], p[1], p[2]].join(",") === sweep.d.samples[0].rgb_obs.join(",") && d.shape[0] === sweep.d.samples.length; })())); })
      .then(function () { return step("sweep_audio_off", Promise.resolve(!$("swaudio").checked && $("swplay").disabled && sweepAudio.ctx === null)); })
      .then(function () { $("swz").value = "0.5"; $("swzr").value = "0.5"; return step("sweep_z_half", drawSweepFromServer().then(function (d) { return d.key_values.z_shift_octaves_trunc8; })); })
      .then(function () {
        var ok = res.boot === true && res.descend === "8647" && res.frames === "4x32x32x3" && res.pixel0 === "7,135,42" && res.js_ping === "pong/function" && res.js_iframe === "42/iframe" && res.files === true && res.agent === true && /^42\//.test(res.js_sandbox) && res.js_no_network === "undefined";
        ok = ok && res.sweep_keys === "19.54420602/41.79770269" && res.sweep_axis_up === true && res.sweep_latin === "Radio|Undae minimae|Infrarubrum|Visibile (lumen)|Ultravioletum" &&
          res.sweep_overlay === true && res.sweep_vis_painted === true && res.sweep_frame0 === true && res.sweep_audio_off === true && res.sweep_z_half === "0.58496250";
        res.verdict = ok ? "PASS" : "FAIL";
        $("smoke").textContent = "SMOKE " + JSON.stringify(res);
        document.body.setAttribute("data-smoke", res.verdict);
        api("POST", "/api/files/write", { path: "smoke_result.json", content: JSON.stringify(res) }).catch(function () {});
        document.querySelector('#tabs button[data-tab="canvas"]').click();
      });
  }
})();
