"""Spec Sheet.

Command to produce navigable documentation from Gherkin feature files.

Usage:
    specsheet [options] SOURCES

Arguments:
    SOURCES     directory containing gherkin features

Options:
    -h --help           Show this help.
    -v --version        Show version.

"""
from docopt import docopt
from specsheet import __version__


def main():
    """Main entry-point for the photo-import command.

    Processes all provided arguments, and performs the desired actions before
    exiting.
    """
    docopt(__doc__, version=__version__)
    exit(0)
