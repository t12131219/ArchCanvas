#!/usr/bin/env python3
"""Check the compact source distribution's live assets without model execution."""
from __future__ import annotations

import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / 'studio/public/preview'


def existing(base: Path, relative: str) -> Path:
    path = (base / relative).resolve()
    if not path.is_relative_to(PREVIEW.resolve()) or not path.is_file():
        raise ValueError(f'Missing or invalid runtime asset: {relative}')
    return path


def read(base: Path, relative: str):
    return json.loads(existing(base, relative).read_text(encoding='utf-8'))


def pinned(base: Path, reference: dict) -> Path:
    path = existing(base, reference['path'])
    data = path.read_bytes()
    if len(data) != reference['bytes'] or hashlib.sha256(data).hexdigest() != reference['sha256']:
        raise ValueError(f'Runtime asset size/hash mismatch: {path.relative_to(ROOT)}')
    return path


class Entries(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        value = values.get('src') if tag == 'script' else values.get('href') if tag in {'link', 'a'} else None
        if value and not value.startswith(('#', 'http:', 'https:', 'data:', '/')):
            self.assets.append(value.split('?', 1)[0].split('#', 1)[0])


def check() -> dict:
    html = PREVIEW / 'yworks_edge_router_lab/index.html'
    parser = Entries()
    parser.feed(html.read_text(encoding='utf-8'))
    for relative in parser.assets:
        existing(html.parent, relative)
    worker = html.parent / 'routing-worker.js'
    for call in re.findall(r'importScripts\(([^)]*)\)', worker.read_text(encoding='utf-8')):
        for relative in re.findall(r"['\"]([^'\"]+)['\"]", call):
            existing(worker.parent, relative)

    semantic = PREVIEW / 'data/semantic'
    models = read(semantic, 'studio-catalog.json')['models']
    for model in models:
        ir = json.loads(pinned(semantic, model['ir']).read_text(encoding='utf-8'))
        if ir['ir_digest'] != model['digest'] or len(ir['nodes']) != model['nodes'] or len(ir['edges']) != model['edges']:
            raise ValueError(f'Model identity/accounting mismatch: {model["id"]}')
        if model.get('presentation'):
            pinned(semantic, model['presentation'])
    existing(semantic, 'authoring-presets.json')

    components = PREVIEW / 'data/source-components'
    families = read(components, 'index.json')['families']
    variants = set()
    for family in families:
        for variant in family['variants']:
            pinned(components, variant)
            variants.add(variant['path'])

    catalog = read(PREVIEW, 'data/summary-cases.json')
    script = existing(PREVIEW, 'data/summary-cases.js').read_text(encoding='utf-8').strip()
    if json.loads(script.removeprefix('window.SummaryCatalog=').removesuffix(';')) != catalog:
        raise ValueError('Browser and JSON case catalogs differ')
    sources = read(PREVIEW, 'data/catalog-sources.json')['cases']
    case_assets = set()
    for case in catalog['cases']:
        for view in case['views'] + case.get('routeTemplates', []):
            for key in ('asset', 'json', 'svg', 'ir'):
                if view.get(key):
                    existing(PREVIEW, view[key])
                    case_assets.add(view[key])
            if view.get('json'):
                graph = read(PREVIEW, view['json'])
                for key in ('source', 'layoutSource', 'irSource'):
                    if graph.get(key):
                        existing(PREVIEW, graph[key])
                for relative in graph.get('sourceDocs', {}).values():
                    existing(PREVIEW, relative)
        descriptor = sources[case['id']]
        if descriptor.get('evidence'):
            existing(PREVIEW, descriptor['evidence'])
        for source in descriptor.get('files', []) + descriptor.get('licenses', []):
            path = existing(PREVIEW, source['asset'])
            if hashlib.sha256(path.read_bytes()).hexdigest() != source['sha256']:
                raise ValueError(f'Source hash mismatch: {source["asset"]}')
    existing(PREVIEW, 'data/examples/river-net.json')
    return {'models': len(models), 'componentFamilies': len(families), 'componentVariants': len(variants),
            'cases': len(catalog['cases']), 'caseAssets': len(case_assets), 'htmlEntries': len(parser.assets)}


if __name__ == '__main__':
    print(json.dumps(check(), ensure_ascii=False))
