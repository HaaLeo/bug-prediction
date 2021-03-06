# ------------------------------------------------------------------------------------------------------
#  Copyright (c) Leo Hanisch. All rights reserved.
#  Licensed under the BSD 3-Clause License. See LICENSE.txt in the project root for license information.
# ------------------------------------------------------------------------------------------------------

from unittest.mock import Mock, patch
from os import path
import pytest

SCM_MOCK = Mock()
TIME_MOCK = Mock()
GLOB_MOCK = Mock()


def setup_module(module):
    module.patcher = patch.dict('sys.modules', {
        'bugprediction.scm': SCM_MOCK,
        'time': TIME_MOCK,
        'glob': GLOB_MOCK
    })
    module.patcher.start()


def teardown_module(module):
    module.patcher.stop()


@pytest.fixture
def scm():
    SCM_MOCK.reset_mock()
    SCM_MOCK.SourceControllManager().iter_change_periods.return_value = [
        {
            'changes': {
                'foo/bar.txt': 4,
                'hello/world.txt': 5
            },
            'end_time': {
                'epoch': 800
            }
        },
        {
            'changes': {
                'foo/bar.txt': 6,
                'hello/world.txt': 7
            },
            'end_time': {
                'epoch': 900
            }
        }
    ]
    return SCM_MOCK


@pytest.fixture(autouse=True)
def time():
    TIME_MOCK.reset_mock()
    TIME_MOCK.time.return_value = 1000
    return TIME_MOCK


def glob():
    GLOB_MOCK.reset_mock()
    GLOB_MOCK.iglob.return_value = ['../test-dir/foo/bar.txt', '../test-dir/hello/world.txt']
    return GLOB_MOCK

@pytest.fixture
def kwargs():
    return {
        'directory': '../test-dir',
        'file_glob': 'test-pattern',
        'contribution': 'full'
    }


def test_predict_full_contribution(kwargs, scm):
    from bugprediction.history_complexity_metric import calculate_hcm

    result, _ = calculate_hcm(**kwargs)
    assert result['foo/bar.txt'] == 1.986803511923148
    assert result['hello/world.txt'] == 1.986803511923148
    scm.SourceControllManager().iter_change_periods.assert_called_once_with(path.normpath('../test-dir/test-pattern'))


def test_predict_percentage_contribution(kwargs, scm):
    kwargs['contribution'] = 'percentage'
    from bugprediction.history_complexity_metric import calculate_hcm

    result, _ = calculate_hcm(**kwargs)
    assert result['foo/bar.txt'] == 0.9000447651638763
    assert result['hello/world.txt'] == 1.0867587467592714
    scm.SourceControllManager().iter_change_periods.assert_called_once_with(path.normpath('../test-dir/test-pattern'))


def test_predict_uniform_contribution(kwargs, scm):
    kwargs['contribution'] = 'uniform'
    from bugprediction.history_complexity_metric import calculate_hcm

    result, _ = calculate_hcm(**kwargs)
    assert result['foo/bar.txt'] == 0.993401755961574
    assert result['hello/world.txt'] == 0.993401755961574
    scm.SourceControllManager().iter_change_periods.assert_called_once_with(path.normpath('../test-dir/test-pattern'))


def test_predict_decay(kwargs, scm):
    kwargs['decay'] = .4
    from bugprediction.history_complexity_metric import calculate_hcm

    result, _ = calculate_hcm(**kwargs)
    assert result['foo/bar.txt'] == 4.230202958175646e-18
    assert result['hello/world.txt'] == 4.230202958175646e-18
    scm.SourceControllManager().iter_change_periods.assert_called_once_with(path.normpath('../test-dir/test-pattern'))


def test_predict_subsystems(kwargs, scm):
    kwargs['subsystems'] = ['foo']
    from bugprediction.history_complexity_metric import calculate_hcm

    result, _ = calculate_hcm(**kwargs)
    assert result['foo'] == 1.986803511923148
    scm.SourceControllManager().iter_change_periods.assert_called_once_with(path.normpath('../test-dir/test-pattern'))
