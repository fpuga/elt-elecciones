#!/bin/bash
set -euo pipefail

this_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && pwd)"

mkdir -p "${this_dir}/../back/data/"
