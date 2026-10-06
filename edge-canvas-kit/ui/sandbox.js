// sandbox.js -- runs editor JavaScript inside a sandboxed iframe (opaque origin, no network: CSP connect-src 'none').
// Prefers a Worker (can be stopped on timeout); falls back to in-frame Function if Workers are unavailable.
"use strict";
(function () {
  var LIMIT_MS = 3000, MAX_LINES = 2000;
  function fmt(a) { try { return typeof a === "string" ? a : JSON.stringify(a); } catch (e) { return String(a); } }
  try { parent.postMessage({ type: "ready" }, "*"); } catch (e) {}
  window.addEventListener("message", function (ev) {
    var msg = ev.data || {};
    if (msg.type === "ping") { ev.source.postMessage({ type: "pong", id: msg.id, worker: typeof Worker }, "*"); return; }
    if (msg.type !== "run" || typeof msg.code !== "string") return;
    var reply = function (out) { ev.source.postMessage({ type: "result", id: msg.id, out: out.out, error: out.error || "", via: out.via }, "*"); };
    var prelude = "var __o=[];var console={log:function(){__o.push(Array.prototype.map.call(arguments,function(a){try{return typeof a==='string'?a:JSON.stringify(a)}catch(e){return String(a)}}).join(' '));if(__o.length>" + MAX_LINES + ")throw new Error('output cap');}};console.error=console.warn=console.info=console.log;self.fetch=undefined;self.XMLHttpRequest=undefined;self.WebSocket=undefined;self.importScripts=undefined;\n";
    var body = prelude + "try{(function(){\n" + msg.code + "\n})();postMessage({out:__o});}catch(e){postMessage({out:__o,error:String(e)});}";
    var w = null;
    if (!msg.noWorker) { try { w = new Worker(URL.createObjectURL(new Blob([body], { type: "text/javascript" }))); } catch (e) { w = null; } }
    if (w) {
      var done = false;
      var timer = setTimeout(function () { if (!done) { done = true; w.terminate(); reply({ out: [], error: "timeout " + LIMIT_MS + " ms (worker stopped)", via: "worker" }); } }, LIMIT_MS);
      w.onmessage = function (e) { if (done) return; done = true; clearTimeout(timer); w.terminate(); reply({ out: e.data.out || [], error: e.data.error, via: "worker" }); };
      w.onerror = function (e) { if (done) return; done = true; clearTimeout(timer); w.terminate(); e.preventDefault(); reply({ out: [], error: String(e.message || "worker error"), via: "worker" }); };
      return;
    }
    var lines = [];
    var con = { log: function () { lines.push(Array.prototype.map.call(arguments, fmt).join(" ")); } };
    con.error = con.warn = con.info = con.log;
    try { new Function("console", msg.code)(con); reply({ out: lines, via: "iframe" }); }
    catch (e) { reply({ out: lines, error: String(e), via: "iframe" }); }
  });
})();
