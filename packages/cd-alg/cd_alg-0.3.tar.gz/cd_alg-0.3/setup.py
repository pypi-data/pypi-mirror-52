from setuptools import setup


# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='cd_alg',
      version='0.3',
      description='algorithms package exercise',
      long_description=long_description,
      author='cdreek',
      author_email='cdreek@example.com',
      license='MIT',
      packages=['cdreek_algorithms'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False
)
