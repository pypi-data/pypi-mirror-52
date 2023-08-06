from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(name='sorting_joany_h_k',
      version='0.1',
      description='Sorting algorithm from Propulsion',
      url='http://github.com/storborg/funniest',
      author='J. Hernandez',
      author_email='joany.hernandez.kong@gmail.com',
      license='MIT',
      packages=['sorting_joany_h_k'],
      zip_safe=False,
      long_description=long_description,
      long_description_content_type='text/markdown')
