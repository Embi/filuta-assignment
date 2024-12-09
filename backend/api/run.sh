#!/bin/bash

# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail

uvicorn api.main:app --workers ${API_WORKERS:-1} --host 0.0.0.0 --port 8000
