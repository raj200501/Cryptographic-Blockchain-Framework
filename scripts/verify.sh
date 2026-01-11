#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

missing=$(python - <<'PY'
import importlib.util

required = ["pytest"]
missing = [pkg for pkg in required if importlib.util.find_spec(pkg) is None]
print(" ".join(missing))
PY
)

if [[ -n "$missing" ]]; then
  echo "Installing missing dependencies: $missing"
  python -m pip install -r requirements.txt
fi

export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
python -m pytest
