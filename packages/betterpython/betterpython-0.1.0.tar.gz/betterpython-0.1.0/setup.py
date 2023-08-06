from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='betterpython',
      version='0.1.0',
      description='Improves on the behavior of python',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      url='https://github.com/jmfernandes/pyLINQ',
      author='Josh Fernandes',
      author_email='joshfernandes@mac.com',
      keywords=['LINQ', 'better', 'python'],
      license='MIT',
      python_requires='>=3.4',
      packages=find_packages(),
      requires=[],
      install_requires=[
      ],
      zip_safe=False)
