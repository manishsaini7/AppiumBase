# #####>>>>>----- REQUIRED/IMPORTANT SETTINGS -----<<<<<#####

# Default maximum time (in seconds) to wait for page elements to appear.
# Different methods/actions in base_case.py use different timeouts.
# If the element to be acted on does not appear in time, the test fails.

MINI_TIMEOUT = 2
SMALL_TIMEOUT = 6
LARGE_TIMEOUT = 10
EXTREME_TIMEOUT = 30


# Default time to wait after each element action performed during Demo Mode.
# Use Demo Mode when you want others to see what your automation is doing.
# Usage: "--demo_mode". (Can be overwritten by using "--demo_sleep=TIME".)
DEFAULT_DEMO_MODE_TIMEOUT = 0.5