#!/usr/bin/env python

from setuptools import setup, find_namespace_packages
from setuptools.command.install import install
import re

VERSION='0.2'

RE_BLANCK=re.compile(r"^\s*#?")
with open('requirements.txt') as f:
    requirements = [x for x in f.read().splitlines() if not RE_BLANCK.match(x)]

class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)

setup(name='datamaestro',
    version=VERSION,
    description='Dataset management',
    author='Benjamin Piwowarski',
    author_email='benjamin@piwowarski.fr',
    url='https://github.com/bpiwowar/datamaestro',
    packages=find_namespace_packages(include="datamaestro.*"),
    install_requires = requirements,
    package_data={'datamaestro': ['LICENSE', 'datamaestro/repositories.yaml']},
    cmdclass={
        'verify': VerifyVersionCommand,
    },
    python_requires='>=3',
    data_files = [
        
    ],
    entry_points = {
        'console_scripts': [
            'datamaestro = datamaestro.__main__:main',                  
        ],         
        'mkdocs.plugins': [
                'datamaestro = datamaestro.commands.site:DatasetGenerator',
        ]
    },
)
