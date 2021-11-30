# --------------------
# SUPPRESSPRINT.PY
# - SuppressPrint class
#   - Sole purpose of suppressing Python terminal output
#   - For debugging only; specifically, .textAlgorithms() method of Maze class
# --------------------

import os, sys

# CITATION
#
# Source code for SuppressPrint class that helps in suppressing Python
# terminal output by redirecting all output to null.
#
# I have only made minimal changes to the original code and do not claim
# credit for any of it.
#
# This code is only used for debugging and testing (in particular, the single
# .testAlgorithms() method of the Maze class. It is never run during gameplay.
#
# Source: https://stackoverflow.com/questions/6735917
# (It appears that the StackOverflow response providing this code has since
# been taken down.)

class SuppressPrint():
    def __enter__(self):
        self.__original__stdout = sys.stdout
        sys.stdout = open("nul", "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self.__original__stdout