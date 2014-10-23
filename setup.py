from setuptools import setup, find_packages
import sys, os

version = '.1'

setup(name='duedil',
      version=version,
      description="Duedil API client",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='duedil, api',
      author='Christian Ledermann',
      author_email='christian.ledermann@gmail.com',
      url='https://github.com/founders4schools/duedil',
      license='Apache License 2.0',
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
