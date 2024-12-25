# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


import os
import sys

# Add the root directory of the project to the Python path
sys.path.insert(0, os.path.abspath("../"))

project = "safe-pfl-distance"
copyright = "2024, MohammadMojtaba Roshani"
author = "MohammadMojtaba Roshani"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
]
templates_path = ["templates"]
exclude_patterns = [
    "build",
    "Thumbs.db",
]

autodoc_mock_imports = ["torch", "scipy", "numpy"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
htmlstatic_path = ["static"]
