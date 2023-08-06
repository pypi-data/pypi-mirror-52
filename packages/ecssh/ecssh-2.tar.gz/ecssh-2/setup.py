from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='ecssh',
      version='2',
      description='accessing aws ecs instances',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://git.osuv.de/m/ecssh',
      author='Markus Bergholz',
      author_email='markuman@gmail.com  ',
      license='WTFPL',
      packages=['ecssh'],
      scripts=['bin/ecssh'],
      zip_safe=True)
