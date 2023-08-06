import codecs
from os import path
from io import open
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# read the dependencies from the requirements.txt file
with codecs.open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='toop',
    version='0.2',
    description='A Site Connectivity Checker for Mac',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Kisekk David',
    author_email='cartpix@gmail.com',
    url="https://github.com/Genza999/toop",
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='python requests monitor',

    packages=find_packages(),

    include_package_data=True,

    package_data={
        'toop': ['toop.dat'],
    },

    scripts=['toop/bin/toop_script.py'],

    install_requires=[
        'appdirs==1.4.3',
        'astroid==2.2.5',
        'autopep8==1.4.4',
        'certifi==2019.6.16',
        'chardet==3.0.4',
        'idna==2.8',
        'isort==4.3.21',
        'lazy-object-proxy==1.4.2',
        'mccabe==0.6.1',
        'pycodestyle==2.5.0',
        'pydbus==0.6.0',
        'pylint==2.3.1',
        'pynotify==0.1.1',
        'requests==2.22.0',
        'ruamel.yaml==0.16.5',
        'ruamel.yaml.clib==0.1.2',
        'six==1.12.0',
        'typed-ast==1.4.0',
        'urllib3==1.25.3',
        'wrapt==1.11.2',
        'termcolor==1.1.0',
        'pyfiglet==0.8.post1'
    ]

)
