"""Vercel entrypoint for the Dash dashboard."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from dashboard import app as dash_app  # noqa: E402

# Vercel Python runtime expects a WSGI app exposed as `app`.
app = dash_app.server
