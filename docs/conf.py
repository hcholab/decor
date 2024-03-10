# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "bitween"
copyright = "2023, Ferhat Erata, Timos Antonopoulos"
author = "Ferhat Erata, Timos Antonopoulos"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.mathjax",
    "autoapi.extension",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.githubpages",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
]
autoapi_dirs = ["../src"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for myst -------------------------------------
# https://myst-parser.readthedocs.io/en/latest/syntax/admonitions.html
myst_enable_extensions = [
    "dollarmath",
    "amsmath",
    "strikethrough",
    "tasklist",
    "fieldlist",
    "attrs_inline",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
# html_theme = "pydata_sphinx_theme"

html_static_path = ["_static"]
