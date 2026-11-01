# Visual workflow

## Start from the active Summary document

Resolve the runtime with the Skill launcher and inspect its actual capabilities.
The development Studio uses the native Summary iframe for graph interaction,
layout, hierarchy, undo/redo and browser persistence. Formal Python source
editing remains a separate workflow; see [runtime-compatibility.md](runtime-compatibility.md).

Reuse the active graph and preserve user edits. A new model-library opening or
an export of the original source does not prove that the edited graph was saved.
Do not change or save the user's reading state merely to run an acceptance test;
use an independent browser context/state root for tests.

## Hierarchy and reading scope

Use **模块展开** and select an actual module by its stable identity. Its source
depth, **架构概览**, **模块详图**, and **恢复目标模块默认展开** affect that scope;
siblings can retain different depths. Use the hierarchy tree or canvas for
local expansion. Do not map these states to the retired fixed L0–L3 matrix or
infer node counts from an old fixture.

For a changed reading view, restore the root module's default expansion when
requested; do not re-import the source or replace the user's graph. Check the
result and save only the state intended by the user.

## Visual edits

Use controls exposed by the current toolbar, selection panel and page/object
menus. Resolve targets through current graph identities. Moves, bends, labels,
styles, legends and annotations are presentation changes; they do not authorize
Python edits or alter canonical tensor/port bindings. Preserve manual geometry
and independent undo history. Check the actual supported operation before using
a CLI or API; do not guess a visual-patch schema from old acceptance material.

Current Summary **编辑** opens a native assembly copy. It does not imply a Python
source draft or source generation. For reviewed Python edits use the explicit
formal source workspace and [source-review.md](source-review.md).

There is no current global black-and-white preset selector. Do not direct the
user to one. Existing monochrome presentation in an imported/saved document
remains supported by the shared renderer; retaining that compatibility is not
evidence of a preset UI.

## Inspect, save and export

Inspect the actual overview and a representative detail. Check text clipping,
ports/endpoints, node/header intrusion, unresolved routes, residual/memory paths
and the smallest labels at final physical size. Pending/failed routes are not a
completed layout, even when the graph remains inspectable.

Export through the current dialog from the current graph revision. Choose the
whole canvas or an offered detail range, the format and physical width. The
85/180 mm choices are output widths, not hierarchy levels. Read the actual text
preflight; 7 pt is a starting recommendation, not publication acceptance.
Inspect generated SVG/PDF/PNG and retain their real receipts. A browser-declared
preview binding must not be reported as verified Python source identity.

For substantive edits, verify undo/redo and save/reopen. Summary browser storage
and editable JSON are distinct from the formal service's CanvasDocument store;
only claim transport/reimport when the actual JSON bytes were checked.

## Verification boundaries

Use the current Summary regression/engine tools in the project's
[development entry](../../../docs/development.md). The former benchmark/study
query-string panels, fixed-frontier visual matrix, formal DOM observer and trial
slot collector have been removed. They are not ways to test the current UI.
Engine/DOM durations and rAF cadence do not certify input-to-paint or presented
FPS; human task and publication review require actual independent observations.
