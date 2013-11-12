import os
from paste.deploy import loadapp

ini_file = os.environ.get('CONFIG', 'production.ini')
config_dir = os.path.abspath(os.path.dirname(ini_file))
app = loadapp('config:%s' % ini_file, relative_to=config_dir)
