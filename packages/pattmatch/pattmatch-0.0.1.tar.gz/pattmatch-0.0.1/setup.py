from setuptools import setup, find_packages
from os import path

readme_folder = path.abspath(path.dirname(__file__))

with open(path.join(readme_folder, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pattmatch',
    version='0.0.1',
    description='Implementation of some pattern matching algorithms',
    long_description=long_description,
    url='https://github.com/monzita/pattmatch',
    author='Monika Ilieva',
    author_email='hidden@hidden.com',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'Programming Language :: Python :: 3.6'
    ],
    license='GNU General Public License v3 or later (GPLv3+)',
    keywords='pattern-matching text string pattern python3 boyer moore rabin karp kmp',
    packages=find_packages(exclude=['contrib', 'tests', 'venv']),
)