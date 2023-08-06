"""
Localizaton support and helper functions.
"""

import os
import locale
import gettext
from typing import List


# The currently active locale
LOCALE = None

# The absolute path to the locale directory
LOCALE_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'locale')

# The currently active translation
TRANSLATION = None


def detect_locale() -> str:
    """
    Detect the current system locale
    """
    return locale.getdefaultlocale()[0]


def set_locale(locale: str):
    """
    Update the globals TRANSLATION and LOCALE to use the specified locale.
    """
    global LOCALE
    global TRANSLATION
    LOCALE = locale
    TRANSLATION = gettext.translation(
        'hellojr',
        localedir=LOCALE_ROOT,
        languages=[locale],
        fallback=True)


# Set the default locale and activate it
LOCALE = detect_locale()
set_locale(LOCALE)


# Determine the available languages
def get_languages() -> List[str]:
    """
    Determine the available languages.
    """
    # Look at the directories in LOCALE_ROOT and return there names
    return [os.path.basename(path[0]) for path in os.walk(LOCALE_ROOT)]


# Wrapper that allows the current language to
def _(*args, **kwargs) -> str:
    """
    Wrapper around gettext to ensure the active language is utilized.
    """
    return TRANSLATION.gettext(*args, **kwargs)
