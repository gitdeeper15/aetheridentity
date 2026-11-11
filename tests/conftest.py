"""Pytest configuration for AetherIdentity tests."""

import sys
from pathlib import Path

# Make src/ importable without installing the package.
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))
