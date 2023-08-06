from os import path

from setuptools import setup, find_packages

from ldrand.cli import VERSION

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ldrand',
    author="Johannes Bechberger",
    author_email="me@mostlynerdless.de",
    description="Link order randomizing linker wrapper",
    long_description=long_description,
    url="https://github.com/parttimenerd/ldrand",
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    tests_require=['pytest'],
    license='GPLv3',
    platforms='linux',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Benchmark",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        'Intended Audience :: Developers',

    ],
    entry_points='''
        [console_scripts]
        ldrand=ldrand.cli:run
        ldrandp=ldrand.cli:runp
    '''
)
