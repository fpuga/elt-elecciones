#!/bin/bash
set -euo pipefail

# --cov-report html
pytest --log-cli-level=Warning back --cov=back --cov-report=term-missing:skip-covered --cov-branch --no-cov-on-fail -m "not slow"
