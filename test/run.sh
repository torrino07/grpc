#!/bin/bash
uv lock
uv venv
source .venv/bin/activate
uv run python test.py
