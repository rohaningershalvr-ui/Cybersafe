# CyberSafe

A lightweight, local file-integrity monitoring and
security-review tool written in Python.

## Features

- Calculate SHA-256 file fingerprints
- Flag selected file extensions for manual review
- Generate JSON scan reports
- Save file-integrity baselines
- Detect added, modified, and removed files
- Run automated unit tests
- Works locally in Termux and Python environments

## Requirements

- Python 3.10 or newer
- No third-party Python packages required

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python scanner.py test_files
python dashboard.py
python baseline.py test_files --save baseline.json
python baseline.py test_files --compare baseline.json \
  --save baseline-latest.json
python compare.py baseline.json baseline-latest.json
python -m unittest -v
