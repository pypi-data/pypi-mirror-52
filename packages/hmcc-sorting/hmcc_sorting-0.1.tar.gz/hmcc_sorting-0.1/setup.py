from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='hmcc_sorting',
      version='0.1',
      description='Package to sort lists',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='',
      author='hmcc',
      author_email='something@example.com',
      license='MIT',
      packages=['hmcc_sorting'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'])
