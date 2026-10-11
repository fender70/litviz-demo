"""Synthetic Idea Landscape for the static demo.

Turns the fixture's claims and edge evidence into passages and places them in 2D the way a UMAP of
embeddings would look: passages of the same kind (problem, method, results...) from papers of the same
method family land near each other. Positions are made up, deterministic (seeded), and labelled synthetic.

usage: python scripts/make_landscape.py <LitViz>/frontend/fixtures/mock_graph.json out.json
"""
import json
import math
import random
import sys

graph = json.load(open(sys.argv[1], encoding="utf-8"))
rng = random.Random(7)

SECTION = {"problem": "Introduction", "method": "Method", "datasets": "Experiments",
           "results": "Results", "limitations": "Limitations"}
families = [f["id"] for f in graph["facets"]["method_families"]]
kinds = list(SECTION)
fam_center = {f: (math.cos(2 * math.pi * i / len(families)) * 6, math.sin(2 * math.pi * i / len(families)) * 6)
              for i, f in enumerate(families)}
kind_center = {k: (math.cos(2 * math.pi * i / len(kinds) + 0.6) * 4, math.sin(2 * math.pi * i / len(kinds) + 0.6) * 4)
               for i, k in enumerate(kinds)}

chunks, points = {}, []


def add(paper, kind, page, text):
    n = sum(1 for c in chunks.values() if c["paper_id"] == paper["id"]) + 1
    cid = f'{paper["id"]}-K{n}'
    fam = paper["tags"]["method_family"]["family_id"]
    fx, fy = fam_center.get(fam, (0, 0))
    kx, ky = kind_center[kind]
    x = 0.6 * fx + 0.4 * kx + rng.gauss(0, 0.7)
    y = 0.6 * fy + 0.4 * ky + rng.gauss(0, 0.7)
    chunks[cid] = {"id": cid, "paper_id": paper["id"], "page": page, "page_end": page, "section": SECTION[kind], "text": text}
    points.append({"id": cid, "paper_id": paper["id"], "page": page, "page_end": page, "section": SECTION[kind],
                   "x": round(x, 4), "y": round(y, 4)})


papers = {p["id"]: p for p in graph["papers"]}
for p in graph["papers"]:
    add(p, "problem", 1, p["summary"])
    for kind, items in p["contributions"].items():
        for c in items:
            add(p, kind, c["page"], f'{c["text"]} "{c["quote"]}"')
for e in graph["edges"]:
    for ev in e["evidence"]:
        if ev.get("context"):
            add(papers[ev["paper_id"]], "method", ev["page"], ev["context"])

layout = {"points": points, "backend": "umap-learn", "skipped": [], "computed_at": graph["generated_at"],
          "seconds": 0, "import_seconds": 0, "fit_seconds": 0, "params": {"n_neighbors": 15, "min_dist": 0.1, "seed": 7},
          "embed_model": "synthetic (demo)", "new_chunks": 0, "removed_chunks": 0}
state = {"status": "ready", "layout": layout, "current": True, "preference": "auto",
         "installed": {"cuml": False, "umap-learn": True}, "min_points": 10,
         "chunks": len(points), "embedded": len(points), "missing_embeddings": 0, "embed_model": "synthetic (demo)"}
json.dump({"state": state, "chunks": chunks}, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False)
print(f"{len(points)} synthetic passages")
