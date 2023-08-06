import datetime
import sys
import time
import urllib

import pytest
from mock import MagicMock

from jasmine.ci import CIRunner
from test.helpers.fake_config import FakeConfig


@pytest.fixture
def sysexit(monkeypatch):
    mock_exit = MagicMock()
    monkeypatch.setattr(sys, 'exit', mock_exit)
    return mock_exit


@pytest.fixture
def test_server(monkeypatch):
    import jasmine.ci
    instance = [None]

    class FakeTestServerThread(object):
        def __init__(self, port, app=None, *args, **kwargs):
            self.port = port
            instance[0] = self
        def start(arg):
            pass
        def join(self):
            pass

    monkeypatch.setattr(jasmine.ci, 'TestServerThread', FakeTestServerThread)
    return lambda: instance[0]


@pytest.fixture
def firefox_driver(monkeypatch):
    import selenium.webdriver.firefox.webdriver

    driver = MagicMock()
    driver_class = lambda: driver
    monkeypatch.setattr(selenium.webdriver.firefox.webdriver, 'WebDriver', driver_class)
    return driver


@pytest.fixture
def suites():
    return [
        {
            "id": 0,
            "name": "datepicker",
            "type": "suite",
            "children": [
                {
                    "id": 0,
                    "name": "calls the datepicker constructor",
                    "type": "spec",
                    "children": []
                },
                {
                    "id": 1,
                    "name": "icon triggers the datepicker",
                    "type": "spec",
                    "children": []
                }
            ]
        }
    ]


@pytest.fixture
def results():
    return [
        {
            "id": "spec0",
            "description": "",
            "fullName": "",
            "status": "failed",
            'failedExpectations': [
                {
                    "matcherName": "toHaveBeenCalledWith",
                    "expected": {
                        "format": "yyy-mm-dd"
                    },
                    "actual": {},
                    "message": "Expected spy datepicker to have been called with [ { format : 'yyy-mm-dd' } ] but actual calls were [ { format : 'yyyy-mm-dd' } ]",
                    "stack": "Totally the one you want",
                    "passed": False
                }

            ]
        },
        {
            "id": "spec1",
            "description": "",
            "fullName": "",
            "status": "passed",
            "failedExpectations": []
        }
    ]


@pytest.fixture
def suite_results():
    return [
        {
            "id": "suite0",
            "status": "failed",
            "failedExpectations": [
                {
                    "message": "something went wrong",
                    "stack": "stack"
                }
            ]
        },
        {
            "id": "suite1",
            "status": "finished"
        }
    ]


@pytest.fixture
def run_details():
    return {
        "overallStatus": "passed",
        "failedExpectations": [],
        "order": {
            "random": False,
            "seed": 54321
        }
    }


@pytest.fixture
def run_details_with_failures():
    return {
        "overallResult": "failed",
        "failedExpectations": [
            {
                "matcherName": "toEqual",
                "message": "Expected 'foo' to equal 'bar'.",
                "stack": "stack trace",
                "passed": False,
                "expected": "foo",
                "actual": "bar"
            },
            {
                "matcherName": "toEqual",
                "message": "Expected 'baz' to equal 'quux'.",
                "stack": "stack trace 2",
                "passed": False,
                "expected": "baz",
                "actual": "quux"
            }
        ],
        "order": {
            "random": False,
            "seed": 54321
        }
    }

@pytest.fixture
def run_details_random():
    return {
        "failedExpectations": [],
        "order": {
            "random": True,
            "seed": 12345
        }
    }


@pytest.fixture
def jasmine_config():
    return FakeConfig(
        src_dir='src',
        spec_dir='spec',
    )

def test_run_builds_url(suites, results, run_details, capsys, sysexit, firefox_driver, test_server, jasmine_config):
    CIRunner(jasmine_config=jasmine_config).run()
    firefox_driver.get.assert_called_with('http://localhost:%s?random=true' % test_server().port)


def test_run_with_random_seed(suites, results, run_details, capsys, sysexit, firefox_driver, test_server, jasmine_config):
    CIRunner(jasmine_config=jasmine_config).run(seed="1234")
    firefox_driver.get.assert_called()
    url = firefox_driver.get.call_args[0][0]
    uri_tuple = urllib.parse.urlparse(str(url))
    params = urllib.parse.parse_qs(uri_tuple[4])
    assert params['seed'] == ['1234']
    assert params['random'] == ['true']


def test_run_exits_with_zero_on_success(suites, run_details, capsys, sysexit, firefox_driver, test_server, jasmine_config):
    def execute_script(js):
        if 'jsApiReporter.finished' in js:
            return True
        if 'jsApiReporter.specResults' in js:
            return []
        if 'jsApiReporter.suiteResults' in js:
            return []
        if 'jsApiReporter.runDetails' in js:
            return run_details
        return None

    def get_log(type):
        return [dict(timestamp=0, level='INFO', message='hello')]

    firefox_driver.execute_script = execute_script
    firefox_driver.get_log = get_log

    CIRunner(jasmine_config=jasmine_config).run(show_logs=True)
    capsys.readouterr()

    assert not sysexit.called
    stdout, _ = capsys.readouterr()

    dt = datetime.datetime.fromtimestamp(0)
    assert '[{0} - INFO] hello\n'.format(dt) not in stdout


def test_run_exits_with_nonzero_on_failure(suites, run_details, capsys, sysexit, firefox_driver, test_server, jasmine_config):
    run_details['overallStatus'] = 'something other than passed'
    def execute_script(js):
        if 'jsApiReporter.finished' in js:
            return True
        if 'jsApiReporter.specResults' in js:
            return []
        if 'jsApiReporter.suiteResults' in js:
            return []
        if 'jsApiReporter.runDetails' in js:
            return run_details
        return None

    timestamp = time.time() * 1000

    def get_log(type):
        assert type == 'browser'
        return [
            dict(timestamp=timestamp, level='INFO', message='hello'),
            dict(timestamp=timestamp + 1, level='WARNING', message='world'),
        ]

    firefox_driver.execute_script = execute_script
    firefox_driver.get_log = get_log

    CIRunner(jasmine_config=jasmine_config).run()

    sysexit.assert_called_with(1)
    stdout, _ = capsys.readouterr()

    assert "Browser Session Logs" not in stdout
    assert "hello" not in stdout
    assert "world" not in stdout


def test_run_with_browser_logs(suites, results, run_details, capsys, sysexit, firefox_driver, test_server, jasmine_config):
    def execute_script(js):
        if 'jsApiReporter.finished' in js:
            return True
        if 'jsApiReporter.specResults' in js:
            return results
        if 'jsApiReporter.suiteResults' in js:
            return []
        if 'jsApiReporter.runDetails' in js:
            return run_details
        return None

    timestamp = time.time() * 1000

    def get_log(type):
        assert type == 'browser'
        return [
            dict(timestamp=timestamp, level='INFO', message='hello'),
            dict(timestamp=timestamp + 1, level='WARNING', message='world'),
        ]

    firefox_driver.execute_script = execute_script
    firefox_driver.get_log = get_log

    CIRunner(jasmine_config=jasmine_config).run(show_logs=True)

    stdout, _ = capsys.readouterr()

    dt = datetime.datetime.fromtimestamp(timestamp / 1000.0)
    assert '[{0} - INFO] hello\n'.format(dt) in stdout

    dt = datetime.datetime.fromtimestamp((timestamp + 1) / 1000.0)
    assert '[{0} - WARNING] world\n'.format(dt) in stdout


def test_displays_afterall_errors(suite_results, suites, results, run_details, capsys, sysexit, firefox_driver, test_server, jasmine_config):
    results[0] = results[1]
    del results[1]

    def execute_script(js):
        if 'jsApiReporter.finished' in js:
            return True
        if 'jsApiReporter.specResults' in js:
            return results
        if 'jsApiReporter.suiteResults' in js:
            return suite_results
        if 'jsApiReporter.runDetails' in js:
            return run_details
        return None

    firefox_driver.execute_script = execute_script

    CIRunner(jasmine_config=jasmine_config).run()
    stdout, _ = capsys.readouterr()

    assert 'something went wrong' in stdout


def test_displays_incomplete_reason(suite_results, suites, run_details, capsys, sysexit, firefox_driver, test_server, jasmine_config):
    run_details['overallStatus'] = 'incomplete'
    run_details['incompleteReason'] = 'out of cheese'

    def execute_script(js):
        if 'jsApiReporter.finished' in js:
            return True
        if 'jsApiReporter.specResults' in js:
            return []
        if 'jsApiReporter.suiteResults' in js:
            return suite_results
        if 'jsApiReporter.runDetails' in js:
            return run_details
        return None

    firefox_driver.execute_script = execute_script

    CIRunner(jasmine_config=jasmine_config).run()
    stdout, _ = capsys.readouterr()

    assert 'Incomplete: out of cheese' in stdout


def test_displays_top_suite_errors(suite_results, suites, results, run_details_with_failures, capsys, sysexit, firefox_driver, test_server, jasmine_config):
    results[0] = results[1]
    del results[1]

    def execute_script(js):
        if 'jsApiReporter.finished' in js:
            return True
        if 'jsApiReporter.specResults' in js:
            return results
        if 'jsApiReporter.suiteResults' in js:
            return suite_results
        if 'jsApiReporter.runDetails' in js:
            return run_details_with_failures
        return None

    firefox_driver.execute_script = execute_script

    CIRunner(jasmine_config=jasmine_config).run()
    stdout, _ = capsys.readouterr()

    assert "Expected 'foo' to equal 'bar'." in stdout
    assert "stack trace" in stdout
    assert "Expected 'baz' to equal 'quux'." in stdout
    assert "stack trace 2" in stdout

    sysexit.assert_called_with(1)


def test_displays_random_seed(results, suite_results, run_details_random, firefox_driver, capsys, test_server, jasmine_config, sysexit):
    def execute_script(js):
        if 'jsApiReporter.finished' in js:
            return True
        if 'jsApiReporter.specResults' in js:
            return results
        if 'jsApiReporter.suiteResults' in js:
            return suite_results
        if 'jsApiReporter.runDetails' in js:
            return run_details_random
        return None

    firefox_driver.execute_script = execute_script

    CIRunner(jasmine_config=jasmine_config).run()
    stdout, _ = capsys.readouterr()
    assert 'Randomized with seed 12345 (jasmine-ci --seed 12345)' in stdout


def test_doesnt_displays_random_seed_if_not_random(results, suite_results, run_details, firefox_driver, capsys, test_server, jasmine_config, sysexit):
    def execute_script(js):
        if 'jsApiReporter.finished' in js:
            return True
        if 'jsApiReporter.specResults' in js:
            return results
        if 'jsApiReporter.suiteResults' in js:
            return suite_results
        if 'jsApiReporter.runDetails' in js:
            return run_details
        return None

    firefox_driver.execute_script = execute_script

    CIRunner(jasmine_config=jasmine_config).run()
    stdout, _ = capsys.readouterr()
    assert 'Randomized with seed' not in stdout

