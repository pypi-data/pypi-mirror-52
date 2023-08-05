import re
from pathlib import Path
from setuptools import setup, find_packages

txt = Path('qeh/__init__.py').read_text()
version = re.search("__version__ = '(.*)'", txt).group(1)

long_description = Path('README.md').read_text()

setup(
    name='qeh',
    version=version,
    description='Quantum Electrostatic Heterostructure Model',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='CAMD',
    author_email='mogje@fysik.dtu.dk',
    url='https://gitlab.com/camd/qeh',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['ase'],
    extras_require={'docs': ['sphinx', 'sphinxcontrib-programoutput']},
    entry_points='''
        [console_scripts]
        qeh=qeh.qeh:main
    ''',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Physics'
    ])
