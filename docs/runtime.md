# Optional isolated CPU runtime

Static source analysis does not require PyTorch. CPU observation is a separate, explicitly requested workflow.

The current execution profile requires Linux x86-64, `/usr/bin/bwrap`, `/usr/bin/readelf`, working user/mount/pid/network namespaces, and seccomp. Install Bubblewrap and binutils with your system package manager. The runtime refuses execution when isolation is unavailable.

From the repository root, create a separate environment:

```bash
python3.11 -m venv .venv-runtime
.venv-runtime/bin/python -m pip install --require-virtualenv \
  --index-url https://download.pytorch.org/whl/cpu --no-deps 'torch==2.5.1+cpu'
.venv-runtime/bin/python -m pip install --require-virtualenv -r requirements-runtime.lock
PYTHONPATH=src .venv/bin/python -B -m archcanvas_cli capabilities
```

The service discovers `.venv-runtime/bin/python` and `requirements-runtime.lock` in this repository. Restart the service after installing or changing this environment. The rest of the application continues to work when this profile is unavailable.

Summary CPU observation uses an explicit `semantic-inputs/1` specification. Formal source transactions use their own input contracts. Inputs, modes, constructor values, seeds and cases must be declared for the chosen workflow; success applies only to the observed cases.

CLI example for the formal runtime:

```bash
PYTHONPATH=src .venv/bin/python -B -m archcanvas_cli runtime \
  --root fixtures/multi_input --entry model:MultiInputAttention \
  --input-spec fixtures/multi_input/input-spec.json \
  --interpreter "$PWD/.venv-runtime/bin/python" \
  --dependency-lock "$PWD/requirements-runtime.lock"
```
