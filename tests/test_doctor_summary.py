"""A compact Agent receipt must preserve the actual integrity decision."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from archcanvas_cli.doctor import diagnose
from archcanvas_cli.__main__ import main


class DoctorSummaryTests(unittest.TestCase):
    def test_compact_cli_retains_identity_and_checks_tampered_frozen_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            index = root / 'studio/dist/index.html'
            index.parent.mkdir(parents=True)
            index.write_text('<html>frozen</html>')
            (root / 'BUNDLE-MANIFEST.json').write_text(json.dumps({
                'schemaVersion': 1, 'product': 'archcanvas', 'kind': 'local-beta-preview',
                'version': '0.1.0-beta.4', 'files': [{
                    'path': 'studio/dist/index.html',
                    'bytes': index.stat().st_size,
                    'sha256': hashlib.sha256(index.read_bytes()).hexdigest()}]}))
            with patch('archcanvas_cli.server.project_root', return_value=root), \
                 patch('archcanvas_cli.doctor.module_catalog', return_value={'modules': ['atom']}), \
                 patch('archcanvas_cli.doctor.canvas_operation', return_value={'presets': 5}):
                full, compact = diagnose(), diagnose(summary=True)
                expected = {**full, 'studio': {k: v for k, v in full['studio'].items() if k != 'assets'}}
                self.assertEqual(compact, expected)
                self.assertEqual(compact['releaseIntegrity'], 'verified')
                self.assertEqual(compact['studio']['assetCount'], 1)
                index.write_text('<html>tampered</html>')
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    status = main(['doctor', '--summary'])
                failed = json.loads(output.getvalue())
                self.assertEqual(status, 2)
                self.assertEqual(failed['releaseIntegrity'], 'mismatch')
                self.assertEqual(failed['status'], 'incomplete')
                self.assertNotEqual(failed['studio']['digest'], compact['studio']['digest'])
                self.assertNotIn('assets', failed['studio'])

    def test_extra_missing_linked_or_malformed_inventory_cannot_be_verified(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            index = root / 'studio/dist/index.html'
            index.parent.mkdir(parents=True)
            index.write_text('<html>frozen</html>')
            row = {'path': 'studio/dist/index.html', 'bytes': index.stat().st_size,
                   'sha256': hashlib.sha256(index.read_bytes()).hexdigest()}
            valid = {'schemaVersion': 1, 'product': 'archcanvas', 'kind': 'local-beta-preview',
                     'version': '0.1.0-beta.7', 'files': [row]}
            manifest = root / 'BUNDLE-MANIFEST.json'
            manifest.write_text(json.dumps(valid))
            with patch('archcanvas_cli.server.project_root', return_value=root), \
                 patch('archcanvas_cli.doctor.canvas_operation', return_value={'presets': 1}):
                def rejected():
                    for summary in (False, True):
                        result = diagnose(summary=summary)
                        self.assertEqual(result['releaseIntegrity'], 'mismatch')
                        self.assertEqual(result['status'], 'incomplete')
                        self.assertEqual(result['distribution'], 'frozen-local-preview')
                extra = index.with_name('unexpected.js')
                extra.write_text('extra')
                rejected()
                extra.unlink()
                extra.symlink_to(index)
                rejected()
                extra.unlink()
                for invalid in ([], {}, {**valid, 'files': []}, {**valid, 'files': [row, row]},
                                {**valid, 'files': [{**row, 'path': '../outside'}]},
                                {**valid, 'files': [{**row, 'bytes': True}]},
                                {**valid, 'files': [{**row, 'path': 'missing'}]}):
                    manifest.write_text(json.dumps(invalid))
                    rejected()
                manifest.write_text('{broken JSON')
                rejected()
                manifest.write_text(json.dumps(valid))
                self.assertEqual(diagnose(summary=True)['releaseIntegrity'], 'verified')
