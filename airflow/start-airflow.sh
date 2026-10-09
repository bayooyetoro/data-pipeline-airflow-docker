#!/usr/bin/env bash
set -euo pipefail

python - <<'PY'
import json
import os
from pathlib import Path

username = os.environ["AIRFLOW_ADMIN_USERNAME"]
password = os.environ["AIRFLOW_ADMIN_PASSWORD"]
password_file = Path(os.environ["AIRFLOW__CORE__SIMPLE_AUTH_MANAGER_PASSWORDS_FILE"])
password_file.write_text(json.dumps({username: password}), encoding="utf-8")
password_file.chmod(0o600)
PY

airflow db migrate
exec airflow standalone
