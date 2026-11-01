# Architecture

ArchCanvas combines a local Python service, a React Studio, a browser canvas engine and a portable Agent Skill.

## Data flow

1. The UI or CLI supplies source text and an explicit entry.
2. Python static analyzers produce architecture data or Summary semantic IR without importing the model.
3. `archcanvas_preview` maps semantic facts, source evidence and identities into the browser protocol.
4. React's `PreviewStudio` embeds the Summary editor through its message bridge.
5. The editor manages its graph, visible semantic cuts, recursive layout, routing and browser persistence.
6. Studio panels map selected objects and presentation changes through explicit identities. The publication backend validates the supplied SVG before optional conversion.

Formal Python editing uses `archcanvas_authoring` and `archcanvas_transactions`. Explicit model observations use `archcanvas_runtime` and its isolated worker. These are separate from visual graph edits.

## Backend packages

| Package | Responsibility |
| --- | --- |
| `archcanvas_cli` | CLI, local HTTP service, persistence and source workspaces |
| `archcanvas_python` | Formal Python source discovery, structure and dependency analysis |
| `archcanvas_summary_semantic` | Summary static semantic IR and explicit observation contracts |
| `archcanvas_preview` | Preview, assembly, source-module and component-library bridges |
| `archcanvas_authoring` | Catalog, drafts, static shape contracts and managed source editing |
| `archcanvas_adapters` | Source-bound adapters and declarative AST view rules |
| `archcanvas_transactions` | Prepared, reviewed and guarded source modifications |
| `archcanvas_runtime` | Isolated CPU control and workers |
| `archcanvas_publication` | SVG validation and SVG/PDF/PNG conversion |

## Frontend

`studio/src/App.tsx` coordinates the workbench. `PreviewStudio.tsx` hosts the embedded canvas; `AuthoringStudio.tsx` implements the formal source/draft workspace. `studio/src/core` holds the formal document, history, geometry and export contracts.

`studio/public/preview/yworks_edge_router_lab` contains the live canvas application, router, graph engine, workers, recursive storage and Studio integrations. `semantic_studio` contains the native semantic projection and layout modules. `data/semantic`, `data/source-components` and the referenced current case assets are runtime resources.

The small retained `snapshots/transformer_programmatic_guide/generated` subset supplies source metadata, original figures and layout/source links used by current cases. It is not the historical audit archive. Source facts and hashes embedded in IR remain unchanged.
