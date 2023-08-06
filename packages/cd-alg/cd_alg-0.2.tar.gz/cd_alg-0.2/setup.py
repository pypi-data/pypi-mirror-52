from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='cd_alg',
      version='0.2',
      description='algorithms package exercise',
      long_description=readme(),
      author='cdreek',
      author_email='cdreek@example.com',
      license='MIT',
      packages=['cdreek_algorithms'],
      install_requires=[
          'markdown',
      ],
      zip_safe=False
)
