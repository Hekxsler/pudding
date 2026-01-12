"""Sphinx configuration for pudding docs.

This is a minimal, sensible default config that reads project metadata
from the package where possible. It aims to be portable for local
documentation builds and CI.
"""

import importlib
import os
import sys
from typing import Any

# -- Path setup --------------------------------------------------------------
# Add project root so autodoc can import the package.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)


# -- Project information -----------------------------------------------------
project_module = importlib.import_module("pudding")
project = getattr(project_module, "__name__", "pudding")
author = ", ".join(
    [a.get("name") or "" for a in getattr(project_module, "__authors__", [])]
) or getattr(project_module, "__author__", "Moritz Hille")
try:
    release = getattr(project_module, "__version__")
except Exception:
    release = "Unknown"

# -- General configuration ---------------------------------------------------
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_rtd_theme",
]

templates_path = ["_templates"]
exclude_patterns: list[str] = ["_build", "Thumbs.db", ".DS_Store"]

# Allow Markdown as source. The MyST parser will handle `.md` files.
# `root_doc` is the Sphinx 4+ name for the master document; set both
# for compatibility with older Sphinx versions.
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
root_doc = "index"
master_doc = "index"

# Optional MyST settings (small, safe defaults)
myst_enable_extensions = [
    "deflist",
]

autodoc_typehints = "description"
autodoc_member_order = "bysource"


# -- Options for HTML output -------------------------------------------------
html_theme = os.environ.get("SPHINX_THEME", "sphinx_rtd_theme")
html_static_path = ["_static"]


def setup(app: Any) -> None:  # pragma: no cover - trivial glue
    """Sphinx setup hook.

    Keep this small — used mostly for extension registration if needed.
    """
    # allow linking to the source repository easily
    app.add_config_value("project_release", release, "env")
