from io import open  # For python2 compatibility
from os import path
from setuptools import setup


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='raho',
    version='0.0.1',
    description='Simple symmetric encryption built on cryptography',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/abhayagiri/raho',
    author='Abhayagiri Dev Monk',
    author_email='devmonk@abhayagiri.org',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='cryptography fernet',
    py_modules=['raho'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    install_requires=['cryptography'],
    setup_requires=['wheel'],
    extras_require={
        'test': ['tox'],
    },
    entry_points={
        'console_scripts': [
            'raho=raho:main',
        ],
    },
)
