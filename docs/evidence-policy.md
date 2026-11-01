# Evidence and archive policy

Current code and test results belong in the development entry point. Historical
receipts certify only their recorded bytes and scope; never rewrite them to make
a later implementation appear certified.

Generate a compact inventory without copying the 4 GB historical tree:

    python scripts/evidence_index.py --output /tmp/archcanvas-evidence-index.json

The index groups tracked evidence by path, counts bytes and nested snapshots,
and binds paths to Git index blob identities. It records tracked evidence changes.
It is an archive/navigation index, not a new acceptance receipt. The checked-in
[baseline index](evidence-index.json) records the initial inventory; regenerate to
a new path when a fresh inventory is needed.

For an external immutable archive, choose a committed evidence group, export it
with Git, record its SHA-256 and retain the commit and group path in the external
archive catalog. For example, with an explicit GROUP:

    git archive --format=tar HEAD "docs/evidence/$GROUP" > /absolute/archive/group.tar
    sha256sum /absolute/archive/group.tar

Verify restoration into an independent directory before considering removal of
any tracked originals. This change adds indexing and prevents new nested evidence
copies; it does not remove history, rewrite Git or relocate existing receipts.
New snapshots should record source blob/hash manifests and only necessary
artifacts. Do not copy docs/evidence inside another evidence directory.
