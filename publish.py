"""
Build script for psg_reskinner.

Usage:

To build and upload to legacy PyPi
> python -m publish.py legacy
"""
from psg_reskinner import __version__ as VERSION
from os import system
from datetime import datetime
from bumpver.version import parse_version
from argparse import ArgumentParser as p


DEFAULT_UPLOAD_DESTINATION = 'legacy'

with open('./.env', 'r') as env:
    TOKEN = env.readline()


def build():
    """
    Builds the project.
    """
    print('Building wheels...')
    system(f'python -m build -n --outdir=./dist/v{parse_version(VERSION).major}/{VERSION}/')


def commit(message: str = f'New Commit at {datetime.now()}'):
    """
    Commits files to local repository.
    """
    print('Staging commit...')
    system(f'git commit -m "{message}" -a')


def upload_testpypi(version: str = VERSION):
    """
    Uploads the project to PyPi's test server.
    :param version: The specific version to upload.
    """
    print('Uploading to TestPyPi...')
    system(f'twine upload --username __token__ --password {TOKEN} --repository testpypi dist/psg_reskinner-{version}*')


def upload_legacy(version: str = VERSION):
    """
    Uploads the project to PyPi's legacy servers.
    :param version: The specific version to upload.
    """
    print('Uploading to PyPi...')
    system(f'twine upload --username __token__ --password {TOKEN} --repository-url https://upload.pypi.org/legacy/ dist/psg_reskinner-{version}*')


def bumpver(major: bool = False, minor: bool = False, patch: bool = True):
    """
    Internal use only.

    Bumps the version a notch using the BumpVer tool.
    """
    print('Updating version...')
    if sum([major, minor, patch]) != 1:
        raise Exception('One (and only one) of major, minor or patch must be set!')
    target = 'major' if major else 'minor' if minor else 'patch'
    system(f'bumpver update --{target}')


def update_demo():
    """
    Internal use only.

    Updates the README with the demo code.
    """
    system('python demo_updater.py')


# update_demo()
commit()
# bumpver()
# build()