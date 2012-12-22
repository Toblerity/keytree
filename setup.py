from setuptools import setup, find_packages
import sys, os

version = '0.2.1'
try:
    desc = open('README.rst', 'r').read()
except:
    desc = ''

setup(name='keytree',
      version=version,
      description="KML utilities for the ElementTree API",
      long_description=desc,
      classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS',
        ],
      keywords='KML etree ElementTree',
      author='Sean Gillies',
      author_email='sgillies@frii.com',
      url='http://atlantides.org/svn/pleiades/pleiades.keytree',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
