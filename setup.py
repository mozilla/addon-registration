import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

with open(os.path.join(here, 'CHANGES.rst')) as f:
    CHANGES = f.read()


requires = ['cornice', 'pyramid']


setup(name='addonreg',
      version='0.1',
      packages=find_packages(),
      include_package_data=True,
      description='',
      long_description=README + '\n\n' + CHANGES,
      zip_safe=False,
      license='APLv2.0',
      classifiers=["Programming Language :: Python", ],
      install_requires=requires,
      author='Mozilla Services',
      author_email='services-dev@mozilla.org',
      url='https://github.com/mozilla-services/addonreg',
      tests_require=['nose', 'mock', 'unittest2'],
      test_suite='nose.collector',
      entry_points={'paste.app_factory': ['main = addonreg:main']})
