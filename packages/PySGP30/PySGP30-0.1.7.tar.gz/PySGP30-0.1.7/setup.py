#!/usr/bin/env python3
import setuptools

with open('README.md', 'r') as f:
    readme = f.read()

setuptools.setup(
    name='PySGP30',
    description='Library for reading data from the Sensirion SGP30',
    version='0.1.7',
    author='Connor Kneebone',
    author_email='connor@sfxrescue.com',
    url='https://github.com/Conr86/PySGP30',
    license='MIT',
    packages=setuptools.find_packages(exclude=('tests')),
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=['smbus2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='sgp30 i2c smbus smbus2',
)
