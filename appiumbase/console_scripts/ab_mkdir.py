"""
Creates a new folder for running SeleniumBase scripts.
Usage:
    appiumbase mkdir [DIRECTORY] [OPTIONS]
    OR     abase mkdir [DIRECTORY] [OPTIONS]
Example:
    abase mkdir ui_tests
Options:
    -b / --basic  (Only config files. No tests added.)
Output:
    Creates a new folder for running ABase scripts.
    The new folder contains default config files,
    sample tests for helping new users get started,
    and Python boilerplates for setting up customized
    test frameworks.
"""

import codecs
import colorama
import os
import sys


def invalid_run_command(msg=None):
    exp = "  ** mkdir **\n\n"
    exp += "  Usage:\n"
    exp += "          appiumbase mkdir [DIRECTORY] [OPTIONS]\n"
    exp += "          OR     abase mkdir [DIRECTORY] [OPTIONS]\n"
    exp += "  Example:\n"
    exp += "          abase mkdir ui_tests\n"
    exp += "  Options:\n"
    exp += "          -b / --basic  (Only config files. No tests added.)\n"
    exp += "  Output:\n"
    exp += "          Creates a new folder for running ABase scripts.\n"
    exp += "          The new folder contains default config files,\n"
    exp += "          sample tests for helping new users get started,\n"
    exp += "          and Python boilerplates for setting up customized\n"
    exp += "          test frameworks.\n"
    if not msg:
        raise Exception("INVALID RUN COMMAND!\n\n%s" % exp)
    elif msg == "help":
        print("\n%s" % exp)
        sys.exit()
    else:
        raise Exception("INVALID RUN COMMAND!\n\n%s\n%s\n" % (exp, msg))


def main():
    c1 = ""
    c5 = ""
    c7 = ""
    cr = ""
    if "linux" not in sys.platform:
        colorama.init(autoreset=True)
        c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
        c5 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
        c7 = colorama.Fore.BLACK + colorama.Back.MAGENTA
        cr = colorama.Style.RESET_ALL

    basic = False
    help_me = False
    error_msg = None
    invalid_cmd = None

    command_args = sys.argv[2:]
    dir_name = command_args[0]
    if dir_name == "-h" or dir_name == "--help":
        invalid_run_command("help")
    elif len(str(dir_name)) < 2:
        error_msg = "Directory name length must be at least 2 characters long!"
    elif "/" in str(dir_name) or "\\" in str(dir_name):
        error_msg = 'Directory name must not include slashes ("/", "\\")!'
    elif dir_name.startswith("-"):
        error_msg = 'Directory name cannot start with "-"!'
    elif os.path.exists(os.getcwd() + "/" + dir_name):
        error_msg = (
            'Directory "%s" already exists in this directory!' % dir_name
        )
    if error_msg:
        error_msg = c5 + "ERROR: " + error_msg + cr
        invalid_run_command(error_msg)

    if len(command_args) >= 2:
        options = command_args[1:]
        for option in options:
            option = option.lower()
            if option == "-h" or option == "--help":
                help_me = True
            elif option == "-b" or option == "--basic":
                basic = True
            else:
                invalid_cmd = "\n===> INVALID OPTION: >> %s <<\n" % option
                invalid_cmd = invalid_cmd.replace(">> ", ">>" + c5 + " ")
                invalid_cmd = invalid_cmd.replace(" <<", " " + cr + "<<")
                invalid_cmd = invalid_cmd.replace(">>", c7 + ">>" + cr)
                invalid_cmd = invalid_cmd.replace("<<", c7 + "<<" + cr)
                help_me = True
                break
    if help_me:
        invalid_run_command(invalid_cmd)

    os.mkdir(dir_name)

    data = []
    appiumbase_req = "appiumbase"
    try:
        from appiumbase import __version__

        seleniumbase_req = "seleniumbase>=%s" % str(__version__)
    except Exception:
        pass
    data.append(appiumbase_req)
    data.append("")
    file_path = "%s/%s" % (dir_name, "requirements.txt")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    data = []
    data.append("[pytest]")
    data.append(
        "addopts = --capture=no -p no:cacheprovider "
        "--pdbcls=IPython.terminal.debugger:TerminalPdb"
    )
    data.append("filterwarnings =")
    data.append("    ignore::pytest.PytestWarning")
    data.append("    ignore:.*U.*mode is deprecated:DeprecationWarning")
    data.append("junit_family = legacy")
    data.append("python_files = test_*.py *_test.py *_tests.py *_suite.py")
    data.append("python_classes = Test* *Test* *Test *Tests *Suite")
    data.append("python_functions = test_*")
    data.append("markers =")
    data.append("    marker1: custom marker")
    data.append("    marker2: custom marker")
    data.append("    marker3: custom marker")
    data.append("    marker_test_suite: custom marker")
    data.append("    expected_failure: custom marker")
    data.append("    local: custom marker")
    data.append("    remote: custom marker")
    data.append("    offline: custom marker")
    data.append("    develop: custom marker")
    data.append("    qa: custom marker")
    data.append("    ci: custom marker")
    data.append("    e2e: custom marker")
    data.append("    ready: custom marker")
    data.append("    smoke: custom marker")
    data.append("    deploy: custom marker")
    data.append("    active: custom marker")
    data.append("    master: custom marker")
    data.append("    release: custom marker")
    data.append("    staging: custom marker")
    data.append("    production: custom marker")
    data.append("")
    file_path = "%s/%s" % (dir_name, "pytest.ini")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    data = []
    data.append("[flake8]")
    data.append("exclude=recordings,temp")
    data.append("")
    data.append("[nosetests]")
    data.append("nocapture=1")
    data.append("logging-level=INFO")
    data.append("")
    data.append("[bdist_wheel]")
    data.append("universal=1")
    file_path = "%s/%s" % (dir_name, "setup.cfg")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    data = []
    data.append("")
    file_path = "%s/%s" % (dir_name, "__init__.py")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    data = []
    data.append("*.py[cod]")
    data.append("*.egg")
    data.append("*.egg-info")
    data.append("dist")
    data.append("build")
    data.append("ghostdriver.log")
    data.append("eggs")
    data.append("parts")
    data.append("bin")
    data.append("var")
    data.append("sdist")
    data.append("develop-eggs")
    data.append(".installed.cfg")
    data.append("lib")
    data.append("lib64")
    data.append("__pycache__")
    data.append(".env")
    data.append(".venv")
    data.append("env/")
    data.append("venv/")
    data.append("ENV/")
    data.append("VENV/")
    data.append("env.bak/")
    data.append("venv.bak/")
    data.append(".abase")
    data.append(".sbase*")
    data.append("appiumbase_env")
    data.append("appiumbase_venv")
    data.append("abase_env")
    data.append("abase_venv")
    data.append("pyvenv.cfg")
    data.append(".Python")
    data.append("include")
    data.append("pip-delete-this-directory.txt")
    data.append("pip-selfcheck.json")
    data.append("ipython.1.gz")
    data.append("nosetests.1")
    data.append("pip-log.txt")
    data.append(".swp")
    data.append(".coverage")
    data.append(".tox")
    data.append("coverage.xml")
    data.append("nosetests.xml")
    data.append(".cache/*")
    data.append(".pytest_cache/*")
    data.append(".pytest_config")
    data.append("junit")
    data.append("test-results.xml")
    data.append(".idea")
    data.append(".project")
    data.append(".pydevproject")
    data.append(".vscode")
    data.append("logs")
    data.append("latest_logs")
    data.append("log_archives")
    data.append("archived_logs")
    data.append("pytestdebug.log")
    data.append("latest_report")
    data.append("report_archives")
    data.append("archived_reports")
    data.append("html_report.html")
    data.append("report.html")
    data.append("report.xml")
    data.append("dashboard.html")
    data.append("dashboard.json")
    data.append("dash_pie.json")
    data.append("dashboard.lock")
    data.append("allure_report")
    data.append("allure-report")
    data.append("allure_results")
    data.append("allure-results")
    data.append("tours_exported")
    data.append("images_exported")
    data.append("saved_cookies")
    data.append("recordings")
    data.append("visual_baseline")
    data.append("proxy.zip")
    data.append("proxy.lock")
    data.append("verbose_hub_server.dat")
    data.append("verbose_node_server.dat")
    data.append("ip_of_grid_hub.dat")
    data.append("downloaded_files")
    data.append("archived_files")
    data.append("assets")
    data.append("temp")
    data.append("temp_*/")
    data.append("node_modules")
    file_path = "%s/%s" % (dir_name, ".gitignore")
    file = codecs.open(file_path, "w+", "utf-8")
    file.writelines("\r\n".join(data))
    file.close()

    if basic:
        success = (
            "\n" + c1 + '* Directory "' + dir_name + '" was created '
            "with config files! *" + cr + "\n"
        )
        print(success)
        return

if __name__ == "__main__":
    invalid_run_command()