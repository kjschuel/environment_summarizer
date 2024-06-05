import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.gatherers import get_python_version

if __name__ == "__main__":
    print(get_python_version())
