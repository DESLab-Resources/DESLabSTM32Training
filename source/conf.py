# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# 
import os,sys
sys.path.insert(0,os.path.abspath('../..'))

project = 'DESLab STM32 Training'
copyright = '2024, Thanh Nguyen-Vu-Minh'
author = 'Thanh Nguyen-Vu-Minh'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel'
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"

# -- Options for EPUB output
epub_show_urls = 'footnote'

html_static_path = ['_static']

pygments_style = 'sphinx'
numfig = True
numfig_format = {
    'code-block': 'Code Block %s'
}
autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = True