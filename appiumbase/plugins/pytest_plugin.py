import colorama
import os
import pytest
import sys
import time
from appiumbase import config as ab_config
from appiumbase.config import settings
from appiumbase.fixtures import constants


pytest_plugins = ["pytester"]  # Adds the "testdir" fixture

def pytest_addoption(parser):
    """
       This plugin adds the following command-line options to pytest:
    """

    parser.addoption(
        "--device",
        action="store",
        dest="device",
        type=str.lower,
        choices=constants.ValidDevices.valid_devices,
        default=constants.Devices.ANDROID,
        help="""Specifies the device to use. Default: ANDROID.
                    If you want to use iphone, explicitly indicate that.
                    Example: (--device=iphone)""",
    )

    parser.addoption(
        "--android",
        action="store_true",
        dest="use_android",
        default=False,
        help="""Shortcut for --device=android. On by default.)""",
    )

    parser.addoption(
        "--iphone",
        action="store_true",
        dest="use_iphone",
        default=False,
        help="""Shortcut for --device=iphone.)""",
    )

    parser.addoption(
        "--env",
        action="store",
        dest="environment",
        type=str.lower,
        choices=(
            constants.Environment.QA,
            constants.Environment.STAGING,
            constants.Environment.DEVELOP,
            constants.Environment.PRODUCTION,
            constants.Environment.MASTER,
            constants.Environment.LOCAL,
            constants.Environment.TEST,
        ),
        default=constants.Environment.TEST,
        help="""This option is used for setting the test env.
                   In tests, use "self.environment" to get the env.""",
    )

    parser.addoption(
        "--data",
        dest="data",
        default=None,
        help="Extra data to pass to tests from the command line.",
    )
    parser.addoption(
        "--var1",
        dest="var1",
        default=None,
        help="Extra data to pass to tests from the command line.",
    )
    parser.addoption(
        "--var2",
        dest="var2",
        default=None,
        help="Extra data to pass to tests from the command line.",
    )
    parser.addoption(
        "--var3",
        dest="var3",
        default=None,
        help="Extra data to pass to tests from the command line.",
    )
    parser.addoption(
        "--cap_file",
        "--cap-file",
        dest="cap_file",
        default=None,
        help="""The file that stores device desired capabilities
                    for device , BrowserStack, Sauce Labs, and other
                    remote web drivers to use.""",
    )

    parser.addoption(
        "--settings_file",
        "--settings-file",
        "--settings",
        action="store",
        dest="settings_file",
        default=None,
        help="""The file that stores key/value pairs for
                    overriding values in the
                    appiumbase/config/settings.py file.""",
    )

    parser.addoption(
        "--emulator",
        "--mobile_emulator",
        action="store_true",
        dest="mobile_emulator",
        default=False,
        help="""If this option is enabled, the mobile emulator
                    will be used while running tests.""",
    )

    parser.addoption(
        "--is_pytest",
        "--is-pytest",
        action="store_true",
        dest="is_pytest",
        default=True,
        help="""This is used by the BaseCase class to tell apart
                   pytest runs from nosetest runs. (Automatic)""",
    )

    parser.addoption(
        "--time_limit",
        "--time-limit",
        "--timelimit",
        action="store",
        dest="time_limit",
        default=None,
        help="""Use this to set a time limit per test, in seconds.
                    If a test runs beyond the limit, it fails.""",
    )

    parser.addoption(
        "--slow_mode",
        "--slow-mode",
        "--slowmo",
        "--slow",
        action="store_true",
        dest="slow_mode",
        default=False,
        help="""Using this slows down the automation.""",
    )

    parser.addoption(
        "--rs",
        "--reuse_session",
        "--reuse-session",
        action="store_true",
        dest="reuse_session",
        default=False,
        help="""The option to reuse the selenium browser window
                    session between tests.""",
    )

    parser.addoption(
        "--bs",
        "--browserstack",
        action="store_true",
        dest="browser_stack",
        default=False,
        help="""The option to use Browser Stack as a remote server
                for webdriver.""",
    )

    sys_argv = sys.argv
    ab_config._device_shortcut = None

    device_changes = 0
    device_set = None
    device_list = []
    if "--device=android" in sys_argv or "--device chrome" in sys_argv:
        device_changes += 1
        device_set = "android"
        device_list.append("--device=android")
    if "--device=iphone" in sys_argv or "--device iphone" in sys_argv:
        device_changes += 1
        device_set = "iphone"
        device_list.append("--device=iphone")
    if "--device=ipad" in sys_argv or "--device ipad" in sys_argv:
        device_changes += 1
        device_set = "ipad"
        device_list.append("--device=ipad")
    if "--android" in sys_argv and not device_set == "android":
        device_changes += 1
        ab_config._device_shortcut = "android"
        device_list.append("--android")
    if "--iphone" in sys_argv and not device_set == "iphone":
        device_changes += 1
        ab_config._device_shortcut = "iphone"
        device_list.append("--iphone")
    if "--ipad" in sys_argv and not device_set == "ipad":
        device_changes += 1
        ab_config._device_shortcut = "ipad"
        device_list.append("--ipad")
    if device_changes > 1:
        message = "\n\n  TOO MANY device types were entered!"
        message += "\n  There were %s found:\n  >  %s" % (
            device_changes,
            ", ".join(device_list),
        )
        message += "\n  ONLY ONE default device is allowed!"
        message += "\n  Select a single device & try again!\n"
        raise Exception(message)

def pytest_configure(config):
    ab_config.item_count = 0
    ab_config.item_count_passed = 0
    ab_config.item_count_failed = 0
    ab_config.item_count_skipped = 0
    ab_config.item_count_untested = 0
    ab_config.is_pytest = True
    ab_config.pytest_config = config
    ab_config.device = config.getoption("device")
    if ab_config._device_shortcut:
        ab_config.device = ab_config._device_shortcut
    ab_config.data = config.getoption("data")
    ab_config.var1 = config.getoption("var1")
    ab_config.var2 = config.getoption("var2")
    ab_config.var3 = config.getoption("var3")
    ab_config.environment = config.getoption("environment")
    ab_config.mobile_emulator = config.getoption("mobile_emulator")
    ab_config.cap_file = config.getoption("cap_file")
    ab_config.settings_file = config.getoption("settings_file")
    ab_config.log_path = "latest_logs/"  # (No longer editable!)
    ab_config._time_limit = config.getoption("time_limit")
    ab_config.time_limit = config.getoption("time_limit")
    ab_config.slow_mode = config.getoption("slow_mode")
    ab_config.reuse_session = config.getoption("reuse_session")
    ab_config.browser_stack = config.getoption("browser_stack")
    ab_config._is_timeout_changed = False
    ab_config._SMALL_TIMEOUT = settings.SMALL_TIMEOUT
    ab_config._LARGE_TIMEOUT = settings.LARGE_TIMEOUT
    ab_config.pytest_html_report = config.getoption("htmlpath")  # --html=FILE
    ab_config._sb_node = {}  # sb node dictionary (Used with the sb fixture)
    # Dashboard-specific variables
    ab_config._results = {}  # SBase Dashboard test results
    ab_config._duration = {}  # SBase Dashboard test duration
    ab_config._display_id = {}  # SBase Dashboard display ID
    ab_config._d_t_log_path = {}  # SBase Dashboard test log path
    ab_config._test_id = None  # The SBase Dashboard test id
    ab_config._latest_display_id = None  # The latest SBase display id
    ab_config._dashboard_initialized = False  # Becomes True after init
    ab_config._has_exception = False  # This becomes True if any test fails
    ab_config._multithreaded = False  # This becomes True if multithreading
    ab_config._only_unittest = True  # If any test uses BaseCase, becomes False
    ab_config._abase_detected = False  # Becomes True during AppiumBase tests
    ab_config._extra_dash_entries = []  # Dashboard entries for non-ABase tests
    ab_config._using_html_report = False  # Becomes True when using html report
    ab_config._dash_is_html_report = False  # Dashboard becomes the html report
    ab_config._saved_dashboard_pie = None  # Copy of pie chart for html report
    ab_config._dash_final_summary = None  # Dash status to add to html report
    ab_config._html_report_name = None  # The name of the pytest html report

    arg_join = " ".join(sys.argv)
    if ("-n" in sys.argv) or (" -n=" in arg_join) or ("-c" in sys.argv):
        ab_config._multithreaded = True
    if "--html" in sys.argv or " --html=" in arg_join:
        ab_config._using_html_report = True
        ab_config._html_report_name = config.getoption("htmlpath")
        if ab_config.dashboard:
            if ab_config._html_report_name == "dashboard.html":
                ab_config._dash_is_html_report = True

def pytest_sessionstart(session):
    pass

def _get_test_ids_(the_item):
    test_id = the_item.nodeid
    if not test_id:
        test_id = "unidentified_TestCase"
    display_id = test_id
    r"""
    # Due to changes in SeleniumBase 1.66.0, we're now using the
    # item's original nodeid for both the test_id and display_id.
    # (This only impacts tests using The Dashboard.)
    # If there are any issues, we'll revert back to the old code.
    test_id = the_item.nodeid.split("/")[-1].replace(" ", "_")
    if "[" in test_id:
        test_id_intro = test_id.split("[")[0]
        parameter = test_id.split("[")[1]
        parameter = re.sub(re.compile(r"\W"), "", parameter)
        test_id = test_id_intro + "__" + parameter
    display_id = test_id
    test_id = test_id.replace("/", ".").replace("\\", ".")
    test_id = test_id.replace("::", ".").replace(".py", "")
    """
    return test_id, display_id

def pytest_runtest_setup(item):
    """ This runs before every test with pytest. """
    test_id, display_id = _get_test_ids_(item)
    ab_config._test_id = test_id
    ab_config._latest_display_id = display_id

def pytest_runtest_teardown(item):
    """This runs after every test with pytest.
    Make sure that webdriver and headless displays have exited.
    (Has zero effect on tests using --reuse-session / --rs)"""
    try:
        self = item._testcase
        try:
            if (
                hasattr(self, "driver")
                and self.driver
                and "--pdb" not in sys.argv
            ):
                self.driver.quit()
        except Exception:
            pass
    except Exception:
        pass

def pytest_sessionfinish(session):
    pass

@pytest.fixture()
def ab(request):
    """AppiumBase as a pytest fixture.
    Usage example: "def test_one(sb):"
    You may need to use this for tests that use other pytest fixtures."""
    from appiumbase import BaseCase

    class BaseClass(BaseCase):
        def setUp(self):
            super(BaseClass, self).setUp()

        def tearDown(self):
            self.save_teardown_screenshot()
            super(BaseClass, self).tearDown()

        def base_method(self):
            pass

    if request.cls:
        request.cls.ab = BaseClass("base_method")
        request.cls.ab.setUp()
        request.cls.ab._needs_tearDown = True
        request.cls.ab._using_ab_fixture = True
        request.cls.ab._using_ab_fixture_class = True
        ab_config._ab_node[request.node.nodeid] = request.cls.ab
        yield request.cls.ab
        if request.cls.ab._needs_tearDown:
            request.cls.ab.tearDown()
            request.cls.ab._needs_tearDown = False
    else:
        ab = BaseClass("base_method")
        ab.setUp()
        ab._needs_tearDown = True
        ab._using_ab_fixture = True
        ab._using_ab_fixture_no_class = True
        ab_config._ab_node[request.node.nodeid] = ab
        yield ab
        if ab._needs_tearDown:
            ab.tearDown()
            ab._needs_tearDown = False


def _perform_pytest_unconfigure_():
    if hasattr(ab_config, "reuse_session") and ab_config.reuse_session:
        # Close the shared browser session
        if ab_config.shared_driver:
            try:
                ab_config.shared_driver.quit()
            except AttributeError:
                pass
            except Exception:
                pass
        ab_config.shared_driver = None
    # Dashboard post-processing: Disable time-based refresh and stamp complete
    if not hasattr(ab_config, "dashboard") or not ab_config.dashboard:
        # Done with "pytest_unconfigure" unless using the Dashboard
        return
    stamp = ""
    if ab_config._dash_is_html_report:
        # (If the Dashboard URL is the same as the HTML Report URL:)
        # Have the html report refresh back to a dashboard on update
        stamp += (
            '\n<script type="text/javascript" src="%s">'
            "</script>" % constants.Dashboard.LIVE_JS
        )
    stamp += "\n<!--Test Run Complete-->"
    find_it = constants.Dashboard.META_REFRESH_HTML
    swap_with = ""  # Stop refreshing the page after the run is done
    find_it_2 = "Awaiting results... (Refresh the page for updates)"
    swap_with_2 = (
        "Test Run ENDED: Some results UNREPORTED due to skipped tearDown()"
    )
    find_it_3 = '<td class="col-result">Untested</td>'
    swap_with_3 = '<td class="col-result">Unreported</td>'
    find_it_4 = 'href="%s"' % constants.Dashboard.DASH_PIE_PNG_1
    swap_with_4 = 'href="%s"' % constants.Dashboard.DASH_PIE_PNG_2
    try:
        abs_path = os.path.abspath(".")
        dashboard_path = os.path.join(abs_path, "dashboard.html")
        # Part 1: Finalizing the dashboard / integrating html report
        if os.path.exists(dashboard_path):
            the_html_d = None
            with open(dashboard_path, "r", encoding="utf-8") as f:
                the_html_d = f.read()
            if ab_config._multithreaded and "-c" in sys.argv:
                # Threads have "-c" in sys.argv, except for the last
                raise Exception('Break out of "try" block.')
            if ab_config._multithreaded:
                dash_pie_loc = constants.Dashboard.DASH_PIE
                pie_path = os.path.join(abs_path, dash_pie_loc)
                if os.path.exists(pie_path):
                    import json

                    with open(pie_path, "r") as f:
                        dash_pie = f.read().strip()
                    ab_config._saved_dashboard_pie = json.loads(dash_pie)
            # If the test run doesn't complete by itself, stop refresh
            the_html_d = the_html_d.replace(find_it, swap_with)
            the_html_d = the_html_d.replace(find_it_2, swap_with_2)
            the_html_d = the_html_d.replace(find_it_3, swap_with_3)
            the_html_d = the_html_d.replace(find_it_4, swap_with_4)
            the_html_d += stamp
            if ab_config._dash_is_html_report and (
                ab_config._saved_dashboard_pie
            ):
                the_html_d = the_html_d.replace(
                    "<h1>dashboard.html</h1>",
                    ab_config._saved_dashboard_pie,
                )
                the_html_d = the_html_d.replace(
                    "</head>",
                    '</head><link rel="shortcut icon" '
                    'href="%s">' % constants.Dashboard.DASH_PIE_PNG_3,
                )
                the_html_d = the_html_d.replace(
                    "<html>", '<html lang="en">'
                )
                the_html_d = the_html_d.replace(
                    "<head>",
                    '<head><meta http-equiv="Content-Type" '
                    'content="text/html, charset=utf-8;">'
                    '<meta name="viewport" content="shrink-to-fit=no">',
                )
                if ab_config._dash_final_summary:
                    the_html_d += ab_config._dash_final_summary
                time.sleep(0.1)  # Add time for "livejs" to detect changes
                with open(dashboard_path, "w", encoding="utf-8") as f:
                    f.write(the_html_d)  # Finalize the dashboard
                time.sleep(0.1)  # Add time for "livejs" to detect changes
                the_html_d = the_html_d.replace(
                    "</head>", "</head><!-- Dashboard Report Done -->"
                )
            with open(dashboard_path, "w", encoding="utf-8") as f:
                f.write(the_html_d)  # Finalize the dashboard
            # Part 2: Appending a pytest html report with dashboard data
            html_report_path = None
            if ab_config._html_report_name:
                html_report_path = os.path.join(
                    abs_path, ab_config._html_report_name
                )
            if (
                ab_config._using_html_report
                and html_report_path
                and os.path.exists(html_report_path)
                and not ab_config._dash_is_html_report
            ):
                # Add the dashboard pie to the pytest html report
                the_html_r = None
                with open(html_report_path, "r", encoding="utf-8") as f:
                    the_html_r = f.read()
                if ab_config._saved_dashboard_pie:
                    h_r_name = ab_config._html_report_name
                    if "/" in h_r_name and h_r_name.endswith(".html"):
                        h_r_name = h_r_name.split("/")[-1]
                    elif "\\" in h_r_name and h_r_name.endswith(".html"):
                        h_r_name = h_r_name.split("\\")[-1]
                    the_html_r = the_html_r.replace(
                        "<h1>%s</h1>" % h_r_name,
                        ab_config._saved_dashboard_pie,
                    )
                    the_html_r = the_html_r.replace(
                        "</head>",
                        '</head><link rel="shortcut icon" href='
                        '"%s">' % constants.Dashboard.DASH_PIE_PNG_3,
                    )
                    if ab_config._dash_final_summary:
                        the_html_r += ab_config._dash_final_summary
                with open(html_report_path, "w", encoding="utf-8") as f:
                    f.write(the_html_r)  # Finalize the HTML report
    except KeyboardInterrupt:
        pass
    except Exception:
        pass
