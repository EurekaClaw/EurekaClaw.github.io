"""Sphinx configuration for EurekaClaw documentation."""

from __future__ import annotations

# -- Project information -------------------------------------------------------
project = "EurekaClaw"
copyright = "2026, EurekaClaw Contributors"
author = "EurekaClaw Contributors"
release = "0.1"

# -- General configuration -----------------------------------------------------
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinxcontrib.mermaid",
]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "tasklist",
    "attrs_inline",
    "fieldlist",
]
myst_heading_anchors = 4

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- HTML output ---------------------------------------------------------------
html_theme = "pydata_sphinx_theme"
html_title = "EurekaClaw"
html_logo = "_static/logo-claw.png"
html_favicon = "_static/logo-claw.png"
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]

html_theme_options = {
    "logo": {
        "text": "EurekaClaw",
        "image_light": "_static/logo.svg",
        "image_dark": "_static/logo.svg",
    },
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/EurekaClaw/EurekaClaw",
            "icon": "fa-brands fa-github",
        },
    ],
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["navbar-icon-links", "theme-switcher"],
    "navbar_persistent": ["search-button"],
    "primary_sidebar_end": ["sidebar-ethical-ads"],
    "secondary_sidebar_items": ["page-toc", "edit-this-page"],
    "footer_start": ["copyright"],
    "footer_end": ["sphinx-version"],
    "use_edit_page_button": True,
    "show_toc_level": 2,
    "navigation_depth": 4,
    "collapse_navigation": False,
    "show_nav_level": 1,
    "pygments_light_style": "tango",
    "pygments_dark_style": "monokai",
    "announcement": None,
}

html_context = {
    "github_user": "EurekaClaw",
    "github_repo": "EurekaClaw.github.io",
    "github_version": "main",
    "doc_path": "source",
}

html_sidebars = {
    "**": ["sidebar-nav-bs"],
}

# -- Copybutton ----------------------------------------------------------------
copybutton_prompt_text = r"\$ |>>> |\.\.\.  "
copybutton_prompt_is_regexp = True

# -- Autodoc -------------------------------------------------------------------
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
    "member-order": "bysource",
}
napoleon_google_docstring = True
napoleon_numpy_docstring = True

# -- Intersphinx ---------------------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# -- Mermaid -------------------------------------------------------------------
mermaid_version = "10.6.1"
