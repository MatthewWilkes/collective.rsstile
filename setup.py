# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.0'
description = 'A tile giving advanced RSS feed options '
long_description = (
    open('README.md').read()
)

setup(name='collective.rsstile',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Framework :: Plone',
          'Framework :: Plone :: 4.2',
          'Framework :: Plone :: 4.3',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='plone tile rss',
      author='Matthew Wilkes et al.',
      author_email='matt@matthewwilkes.name',
      url='https://github.com/collective/collective.rsstile',
      license='GPLv2',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'plone.api',
          'plone.app.blocks',

      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
