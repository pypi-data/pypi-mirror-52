from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pyLINQ',
      version='0.0.1',
      description='Adds the LINQ functionality to Python.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/jmfernandes/robin_stocks',
      author='Josh Fernandes',
      author_email='joshfernandes@mac.com',
      keywords=['LINQ'],
      license='MIT',
      python_requires='>=3',
      packages=find_packages(),
      requires=[],
      install_requires=[
      ],
      zip_safe=False)
