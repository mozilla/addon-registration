import mozilla_sphinx_theme
import os

extensions = []
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'Addon registration'
copyright = u'2013, Mozilla Services'
version = '0.1'
release = '0.1'
exclude_patterns = ['_build']

pygments_style = 'sphinx'

html_theme_path = [os.path.dirname(mozilla_sphinx_theme.__file__)]

html_theme = 'mozilla'
html_static_path = ['_static']

htmlhelp_basename = 'Addonregistrationdoc'
