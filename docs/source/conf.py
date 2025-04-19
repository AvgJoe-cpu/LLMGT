import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'llmgt'
author = 'Jona'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',     # Extracts docs from Python docstrings
    'sphinx.ext.napoleon',    # Supports Google/NumPy style docstrings
    'sphinx.ext.viewcode',    # Adds links to your Python source code
    'sphinx.ext.autosummary', # Optional: creates summary tables
]
autosummary_generate = True  # Enables autosummary tables to be built


templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_options = {
    'collapse_navigation': False,  # sidebar stays open
    'navigation_depth': 4,         # deeper nesting visibility
}