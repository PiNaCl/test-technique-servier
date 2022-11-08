import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from resources import dataframe_from_files


__all__ = ["dataframe_from_files"]
