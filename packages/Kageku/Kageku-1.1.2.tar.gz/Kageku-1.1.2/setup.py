from setuptools import setup

with open('README.md') as f:
  long_description = f.read()

setup(
  name='Kageku',
  version='1.1.2',
  url='https://github.com/lucaspellegrinelli/kageku',
  license='MIT License',
  author='Lucas Pellegrinelli',
  author_email='lucas.pellegrinelli@hotmail.com',
  description='Implementation of a chess based game created by me and some friends for an RPG we play',
  long_description=long_description,
  long_description_content_type='text/markdown',
  packages=['kageku']
)
