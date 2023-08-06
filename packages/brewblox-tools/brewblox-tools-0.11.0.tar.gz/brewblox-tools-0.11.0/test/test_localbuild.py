"""
Tests localbuild.py
"""

from subprocess import STDOUT
from unittest.mock import call

import pytest

from brewblox_tools import localbuild

TESTED = localbuild.__name__


@pytest.fixture
def mocked_utils(mocker):
    mocked = [
        'glob',
        'getenv',
        'remove',
        'check_call',
        'check_output',
        'find_dotenv',
        'load_dotenv',
    ]
    return {k: mocker.patch(TESTED + '.' + k) for k in mocked}


@pytest.fixture
def distcopy_mock(mocker):
    return mocker.patch(TESTED + '.distcopy.main')


@pytest.fixture
def run_mock(mocker):
    return mocker.patch(TESTED + '.run')


def localbuild_sh(context):
    return f'cd {context} && if [ -f ./localbuild.sh ]; then bash ./localbuild.sh; fi'


def test_run(mocked_utils):
    localbuild.run('test test one two')
    mocked_utils['check_call'].assert_called_once_with(
        'test test one two', shell=True, stderr=STDOUT
    )


def test_localbuild_simple(mocked_utils, distcopy_mock, run_mock):
    mocked_utils['glob'].return_value = ['f1', 'f2']
    mocked_utils['getenv'].side_effect = [
        'bb-repo',
    ]

    localbuild.main([])

    assert distcopy_mock.call_args_list == [
        call('dist/ docker/dist/'.split()),
    ]
    assert mocked_utils['remove'].call_args_list == [
        call('f1'),
        call('f2'),
    ]
    assert run_mock.call_args_list == [
        call('python setup.py sdist'),
        call('pipenv lock --requirements > docker/requirements.txt'),
        call(localbuild_sh('docker')),
        call('docker build ' +
             '--build-arg service_info="$(git describe) @ $(date)" ' +
             '--no-cache --tag bb-repo:local --file docker/amd/Dockerfile docker')
    ]


def test_localbuild_all(mocked_utils, distcopy_mock, run_mock):
    mocked_utils['glob'].return_value = ['f1', 'f2']
    mocked_utils['getenv'].side_effect = [
        'bb-repo',
        'feature/funky_branch',
    ]

    localbuild.main(['--arch', 'amd', 'arm',
                     '--tags', 'test:tag',
                     '--push',
                     '--branch-tag',
                     '--pull',
                     '--context', 'dk',
                     '--file', 'df',
                     '--distcopy', 'config',
                     ])

    assert distcopy_mock.call_args_list == [
        call('dist/ dk/dist/'.split()),
        call('config/ dk/config/'.split()),
    ]
    assert run_mock.call_args_list == [
        call('python setup.py sdist'),
        call('pipenv lock --requirements > dk/requirements.txt'),
        call(localbuild_sh('dk')),
        call('docker build --pull ' +
             '--build-arg service_info="$(git describe) @ $(date)" --no-cache ' +
             '--tag bb-repo:local ' +
             '--tag bb-repo:test-tag ' +
             '--tag bb-repo:feature-funky-branch ' +
             '--file dk/amd/df ' +
             'dk'),
        call('docker push bb-repo:test-tag'),
        call('docker push bb-repo:feature-funky-branch'),
        call('docker run --rm --privileged multiarch/qemu-user-static:register --reset ' +
             '&& ' +
             'docker build --pull ' +
             '--build-arg service_info="$(git describe) @ $(date)" --no-cache ' +
             '--tag bb-repo:rpi-local ' +
             '--tag bb-repo:rpi-test-tag ' +
             '--tag bb-repo:rpi-feature-funky-branch ' +
             '--file dk/arm/df ' +
             'dk'),
        call('docker push bb-repo:rpi-test-tag'),
        call('docker push bb-repo:rpi-feature-funky-branch'),
    ]


def test_localbuild_no_setup(mocked_utils, distcopy_mock, run_mock):
    mocked_utils['glob'].return_value = ['f1', 'f2']
    mocked_utils['getenv'].side_effect = [
        'bb-repo',
    ]

    localbuild.main(['--no-setup'])

    assert distcopy_mock.call_count == 0
    assert mocked_utils['remove'].call_count == 0
    assert run_mock.call_args_list == [
        call(localbuild_sh('docker')),
        call('docker build ' +
             '--build-arg service_info="$(git describe) @ $(date)" ' +
             '--no-cache --tag bb-repo:local --file docker/amd/Dockerfile docker')
    ]
