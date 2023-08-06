from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='extools',
    version='0.1.1',
    description='Tools for Orchid Extender',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://2665093.ca',
    author='Chris Binckly, 2665092 Ontario Inc.',
    author_email='cbinckly@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    keywords='sage orchid extender',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='=3.4.*',
    install_requires=[],
    extras_require={
    },
    package_data={
    },
)

