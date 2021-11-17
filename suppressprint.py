import os, sys

# For testing and debugging only
#   From https://stackoverflow.com/questions/6735917
class SuppressPrint():
    def __enter__(self):
        self.__original__stdout = sys.stdout
        sys.stdout = open("nul", "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self.__original__stdout