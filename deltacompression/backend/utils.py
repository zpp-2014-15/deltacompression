"""Functions and classes used in multiple modules"""

import os
import os.path as op

def getAllDirectories(directory):
    """
    Args:
        directory: path to the directory
    Returns:
        a lexicographically sorted list of subdirectories of a given directory
    Raises:
        OSError in case the argument was not a valid directory
    """
    all_files = [op.join(directory, file_name)
                 for file_name in os.listdir(directory)]
    return sorted(filter(op.isdir, all_files))
