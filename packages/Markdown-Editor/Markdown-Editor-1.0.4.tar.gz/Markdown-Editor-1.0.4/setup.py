#!/usr/bin/env python
import os
import re
import codecs
from os import path

from setuptools import setup

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

install_reqs = parse_requirements('requirements.txt')
reqs = [str(ir) for ir in install_reqs]

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with codecs.open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

data_dirs = ['markdown_editor/libs', 'markdown_editor/css', 'markdown_editor/js']
data_files = ['markdown_editor/markdown_edit.tpl']

r = re.compile('^markdown_editor/')
datafiles = []
for data_dir in data_dirs:
    datafiles.extend(r.sub('', d) + '/' + f for d, _, files in os.walk(data_dir) if files for f in files)

datafiles.extend(r.sub('', f) for f in data_files)

setup(name='Markdown-Editor',
      version='1.0.4',
      description='Standalone editor for your markdown files',
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
      author='Nicolas Cornette',
      author_email='nicolas.cornette@gmail.com',
      url='https://github.com/ncornette/Python-Markdown-Editor.git',
      install_requires=reqs,
      packages=['markdown_editor'],
      py_modules=['markdown_edit'],
      package_data={'markdown_editor': datafiles},
      entry_points={
          'console_scripts': [
              'markdown_edit = markdown_edit:main'
          ]
      }
      )
