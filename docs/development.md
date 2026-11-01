# Current development and validation

The maintained source tree, local frozen bundles and historical acceptance
receipts are distinct versions. Start with the Skill launcher doctor summary,
then inspect actual runtime capabilities. Default native assembly and formal
Python authoring have separate contracts; see
[runtime compatibility](../skills/archcanvas/references/runtime-compatibility.md).
The [2026-11-01 maintenance report](maintenance-20261101.md) records this change's
actual test results and remaining gaps.

## Local build

Use Python 3.11+ and Node 24+. In a new checkout:

    python3 -m venv .venv
    cd studio
    npm ci
    npm run build
    npm test
    npm run audit:preview
    cd ..
    PYTHONPATH=src .venv/bin/python -m archcanvas_cli serve --data-dir /absolute/state-root

Static analysis needs no PyTorch and never runs model source. Publication and
kernel-isolated CPU execution remain optional separately installed profiles;
their dependency locks and capability checks are documented in the README.
One service owns each state root.

## Regression and CI scope

The GitHub workflow builds with locked dependencies, runs the complete Node test
entry and selected Python static/real-loopback regressions. It does not certify
three-host Agent E2E, a full browser matrix, publication review or actual model
execution. Summary HTTP cancel tests use mocks; actual CPU tests require the
explicit Linux profile. Skipped tests are not execution evidence.

For the full backend collection in a suitably configured local environment:

    PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v

Keep fail/skip counts with the exact commit and build. Do not add unrelated
historical counts together or regenerate acceptance evidence to hide failures.
The large Transformer still has explicitly diagnosed overlapping routes.
An inspectable native graph is not a complete layout: tests require its pending
or failed markers, preserve its source/history, and reject a successful Apply
when full geometry validation fails. Parameter-read arrows are exact consumer
annotations and remain covered by the canonical accounting tests.

The optional DOM export check accepts an existing browser through
`ARCHCANVAS_TEST_BROWSER` and Playwright through `ARCHCANVAS_TEST_PLAYWRIGHT`.
Use the installed headless-shell when the full Chromium executable cannot start;
report skipped/unavailable browser checks explicitly.

The generated current AST test fixture uses repository-relative parser paths;
after changing its declared parser dependencies, regenerate it and rerun its
independent graph assertions:

    .venv/bin/python -I -B studio/scripts/generate-preview-ast-fixture.py

## Distribution

New candidates carry studio/src, studio/scripts, studio/public and prebuilt
studio/dist; Python/npm dependencies are installed separately. The bounded
uncompressed bundle budget is 1280 MiB/20,000 files, including its manifest.
Historical bundles retain their own inventories.

    python scripts/m5_beta_bundle.py candidate --project-root . --version 0.1.0-beta.7 --output /absolute/new-candidate.tar.gz

The bundle suite includes independent unpacking and rebuilding using explicitly
reused locked node_modules. That proves source/asset completeness, not a clean
network install. A rebuilt or otherwise modified frozen directory needs a fresh
manifest before it can report verified; doctor rejects missing, additional,
linked and altered files. Rebuilding does not grant a new host/publication claim.

## License and history

Original project code is licensed under [Apache-2.0](../LICENSE). Vendored code,
model materials and fonts retain their own licenses; consult
[third-party notices](../THIRD_PARTY_NOTICES.md). Do not relicense third-party
materials by applying the project license to them.

Historical receipts remain immutable. See the [evidence policy](evidence-policy.md)
and [baseline index](evidence-index.json) for navigation and external archiving.
