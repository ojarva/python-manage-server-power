from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='manage_server_power',
    version='0.0.1',
    description='Small library for shutting down and starting up local server',
    long_description=long_description,
    url='https://github.com/ojarva/python-manage-server-power',
    author='Olli Jarva',
    author_email='olli@jarva.fi',
    license='BSD',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    keywords='wol wake-on-lan',
    packages=["manage_server_power"],
    test_suite="tests",
    install_requires=['wakeonlan', 'paramiko'],

    extras_require = {
        'dev': ['twine', 'wheel'],
    },
)
