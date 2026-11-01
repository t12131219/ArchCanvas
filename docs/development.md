# Development

Use Python 3.11+ and Node.js 24+. Run commands from the repository root.

## Build

```bash
python3 -m venv .venv
cd studio
npm ci
npm run build
npm run audit:preview
cd ..
python3 -B scripts/check_assets.py
```

For frontend development, start the Python service on port 8765, then run `npm run dev` in `studio`. Vite forwards `/api` to that service. Rebuild the frontend before serving its production files.

## Tests

Install `requirements.lock` into `.venv` and provide system Cairo before running the complete backend suite; several export tests exercise actual PDF/PNG conversion. The CI workflow installs these dependencies.

```bash
PYTHONPATH=src .venv/bin/python -B -m unittest discover -s tests -v
cd studio
npm test
```

Tests tied to archived releases, removed migration snapshots and historical acceptance reports are excluded from this source distribution. Retained tests cover runtime functionality. Optional Cairo/PDF, browser and isolated CPU checks may require additional dependencies or environment support; report their skips separately.

`python3 -B scripts/check_assets.py` checks current catalogs, pinned model and component bytes, source resources and browser script entries. It needs no third-party Python packages. `npm run audit:preview` checks frontend module boundaries.

The optional browser export check accepts an existing browser through `ARCHCANVAS_TEST_BROWSER` and Playwright through `ARCHCANVAS_TEST_PLAYWRIGHT`.

## Runtime utilities

- `scripts/canvas_bridge.mjs` implements CLI/service canvas operations using the TypeScript core.
- `scripts/export_canvas.mjs` exports a saved canvas document.
- `scripts/atomic_export.mjs` stages export files and receipts together, with recovery for ordinary failures.
- `scripts/build_source_component_library.py` rebuilds the built-in component library from the bundled semantic catalog.

## Repository contents

Commit source, dependency locks, current model data, tests, documentation and licenses. Do not commit `.venv`, `.venv-runtime`, `node_modules`, `studio/dist`, `.archcanvas`, caches or test-generated scratch directories. The built frontend copies public assets into `studio/dist`; keeping both in Git would duplicate them.

Use a fresh state directory for development HTTP checks. Model paths embedded in bundled IR are provenance labels; do not access external local paths or rewrite digests to make them appear newly verified.
