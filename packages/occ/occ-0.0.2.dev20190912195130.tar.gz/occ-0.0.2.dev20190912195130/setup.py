
from setuptools import setup, find_packages
from occ.core import version

VERSION = version.get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='occ',
    version=VERSION,
    description='Octavia Chicken Checker looks for abandoned Octavia load balancer artifacts, amphoras, and so forth. Optionally it will clean them up as well.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Cody Bunch',
    author_email='cody.bunch@rackspace.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
    ],
    url='http://github.com/bunchc/octvia_chicken_checker/',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'occ': ['templates/*']},
    include_package_data=True,
    install_requires=[
        'cement==3.0.4',
        'jinja2',
        'pyyaml',
        'colorlog',
    ],
    entry_points="""
        [console_scripts]
        occ = occ.main:main
    """,
)
