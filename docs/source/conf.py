""" Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
http://www.sphinx-doc.org/en/master/config
"""

import os
import sys

import django

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# sys.path.insert(0, os.path.abspath('.'))

# Work our way back up from the source directory to the project level so
# Django can find its settings file.

# absolute path to conf.py including name
full_path_w_filename = os.path.abspath(__file__)

# full path to direcctory containing conf.py ( = source)
directory_containing_file = os.path.dirname(full_path_w_filename)

# Full path to directory containing soure directory ( = docs)
parent_directory = os.path.dirname(directory_containing_file)

# directory containing docs directory ( = project directory)
BASE_DIR = os.path.dirname(parent_directory)

# Supposed to be: /Volumes/MBPC/Dvl/Python/PythonProjects/Food-Pantry-Inventory

# directory containing our Django application
django_app_directory = os.path.join(BASE_DIR, 'fpiweb/')

# now add both to the system PATH
sys.path.insert(0, BASE_DIR)
sys.path.insert(1, django_app_directory)

# set the environment variable that Django code looks for
os.environ['DJANGO_SETTINGS_MODULE'] = 'FPIDjango.settings'

# Invoke Django code to establish its environment
from django.conf import settings
settings.configure()
django.setup()

# -- Project information -----------------------------------------------------

project = 'Food Pantry Inventory System'
copyright = '2019, (See Contributors.md)'
author = '(See Contributors.md)'

# The full version, including alpha/beta/rc tags
release = '0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinxcontrib.plantuml'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Title appended to any title for each HTML page generated.
html_title = "Food Pantry Inventory"

# Shorter title used when needed.
htmo_short_title = "Inventory"

# Date stamp each page of documentation.  (Empty string used default format.)
html_last_updated_fmt = ""

# EOF
