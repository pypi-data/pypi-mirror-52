"""The setup module for django_saml2_auth.
See:
https://github.com/fangli/django_saml2_auth
"""

from codecs import open
from os import path

from setuptools import (setup, find_packages)

import django_saml2_auth_metadata_inline

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django_saml2_auth_metadata_inline',

    version=django_saml2_auth_metadata_inline.__version__,

    description='Inline metadata plugin for django-saml2-auth',
    long_description=long_description,

    url='https://github.com/ambsw/django-saml2-auth-metadata-inline',

    author='Clayton Daley',
    author_email='technology+saml2_metadata_plugin@gmail.com',

    license='Apache 2.0',

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: Apache Software License',

        'Framework :: Django :: 1.5',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='Django SAML2 Plugin for Inline Metadata',

    packages=find_packages(),

    install_requires=['django_saml2_auth',
                      ],
    include_package_data=True,
)
