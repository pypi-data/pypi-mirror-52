
from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='for.py',
    version='1.0.3',
    description='An async Python API wrapper for the Fortnite API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Akhil2149/forpy',
    author='Akhil',
    author_email='akhilaug2003@gmail.com',
    license='MIT',
    python_requires='>=3.6',
    keywords=['fortnite, forpy, api-wrapper, async'],
    packages=find_packages(),
    install_requires=['aiohttp', 'python-box','python_version>="3.6"']
)
