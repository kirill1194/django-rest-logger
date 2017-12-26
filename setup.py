from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='djangorestlogger',
    version='0.1',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=[
        'urllib3>=1.22',
        'Django>=1.8'
    ],
    include_package_data=True,
)