import os
from codecs import open

from setuptools import setup, find_packages


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
VERSION = __import__('template_helpers').__version__


with open(os.path.join(BASE_DIR, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='django-template-helpers',
    version=VERSION,
    description=(
        'django-template-helpers provides template tags to add missing '
        'features to the Django template language.'
    ),
    long_description=long_description,
    url='https://github.com/moccu/django-template-helpers',
    project_urls={
        'Bug Reports': 'https://github.com/moccu/django-template-helpers/issues',
        'Source': 'https://github.com/moccu/django-template-helpers',
    },
    author='Moccu GmbH & Co. KG',
    author_email='info@moccu.com',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[],
    include_package_data=True,
    keywords='django templates',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
