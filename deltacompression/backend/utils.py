import os
import os.path as op

def getAllDirectories(directory):
    all_files = [op.join(directory, file_name)
                 for file_name in os.listdir(directory)]
    return sorted(filter(op.isdir, all_files))
