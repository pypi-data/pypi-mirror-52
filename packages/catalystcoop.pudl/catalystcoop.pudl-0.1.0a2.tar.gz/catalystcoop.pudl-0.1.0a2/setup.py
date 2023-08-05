#!/usr/bin/env python
"""Setup script to make PUDL directly installable with pip."""

from pathlib import Path

from setuptools import find_packages, setup

install_requires = [
    'coloredlogs',
    'datapackage',
    'dbfread',
    'goodtables',
    'matplotlib',
    'networkx>=2.2',
    'numpy',
    'pandas>=0.24',
    'psycopg2',
    'pyyaml',
    'scikit-learn>=0.20',
    'scipy',
    'sqlalchemy>=1.3.0',
    'tableschema',
    'tableschema-sql',
    'timezonefinder',
    'xlsxwriter',
]

doc_requires = [
    'doc8',
    'sphinx',
    'sphinx_rtd_theme',
]

test_requires = [
    'bandit',
    'coverage',
    'doc8',
    'flake8',
    'flake8-docstrings',
    'flake8-builtins',
    'pep8-naming',
    'pre-commit',
    'pydocstyle',
    'pytest',
    'pytest-cov',
]

validate_requires = [
    'matplotlib',
    'nbval',
]

parquet_requires = [
    'pyarrow>=0.14.0',
    'python-snappy'
]

readme_path = Path(__file__).parent / "docs" / "README.rst"
long_description = readme_path.read_text()


setup(
    name='catalystcoop.pudl',
    description='An open data processing pipeline for public US utility data.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    use_scm_version=True,
    author='Catalyst Cooperative',
    author_email='pudl@catalyst.coop',
    maintainer='Zane A. Selvans',
    maintainer_email='zane.selvans@catalyst.coop',
    url="https://catalyst.coop/pudl",
    project_urls={
        "Source": "https://github.com/catalyst-cooperative/pudl",
        "Documentation": "https://catalystcoop-pudl.readthedocs.io",
        "Issue Tracker": "https://github.com/catalyst-cooperative/pudl/issues",
    },
    license='MIT',
    keywords=[
        'electricity', 'energy', 'data', 'analysis', 'mcoe', 'climate change',
        'finance', 'eia 923', 'eia 860', 'ferc', 'form 1', 'epa ampd',
        'epa cems', 'coal', 'natural gas', ],
    python_requires='>=3.7, <3.8.0a0',
    setup_requires=['setuptools_scm'],
    install_requires=install_requires,
    extras_require={
        "doc": doc_requires,
        "parquet": parquet_requires,
        "test": test_requires,
        "validate": validate_requires,
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    # package_data is data that is deployed within the python package on the
    # user's system. setuptools will get whatever is listed in MANIFEST.in
    include_package_data=True,
    # This defines the interfaces to the command line scripts we're including:
    entry_points={
        'console_scripts': [
            'pudl_data = pudl.workspace.datastore_cli:main',
            'pudl_setup = pudl.workspace.setup_cli:main',
            'pudl_etl = pudl.cli:main',
            'ferc1_to_sqlite = pudl.convert.ferc1_to_sqlite:main',
            'epacems_to_parquet = pudl.convert.epacems_to_parquet:main [parquet]',  # noqa: E501
        ]
    },
)
