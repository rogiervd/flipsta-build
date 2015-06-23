# Configuration file for the Sphinx documentation generator.
# This picks up values from ../documentation_configuration.py.
# This gets copied to conf.py in the output directory and then picked up by
# Sphinx.

import sys, os

sys.path.insert (1, '../..')
import documentation_configuration

# To install Breathe, by downloading it, extracting it, cd-ing into the
# directory,
# and saying
#   python setup.py build
#   python setup.py install --user
extensions = ['sphinx.ext.pngmath', 'sphinx.ext.todo', 'breathe']

source_suffix = '.rst'

master_doc = 'index'
project = documentation_configuration.mainProjectName
copyright = documentation_configuration.copyright
version = documentation_configuration.version
release = documentation_configuration.release

pygments_style = 'sphinx'
html_theme = 'nature'
templates_path = ['_templates']

# Options for Breathe.
breathe_projects = { documentation_configuration.mainProject: "../doxygen/xml" }
breathe_default_project = documentation_configuration.mainProject
