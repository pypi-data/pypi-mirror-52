"""
Basic command line interface
"""
import os
from typing import List

from ldrand.linker import process_linker
from ldrand.util import BIN_PATH

VERSION = "0.42"


def run(args: List[str]):
    """
    Processes the arguments and calls the linker wrapper
    :param args: arguments to process
    """
    process_linker(args)


def runp():
    """
    Outputs the path to the ``bin`` folder
    """
    print(BIN_PATH)
