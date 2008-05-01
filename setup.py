from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='keytree',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[],
      keywords='',
      author='Sean Gillies',
      author_email='sgillies@frii.com',
      url='',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      test_suite='keytree.tests.test_suite',
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
