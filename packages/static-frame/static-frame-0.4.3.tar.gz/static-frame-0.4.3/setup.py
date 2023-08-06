# Always prefer setuptools over distutils
from setuptools import setup  # type: ignore
# To use a consistent encoding
from codecs import open
from os import path

# https://packaging.python.org/distributing/
# to deploy:
# pip install wheel, twine
# python setup.py sdist
# python setup.py bdist_wheel
# twine upload dist/*
# rm -r build; rm -r dist; rm -r *.egg-info

# in /static-frame-feedstock/recipe
# update meta.yaml in feedstock: set version and tar sha256 for tar, commit and push
# submit PR to conda-forge/static-frame-feedstock from fork
# merge into conda forge feedstock after all checks pass

root_dir_fp = path.abspath(path.dirname(__file__))

def get_long_description() -> str:
#     with open(path.join(root_dir_fp, 'README.rst'), encoding='utf-8') as f:
#         return f.read()
    return '''The StaticFrame library consists of the Series and Frame, immutable data structures for one- and two-dimensional calculations with self-aligning, labelled axes. StaticFrame meets the need for an immutable Pandas DataFrame with a consistent, functional interface. While many interfaces are similar to Pandas, StaticFrame deviates from Pandas in many ways: all data is immutable, and indices are always unique; the full range of NumPy data types is preserved, and date-time indices use discrete NumPy types; hierarchical indices are seamlessly integrated; and flexible approaches to element, row, and column iteration and function application are provided in a uniform interface.

Code: https://github.com/InvestmentSystems/static-frame

Docs: http://static-frame.readthedocs.io

Packages: https://pypi.org/project/static-frame
'''

def get_version() -> str:
    with open(path.join(root_dir_fp, 'static_frame', '__init__.py'), encoding='utf-8') as f:
        for l in f:
            if l.startswith('__version__'):
                if '#' in l:
                    l = l.split('#')[0].strip()
                return l.split('=')[-1].strip()[1:-1]
    raise ValueError("__version__ not found!")

setup(
    name='static-frame',
    version=get_version(),
    description='Immutable structures for one- and two-dimensional calculations with labelled axes',
    long_description=get_long_description(),
    python_requires='>3.6.0',
    install_requires=['numpy>=1.14.2'],
    url='https://github.com/InvestmentSystems/static-frame',
    author='Christopher Ariza',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development',
            'License :: OSI Approved :: MIT License',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            ],

    keywords='staticframe pandas numpy immutable array',
    packages=[
            'static_frame',
            'static_frame.core',
            'static_frame.performance',
            ],
)
