from __future__ import print_function

import os
import subprocess
from multiprocessing import Pool, cpu_count

ISBI_TRAIN_DIR = 'ISBI_train'
ISBI_TEST_DIR = 'ISBI_test'

def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def bet(src_path, dst_path, frac="0.5"):
    command = ["bet", src_path, dst_path, "-R", "-f", frac, "-g", "0"]
    subprocess.call(command)
    return


def unwarp_strip_skull(arg, **kwarg):
    return strip_skull(*arg, **kwarg)


def strip_skull(src_path, dst_path, frac="0.4"):
    print("Working on :", src_path)
    try:
        bet(src_path, dst_path, frac)
    except RuntimeError:
        print("\tFailed on: ", src_path)

    return

for ISBI_DIR in [ISBI_TRAIN_DIR, ISBI_TEST_DIR]:
    parent_dir = os.path.dirname(os.getcwd())
    data_dir = os.path.join(parent_dir, "data")
    data_src_dir = os.path.join(data_dir, "{0}_reg".format(ISBI_DIR))
    data_dst_dir = os.path.join(data_dir, "{0}_brain".format(ISBI_DIR))
    create_dir(data_dst_dir)

    # Create the 01_01, etc. folder structure from data_src_dir, but in data_dst_dir
    data_src_paths, data_dst_paths = [], []
    for dir in os.listdir(data_src_dir):
        src_dir = os.path.join(data_src_dir, dir)
        dst_dir = os.path.join(data_dst_dir, dir)
        create_dir(dst_dir)

        for f in os.listdir(src_dir):
            f_src_path = os.path.join(src_dir, f)
            f_dst_path = os.path.join(dst_dir, f)
            data_src_paths.append(f_src_path)
            data_dst_paths.append(f_dst_path)
    # Test
    # strip_skull(data_src_paths[0], data_dst_paths[0])

    # Multi-processing
    paras = zip(data_src_paths, data_dst_paths)
    pool = Pool(processes=cpu_count())
    pool.map(unwarp_strip_skull, paras)



