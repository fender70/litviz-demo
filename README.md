# LitViz Sandbox

A single-page, in-browser demo of the LitViz workflow on **synthetic papers**:

1. **Parse**: five fictional papers, given as page text
2. **Extract**: scripted "model output" (claims with supporting quotes, some deliberately wrong)
3. **Verify**: every quote must appear word for word in its paper (a port of LitViz's `pipeline/verify.py`)
4. **Link**: scripted relations between papers, each backed by a quote from the source paper
5. **Map**: the grounding mode (`strict` / `lenient` / `open`) decides what reaches the graph

No model, no backend, no network calls. Everything runs in the page.

**Try:** edit a quote so one word differs, edit a page to remove a sentence a link depends on,
add your own paper and a link to it, switch grounding modes, or download the resulting `graph.json`.

Built-in test cases: paraphrase, wrong number, elided quote (`...`), too-short quote, model inference
with no quote, a hyphen at a line break, curly quotes, a sentence across a page break, and a fabricated link.

Feedback: open an issue in this repo.
