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
import sphinx_rtd_theme

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

# The version identifier (major and minor only)
version = '0.1'
# The full release identifier, including alpha/beta/rc tags
release = '0.1.1a1'


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
    'recommonmark',
    'sphinx_rtd_theme',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    'django.log',
    'fpiweb.log',
    'root.log',
]

# options to specify what to include or exclude in the Sphinx output.

# Note - Apparently the Unittest library never uses Sphinx for documentation
# or the maintainers would have cleaned up the comments.

# Note - Apparently, just the presence of the key in the options dictionary
# is sufficient to enable the option.  Hence the options we don't want are
# commented out.
autodoc_default_options = {
    'members': True,                  # include members (default)
    'undoc-members': True,            # include members with no documentation
    'member-order': 'alphabetical',   # sort members alphabetically
    # 'private-members': None,          # document members beginning with "_"
    # 'special-members': None,          # document dunderbar members
    # 'inherited-members': None,        # show inherited members
    'show-inheritance': True,         # shows inheritance below signature
    # 'ignore-module-all': None,        # include __all__ member
    'exclude-members':
        'assertWarnsRegex, '
        'assertTupleEqual, '
        'assertRaisesRegex, '
        'assertListEqual, '
        'assertFieldOutput, '
        'assertSequenceEqual, '
        'assertSetEqual, '
        'prepare, '
        '_pre_setup, '
        '_post_teardown',             # exclude members in list
}

# allow markdown documents to be included via the recommonmark library
source_suffix = ['.rst', '.md']

# path to possible processing tool to convert images from one format to another
# image_converter = '/usr/local/bin/convert'

# automatically generate autodoc stub files for any new modules
autosummary_generate = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

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

# The following configures the Read-the-Docs theme.  See
# https://sphinx-rtd-theme.readthedocs.io/en/stable/index.html for details on
# configuration options.
html_theme_options = {
    'canonical_url': '',
    # 'analytics_id': 'UA-XXXXXXX-1',  #  Provided by Google in your dashboard
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    # 'vcs_pageview_mode': '',
    'style_nav_header_background': 'white',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
}

# EOF
