try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages
from io import open
from os import path

import pathlib
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# automatically captured required modules for install_requires in requirements.txt
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs \
                    if 'git+' not in x]
setup (
 name = 'LIM-cpu',
 description = 'Simple command line app for converting asm files to bin files for the LIM cpu',
 version = '1.0.1',
 packages = find_packages(), # list of all packages
 install_requires = install_requires,
 python_requires='>=3.9', # any python greater than 3.9
 entry_points='''
        [console_scripts]
        LIM-cpu=LIM.LIM:main
    ''',
 author="Henry Price",
 keyword="lim, asm, assembler, assembly, CPU",
 long_description=README,
 long_description_content_type="text/markdown",
 license='MIT',
 url='https://github.com/Spud304/LIM-Assembler',
 download_url='https://github.com/Spud304/LIM-Assembler/archive/1.0.6.tar.gz',
  dependency_links=dependency_links,
  author_email='hcprice115@gmail.com',
  classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ]
)