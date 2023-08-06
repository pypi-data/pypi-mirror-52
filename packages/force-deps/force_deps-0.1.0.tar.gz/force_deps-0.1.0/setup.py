from setuptools import setup, find_packages
from codecs import open
from os import path

# change from cookiecutter to always initialize with 0.1.0
__version__ = "0.1.0"

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# # get the dependencies and installs
# with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
#     all_reqs = f.read().split('\n')

install_requires = []
dependency_links = []

setup(
    name='force_deps',
    version=__version__,
    description='a small package for enforcing package requirements at the class- or function-level',
    long_description=long_description,
    url='https://github.com/maxblee/force_deps',
    download_url='https://github.com/maxblee/force_deps/tarball/' + __version__,
    license='BSD',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Max Lee',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='maxbmhlee@gmail.com'
)