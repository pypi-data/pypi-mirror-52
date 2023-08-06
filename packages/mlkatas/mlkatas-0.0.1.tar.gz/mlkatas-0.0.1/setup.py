"""Setup for the mlkatas package."""

import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Baptiste  Pesquet",
    author_email="bpesquet@gmail.com",
    name='mlkatas',
    license="MIT",
    description='Utility functions for Machine Learning',
    version='0.0.1',
    long_description=README,
    url='https://github.com/bpesquet/mlkatas',
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=['numpy', 'matplotlib'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)
