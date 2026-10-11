# LitViz demo

**Live:** https://fender70.github.io/litviz-demo/

The real LitViz interface (map, matrix, frontier, Idea Landscape, 3D view, filters, facets, evidence,
walkthrough) running in the browser on **fictional sample papers**. There is no backend and no model:
the app runs in its fixture mode, and the yellow *FIXTURE DATA* badge says so. Chat, uploads and
re-runs need the local model, so the demo explains that instead of answering.

- **Idea Landscape / 3D landscape axes:** served by `demo/demo-shim.js` from a *synthetic* layout
  (`scripts/make_landscape.py`): passages are the sample papers' claims and evidence, placed by kind and
  method family, not by real embeddings.
- **[Sandbox](https://fender70.github.io/litviz-demo/sandbox/)**: a small page that runs the
  quote-verification step for real (a port of `pipeline/verify.py`). Edit quotes and pages, switch
  grounding modes (strict / lenient / open) and see what reaches the map.

## Rebuilding

```bash
scripts/build.sh /path/to/LitViz   # builds that checkout's frontend into this repo's root
```

The build changes one line of the app: the Idea Landscape is not disabled in fixture mode.

Feedback: open an issue in this repo.
