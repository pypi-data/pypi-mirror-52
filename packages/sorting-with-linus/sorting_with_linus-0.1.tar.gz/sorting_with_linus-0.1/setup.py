from setuptools import setup
from setuptools import find_packages

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sorting_with_linus',
    version='0.1',
    description='Just a few sorting algorithms, which you may find useful (or not).',
    url='https://gitlab.propulsion-home.ch/linus-ritzmann/week-3/day-4',
    author='Linus Ritzmann',
    author_email='linus.ritzmann@gmail.com',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.7'
)
