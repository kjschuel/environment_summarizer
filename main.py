"""
For testing purposes. 
Will be removed when the module is complete.

"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import src.utils as utils

if __name__ == "__main__":
    utils.write_versions()
