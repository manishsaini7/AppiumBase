"""
This module contains shared utility methods.
"""
import time
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchAttributeException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import NoSuchWindowException
from appiumbase.common.exceptions import TimeLimitExceededException
from appiumbase import config as ab_config


def format_exc(exception, message):
    """
    Formats an exception message to make the output cleaner.
    """
    if exception == Exception:
        exc = Exception
        return exc, message
    elif exception == ElementNotVisibleException:
        exc = ElementNotVisibleException
    elif exception == "ElementNotVisibleException":
        exc = ElementNotVisibleException
    elif exception == NoSuchElementException:
        exc = NoSuchElementException
    elif exception == "NoSuchElementException":
        exc = NoSuchElementException
    elif exception == NoAlertPresentException:
        exc = NoAlertPresentException
    elif exception == "NoAlertPresentException":
        exc = NoAlertPresentException
    elif exception == NoSuchAttributeException:
        exc = NoSuchAttributeException
    elif exception == "NoSuchAttributeException":
        exc = NoSuchAttributeException
    elif exception == NoSuchFrameException:
        exc = NoSuchFrameException
    elif exception == "NoSuchFrameException":
        exc = NoSuchFrameException
    elif exception == NoSuchWindowException:
        exc = NoSuchWindowException
    elif exception == "NoSuchWindowException":
        exc = NoSuchWindowException
    elif type(exception) is str:
        exc = Exception
        message = "%s: %s" % (exception, message)
        return exc, message
    else:
        exc = Exception
        return exc, message
    message = _format_message(message)
    return exc, message


def _format_message(message):
    message = "\n " + message
    return message


def __time_limit_exceeded(message):
    raise TimeLimitExceededException(message)


def check_if_time_limit_exceeded():
    time_limit = 1000
    now_ms = int(time.time() * 1000)
    if now_ms > ab_config.start_time_ms + ab_config.time_limit_ms:
        display_time_limit = time_limit
        plural = "s"
        if float(int(time_limit)) == float(time_limit):
            display_time_limit = int(time_limit)
            if display_time_limit == 1:
                plural = ""
        message = (
                "This test has exceeded the time limit of %s second%s!"
                % (display_time_limit, plural)
            )
        message = _format_message(message)
        __time_limit_exceeded(message)