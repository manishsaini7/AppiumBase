"""
AppiumBase console scripts runner
Usage:
appiumbase [COMMAND] [PARAMETERS]
  OR   abase [COMMAND] [PARAMETERS]
Examples:
abase methods
abase options
abaseir ui_tests
"""

import colorama
import sys

colorama.init(autoreset=True)


def show_usage():
    show_basic_usage()
    sc = ""
    sc += '    Type "abase help [COMMAND]" for specific command info.\n'
    sc += '    For info on all commands, type: "appiumbase --help".\n'
    sc += ' * (Use "pytest" for running tests) *\n'
    if "linux" not in sys.platform:
        c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
        c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
        c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
        c4 = colorama.Fore.MAGENTA + colorama.Back.LIGHTYELLOW_EX
        cr = colorama.Style.RESET_ALL
        sc = sc.replace("appiumbase", c1 + "appium" + c2 + "base" + cr)
        sc = sc.replace("abase", c1 + "a" + c2 + "base" + cr)
        sc = sc.replace("pytest", c3 + "pytest" + cr)
        sc = sc.replace("--help", c4 + "--help" + cr)
        sc = sc.replace("help", c4 + "help" + cr)
    print(sc)


def show_basic_usage():
    import time
    time.sleep(0.25)  # Enough time to see the logo
    show_package_location()
    show_version_info()
    print("")
    sc = ""
    sc += ' * USAGE: "appiumbase [COMMAND] [PARAMETERS]"\n'
    sc += ' *    OR:        "abase [COMMAND] [PARAMETERS]"\n'
    sc += "\n"
    sc += "COMMANDS:\n"
    sc += "      methods         (List common Python methods)\n"
    sc += "      options         (List common pytest options)\n"
    sc += "      mkdir           [DIRECTORY] [OPTIONS]\n"
    sc += "      print           [FILE] [OPTIONS]\n"
    sc += ' * (EXAMPLE: "sbase install chromedriver latest")  *\n'
    sc += ""
    if "linux" not in sys.platform:
        c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
        c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
        cr = colorama.Style.RESET_ALL
        sc = sc.replace("appiumbase", c1 + "appium" + c2 + "base" + cr)
        sc = sc.replace("abase", c1 + "a" + c2 + "base" + cr)
    print(sc)



def show_mkdir_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = "  " + c2 + "** " + c3 + "mkdir" + c2 + " **" + cr
    print(sc)
    print("")
    print("  Usage:")
    print("           appiumbase mkdir [DIRECTORY] [OPTIONS]")
    print("           OR:    abase mkdir [DIRECTORY] [OPTIONS]")
    print("  Example:")
    print("           abase mkdir ui_tests")
    print("  Options:")
    print("         -b / --basic  (Only config files. No tests added.)")
    print("  Output:")
    print("           Creates a new folder for running ABase scripts.")
    print("           The new folder contains default config files,")
    print("           sample tests for helping new users get started,")
    print("           and Python boilerplates for setting up customized")
    print("           test frameworks.")
    print("")


def show_print_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = "  " + c2 + "** " + c3 + "print" + c2 + " **" + cr
    print(sc)
    print("")
    print("  Usage:")
    print("         appiumbase print [FILE] [OPTIONS]")
    print("         OR:    abase print [FILE] [OPTIONS]")
    print("  Options:")
    print("         -n   (Add line Numbers to the rows)")
    print("  Output:")
    print("         Prints the code/text of any file")
    print("         with syntax-highlighting.")
    print("")


def show_extract_objects_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = "  " + c2 + "** " + c3 + "extract-objects" + c2 + " **" + cr
    print(sc)
    print("")
    print("  Usage:")
    print("           appiumbase extract-objects [SB_FILE.py]")
    print("           OR:    sbase extract-objects [SB_FILE.py]")
    print("  Output:")
    print("           Creates page objects based on selectors found in a")
    print("           appiumbase Python file and saves those objects to the")
    print('           "page_objects.py" file in the same folder as the tests.')
    print("")


def show_inject_objects_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = "  " + c2 + "** " + c3 + "inject-objects" + c2 + " **" + cr
    print(sc)
    print("")
    print("  Usage:")
    print("           appiumbase inject-objects [SB_FILE.py] [OPTIONS]")
    print("           OR:    sbase inject-objects [SB_FILE.py] [OPTIONS]")
    print("  Options:")
    print("           -c, --comments  (Add object selectors to the comments.)")
    print("                           (Default: No added comments.)")
    print("  Output:")
    print('           Takes the page objects found in the "page_objects.py"')
    print("           file and uses those to replace matching selectors in")
    print("           the selected appiumbase Python file.")
    print("")


def show_objectify_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = "  " + c2 + "** " + c3 + "objectify" + c2 + " **" + cr
    print(sc)
    print("")
    print("  Usage:")
    print("           appiumbase objectify [SB_FILE.py] [OPTIONS]")
    print("           OR:    sbase objectify [SB_FILE.py] [OPTIONS]")
    print("  Options:")
    print("           -c, --comments  (Add object selectors to the comments.)")
    print("                           (Default: No added comments.)")
    print("  Output:")
    print("           A modified version of the file where the selectors")
    print("           have been replaced with variable names defined in")
    print('           "page_objects.py", supporting the Page Object Pattern.')
    print("")
    print('           (appiumbase "objectify" has the same outcome as')
    print('            combining "extract-objects" with "inject-objects")')
    print("")


def show_revert_objects_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = "  " + c2 + "** " + c3 + "revert-objects" + c2 + " **" + cr
    print(sc)
    print("")
    print("  Usage:")
    print("           appiumbase revert-objects [SB_FILE.py] [OPTIONS]")
    print("           OR:    sbase revert-objects [SB_FILE.py] [OPTIONS]")
    print("  Options:")
    print("           -c, --comments  (Keep existing comments for the lines.)")
    print("                           (Default: No comments are kept.)")
    print("  Output:")
    print('           Reverts the changes made by "appiumbase objectify" or')
    print('           "appiumbase inject-objects" when run against a')
    print("           appiumbase Python file. Objects will get replaced by")
    print('           selectors stored in the "page_objects.py" file.')
    print("")


def show_encrypt_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = "  " + c2 + "** " + c3 + "encrypt OR obfuscate" + c2 + " **" + cr
    print(sc)
    print("")
    print("  Usage:")
    print("           appiumbase encrypt   ||   appiumbase obfuscate")
    print("                                --OR--")
    print("                  sbase encrypt   ||          sbase obfuscate")
    print("  Output:")
    print("           Runs the password encryption/obfuscation tool.")
    print("           (Where you can enter a password to encrypt/obfuscate.)")
    print("")


def show_decrypt_usage():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = "  " + c2 + "** " + c3 + "decrypt OR unobfuscate" + c2 + " **" + cr
    print(sc)
    print("")
    print("  Usage:")
    print("           appiumbase decrypt   ||   appiumbase unobfuscate")
    print("                                --OR--")
    print("                  sbase decrypt   ||          sbase unobfuscate")
    print("  Output:")
    print("           Runs the password decryption/unobfuscation tool.")
    print("           (Where you can enter an encrypted password to decrypt.)")
    print("")



def get_version_info():
    # from pkg_resources import get_distribution
    # version = get_distribution("appiumbase").version
    from appiumbase import __version__

    version_info = None
    c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sb_text = c1 + "appiium" + c2 + "base" + cr
    version_info = "%s %s%s%s" % (sb_text, c3, __version__, cr)
    return version_info


def show_version_info():
    version_info = get_version_info()
    print("%s" % version_info)


def get_package_location():
    # from pkg_resources import get_distribution
    # location = get_distribution("appiumbase").location
    import os
    import appiumbase

    location = os.path.dirname(os.path.realpath(appiumbase.__file__))
    if location.endswith("appiumbase"):
        location = location[0 : -len("appiumbase")]  # noqa: E203
    return location


def show_package_location():
    location = get_package_location()
    print("%s" % location)


def show_methods():
    c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    c4 = colorama.Fore.MAGENTA + colorama.Back.LIGHTYELLOW_EX
    c5 = colorama.Fore.LIGHTRED_EX + colorama.Back.LIGHTGREEN_EX
    cr = colorama.Style.RESET_ALL
    sc = (
        "\n " + c2 + " ** " + c3 + " appiumbase Python Methods "
        "" + c2 + " ** " + cr
    )
    print(sc)
    print("")
    line = "Here are some common methods that come with appiumbase:"
    line = c1 + line + cr
    print(line)
    line = "(Some optional args are not shown here)"
    print(line)
    print("")
    sbm = ""
    sbm += "*.click(selector) => Click on the element.\n"
    sbm += "*.wait_for_element_present(selector) => Wait for the element to be present"
    sbm = sbm.replace("*.", "self." + c1).replace("(", cr + "(")
    sbm = sbm.replace("self.", c2 + "self" + c5 + "." + cr)
    sbm = sbm.replace("(", c3 + "(" + c4)
    sbm = sbm.replace(")", c3 + ")" + cr)
    print(sbm)


def show_options():
    c1 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    c4 = colorama.Fore.MAGENTA + colorama.Back.LIGHTYELLOW_EX
    c5 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
    cr = colorama.Style.RESET_ALL
    sc = "\n " + c2 + " ** " + c3 + " pytest CLI Options " + c2 + " ** " + cr
    print(sc)
    print("")
    line = "Here are some common pytest options to use with appiumbase:"
    line = c1 + line + cr
    print(line)
    line = '(Some options are Chromium-specific, e.g. "--guest --mobile")'
    print(line)
    op = "\n"
    op += '--device=Device  (The device is in use. Default is "android")\n'
    op += "--slow  (Slow down the automation. Faster than using Demo Mode.)\n"
    op += "--reuse-session / --rs  (Reuse browser session between tests.)\n"
    op += "--dashboard  (Enable appiumbase's Dashboard at dashboard.html)\n"
    op += "-m=MARKER  (Run tests with the specified pytest marker.)\n"
    op += "-n=NUM  (Multithread the tests using that many threads.)\n"
    op += "-v  (Verbose mode. Print the full names of each test run.)\n"
    op += "--html=report.html  (Create a detailed pytest-html report.)\n"
    op += "--collect-only / --co  (Only show discovered tests. No run.)\n"
    op += "--co -q  (Only show full names of discovered tests. No run.)\n"
    op += "--pdb  (Enter the Post Mortem Debug Mode after any test fails.)\n"
    op += "--trace  (Enter Debug Mode immediately after starting any test.)\n"
    op += "      | Debug Mode Commands  >>>   help / h: List all commands. |\n"
    op += "      |   n: Next line of method. s: Step through. c: Continue. |\n"
    op += "      |  return / r: Run until method returns. j: Jump to line. |\n"
    op += "      | where / w: Show stack spot. u: Up stack. d: Down stack. |\n"
    op += "      | longlist / ll: See code. dir(): List namespace objects. |\n"
    op += "-x  (Stop running the tests after the first failure is reached.)\n"
    op += "--archive-logs  (Archive old log files instead of deleting them.)\n"
    op += "--mobile  (Use mobile device emulator during tests.)\n"
    op += "--settings-file=FILE  (Override default appiumbase settings.)\n"
    op += '--env=ENV  (Set the test env. Access with "self.env" in tests.)\n'
    op += '--data=DATA  (Extra test data. Access with "self.data" in tests.)\n'
    op += cr
    op = op.replace("\n-", "\n" + c1 + "-").replace("  (", cr + "  (")
    op = op.replace(" / -", cr + " / " + c1 + "-")
    op = op.replace("=", c2 + "=" + c3)
    op = op.replace(" | ", " |" + c3 + " ").replace("|\n", cr + "|\n")
    op = op.replace(": ", c5 + ":" + c3 + " ")
    op = op.replace("Debug Mode Commands", c5 + "Debug Mode Commands" + c3)
    op = op.replace(">>>", c4 + ">>>" + c3)
    print(op)
    line = "For the full list of " + c2 + "command-line options" + cr
    line += ', type: "' + c3 + "pytest" + cr + " " + c1 + "--help" + cr + '".'
    print(line)
    print("")


def show_detailed_help():
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    c3 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    c6 = colorama.Back.CYAN
    cr = colorama.Style.RESET_ALL
    show_basic_usage()
    print(c6 + "            " + c2 + "  Commands:  " + c6 + "            ")
    print(cr)
    show_mkdir_usage()
    print('* (Use "' + c3 + "pytest" + cr + '" for running tests) *\n')


def main():
    command = None
    command_args = None
    num_args = len(sys.argv)
    if num_args == 1:
        show_usage()
        return
    elif num_args == 2:
        command = sys.argv[1]
        command_args = []
    elif num_args > 2:
        command = sys.argv[1]
        command_args = sys.argv[2:]
    command = command.lower()

    if command == "mkdir":
        if len(command_args) >= 1:
            from appiumbase.console_scripts import ab_mkdir

            ab_mkdir.main()
        else:
            show_basic_usage()
            show_mkdir_usage()
    elif command == "methods" or command == "--methods":
        show_methods()
    elif command == "options" or command == "--options":
        show_options()
    elif command == "help" or command == "--help":
        if len(command_args) >= 1:
            if command_args[0] == "mkdir":
                print("")
                show_mkdir_usage()
                return
        show_detailed_help()
    else:
        show_usage()
        colorama.init(autoreset=True)
        c5 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
        c7 = colorama.Fore.BLACK + colorama.Back.MAGENTA
        cr = colorama.Style.RESET_ALL
        invalid_cmd = "===> INVALID COMMAND: >> %s <<\n" % command
        invalid_cmd = invalid_cmd.replace(">> ", ">>" + c5 + " ")
        invalid_cmd = invalid_cmd.replace(" <<", " " + cr + "<<")
        invalid_cmd = invalid_cmd.replace(">>", c7 + ">>" + cr)
        invalid_cmd = invalid_cmd.replace("<<", c7 + "<<" + cr)
        print(invalid_cmd)


if __name__ == "__main__":
    main()