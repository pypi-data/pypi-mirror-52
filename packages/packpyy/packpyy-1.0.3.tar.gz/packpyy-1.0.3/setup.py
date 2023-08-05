
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_args = dict(
   name='packpyy',
   version='1.0.3',
   description='Een test pippackage voor project',
   license='MIT',
   packages=find_packages(),
   author='Mark Rozing',
   author_email='asjen@live.nl',
   keywords=['test'],
)
if __name__ == '__main__':
   setup(**setup_args)