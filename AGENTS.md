# ArchCanvas development

- The repository contains the complete maintained runtime and Studio. Do not introduce paths or runtime dependencies on another checkout, a prototype, or a local development machine.
- Visual gestures and language edits share typed canvas operations and undo history. Visual edits do not silently modify Python model source.
- The Summary canvas owns its graph, routing, history and browser persistence. Connect it to Studio through the existing message bridge and explicit source identities.
- Static analysis reads source text without importing or executing user models. Unknown structures retain diagnostics. Explicit CPU observations use the isolated runtime.
- Formal source edits use managed copies, independently checked supported operations, concrete review and guarded commit.
- Keep source identities, evidence and model/operand accounting intact when changing presentation. Do not rewrite signed model data solely to remove provenance paths.
- Keep the repository compact: do not commit virtual environments, node_modules, dist, runtime state, build caches, screenshots, historical evidence or copied source trees.
- Keep third-party license texts and source headers. Instructions for development checks are in docs/development.md.
