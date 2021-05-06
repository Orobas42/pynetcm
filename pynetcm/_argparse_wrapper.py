from __future__ import absolute_import
import argparse

class ArgparseWrapper(object):

    def __init__(self, version, description="", epilog=""):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=description, epilog=epilog)
        self.parser.add_argument(
            "--version", action="version", version="%(prog)s " + version)
