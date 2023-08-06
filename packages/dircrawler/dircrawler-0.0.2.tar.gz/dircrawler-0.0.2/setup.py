from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='dircrawler',
    version='0.0.2',
    description='General purpose crawler',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='mhaisham',
    author_email='mhaisham79@gmail.com',
    packages=find_packages(),
    python_requires='>=3.6'
)