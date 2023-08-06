"""Starts the program."""

import signal
import sys

try:
    from gi.repository import GLib
except ImportError:
    print("-" * 79)
    print("please do sudo apt install python-gi")
    print("-" * 79)
    raise

from xpl import __config__
from xpl.xpl import XPL


def main():
    """Runs app from xpl.xpl module."""
    app = XPL()
    GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, app.on_quit)
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)


if __name__ == "__main__":
    main()

#TODO make peaks clickable
