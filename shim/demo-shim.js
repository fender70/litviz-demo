// Static demo: there is no LitViz backend behind this page. The app runs on its bundled fixture
// (hand-written, fictional papers). This shim answers the Idea Landscape endpoints from a synthetic
// layout so the Ideas and 3D views have something to show; every other /api call gets a 404,
// which the app treats as "no backend".
(function () {
  const base = document.currentScript.src.replace(/[^/]*$/, "");
  let data = null;
  const load = () => (data ??= fetch(base + "landscape.json").then((r) => r.json()));
  const json = (body, status = 200) =>
    new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
  const realFetch = window.fetch.bind(window);

  window.fetch = async function (input, init) {
    const raw = typeof input === "string" ? input : input instanceof URL ? input.href : input.url;
    const url = new URL(raw, location.href);
    if (url.origin !== location.origin || !url.pathname.startsWith("/api/")) return realFetch(input, init);
    const path = url.pathname;
    if (path === "/api/landscape") return json((await load()).state);
    if (path === "/api/landscape/search") {
      const d = await load();
      const words = (url.searchParams.get("q") || "").toLowerCase().split(/\W+/).filter((w) => w.length > 2);
      const k = Number(url.searchParams.get("k")) || 30;
      const hits = Object.values(d.chunks)
        .map((c) => {
          const t = c.text.toLowerCase();
          const score = words.reduce((s, w) => s + (t.includes(w) ? 1 : 0), 0) / Math.max(1, words.length);
          return { id: c.id, paper_id: c.paper_id, page: c.page, section: c.section, score,
                   snippet: c.text.slice(0, 220), on_map: true, embedded: true };
        })
        .filter((h) => h.score > 0)
        .sort((a, b) => b.score - a.score)
        .slice(0, k);
      return json({ query: url.searchParams.get("q") || "", mode: "keyword", hits });
    }
    const m = path.match(/^\/api\/landscape\/chunks\/(.+)$/);
    if (m) {
      const c = (await load()).chunks[decodeURIComponent(m[1])];
      return c ? json(c) : json({ detail: "not found" }, 404);
    }
    return json({ detail: "Static demo: no backend" }, 404);
  };
})();
