
"""Setup for the chocobo package."""

import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Preflet",
    author_email="preflet@outlook.com",
    name='preflet',
    license="MIT",
    description='The official Python SDK to go along with Preflet.',
    version='v0.0.1',
    long_description=README,
    url='https://www.preflet.com',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=['requests', 'scikit-learn',
                      'pandas', 'tabulate', 'pycryptodome'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)
