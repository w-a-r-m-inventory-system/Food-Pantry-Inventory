""" Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
http://www.sphinx-doc.org/en/master/config
"""

import os
import shutil
import sys

import django
import recommonmark

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

# full path to directory containing conf.py ( = source)
directory_containing_conf = os.path.dirname(full_path_w_filename)

# Full path to directory containing source directory ( = docs)
parent_directory = os.path.dirname(directory_containing_conf)

# directory containing docs directory ( = project directory)
BASE_DIR = os.path.dirname(parent_directory)

# Supposed to be: /.../Food-Pantry-Inventory

# directory containing our Django application
django_app_directory = os.path.join(BASE_DIR, 'fpiweb/')

# Ensure private settings file exists before attempting docs build
private_settings_module_path = os.path.join(BASE_DIR, 'FPIDjango', 'private')
private_settings_file_path = os.path.join(private_settings_module_path, 'settings_private.py')
if not os.path.exists(private_settings_file_path):
    if not os.path.exists(private_settings_module_path):
        os.mkdir(private_settings_module_path)
    shutil.copy(
        os.path.join(BASE_DIR, 'FPIDjango', 'settings_private.py'),
        private_settings_file_path
    )

# Tell Sphinx to ignore Django imports
# autodoc_mock_imports = ["django"]

# now add both to the system PATH
sys.path.insert(0, BASE_DIR)
sys.path.insert(1, django_app_directory)

# set the environment variable that Django code looks for
os.environ['DJANGO_SETTINGS_MODULE'] = 'FPIDjango.settings'

# Invoke Django code to establish its environment
django.setup()

# -- Project information -----------------------------------------------------

project = 'Food Pantry Inventory System'
copyright = '2020, (See Contributors)'
author = '(See Contributors)'

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
    'sphinxcontrib.plantuml',
    'recommonmark'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'django.log',
                    'fpiweb.log', 'root.log', ]


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
html_short_title = "Inventory"

# Date stamp each page of documentation.  (Empty string used default format.)
html_last_updated_fmt = ""

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = os.path.join('_static', 'Food_Pantry_Logo.jpg')

# EOF
