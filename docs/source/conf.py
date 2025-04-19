import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))

# -- Project information -----------------------------------------------------
project = 'llmgt'
author = 'Jona'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
]

autosummary_generate = True

templates_path = ['_templates']
exclude_patterns = []

# -- Theme setup -------------------------------------------------------------
html_theme = "furo"
html_theme_options = {
    # Sidebar options
    "sidebar_hide_name": False,   # Show project name in sidebar
    "navigation_with_keys": True, # Enable arrow-key navigation between pages

    # Theme switching
    "light_logo": "logo-light.png",
    "dark_logo": "logo-dark.png",

    # Custom colors and fonts for light mode
    "light_css_variables": {
        "color-brand-primary": "#007acc",
        "color-brand-content": "#1a5f85",
        "font-stack": "Inter, system-ui, sans-serif",
    },

    # Custom colors and fonts for dark mode
    "dark_css_variables": {
        "color-brand-primary": "#0df0ff",
        "color-brand-content": "#5bd6ff",
        "font-stack": "Inter, system-ui, sans-serif",
    }
}

# Optional: Keep static path for images, logos, etc.
html_static_path = ['_static']
