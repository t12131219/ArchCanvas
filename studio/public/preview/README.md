# ArchCanvas canvas

This directory contains the browser canvas embedded by ArchCanvas Studio. Build and start the application from the repository root as described in its README; this directory does not require a separate server.

The canvas supports source inspection, recursive expansion, editing, undo/redo, routing and SVG/JSON export. Model-source facts and declared visual draft changes retain separate identities. Visual edits never silently modify Python source.

Current model data and source components live in `data/`. The small retained source/figure files in `snapshots/` back the current examples' source links. Historical audit archives and duplicate model catalogs are excluded.

Browser state uses IndexedDB/localStorage for the current origin. Export editing JSON before changing browser, host or port. See `source_adapter/README.md` for source import and `BRIDGE.md` for the Studio integration protocol.
