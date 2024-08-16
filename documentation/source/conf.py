# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'SWAP-IT Execution Engine'
copyright = '2024, Fraunhofer IOSB Author (Florian Düwel)'
author = 'Fraunhofer IOSB Author (Florian Düwel)'
release = '0.9.9'

html_theme_options = {
    "collapse_navigation": True,
    'sticky_navigation': False,
    "navigation_depth": 6
}


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.intersphinx',
              'sphinx.ext.autosectionlabel',
              'rst2pdf.pdfbuilder']

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']



pdf_documents = [('index', u'SWAP-IT Demonstration Scenario', u'SWAP-IT Demonstration Scenario', u'Fraunhofer IOSB (Author: Florian Düwel)'),]
