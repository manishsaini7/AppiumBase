class Environment:
    # Usage Example => "--env=qa" => Then access value in tests with "self.env"
    QA = "qa"
    STAGING = "staging"
    DEVELOP = "develop"
    PRODUCTION = "production"
    MASTER = "master"
    LOCAL = "local"
    TEST = "test"

class Files:
    DOWNLOADS_FOLDER = "downloaded_files"
    ARCHIVED_DOWNLOADS_FOLDER = "archived_files"


class Values:
    # Demo Mode has slow scrolling to see where you are on the page better.
    # However, a regular slow scroll takes too long to cover big distances.
    # If the scroll distance is greater than SSMD, a slow scroll speeds up.
    SSMD = 900  # Smooth Scroll Minimum Distance (for advanced slow scroll)


class ValidDevices:
    valid_devices = [
        "android",
        "iphone",
        "ipad",
        "remote",
    ]

class Devices:
    ANDROID = "android"
    IPHONE = "iphone"
    IPAD = "ipad"
    REMOTE = "remote"
    VERSION = {
        "android": None,
        "iphone": None,
        "ipad": None,
        "remote": None,
    }

    LATEST = {
        "android": None,
        "iphone": None,
        "ipad": None,
        "remote": None,
    }

class State:
    PASSED = "Passed"
    FAILED = "Failed"
    SKIPPED = "Skipped"
    UNTESTED = "Untested"
    ERROR = "Error"
    BLOCKED = "Blocked"
    DEPRECATED = "Deprecated"