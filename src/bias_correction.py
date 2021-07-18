from __future__ import print_function

import os
from multiprocessing import Pool, cpu_count
from nipype.interfaces.ants.segmentation import N4BiasFieldCorrection

ISBI_TRAIN_DIR = 'ISBI_train'
ISBI_TEST_DIR = 'ISBI_test'

def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def unwarp_bias_field_correction(arg, **kwarg):
    return bias_field_correction(*arg, **kwarg)


def bias_field_correction(src_path, dst_path):
    print("N4ITK on: ", src_path)
    try:
        n4 = N4BiasFieldCorrection()
        n4.inputs.input_image = src_path
        n4.inputs.output_image = dst_path

        n4.inputs.dimension = 3
        n4.inputs.n_iterations = [100, 100, 60, 40]
        n4.inputs.shrink_factor = 3
        n4.inputs.convergence_threshold = 1e-4
        n4.inputs.bspline_fitting_distance = 300
        n4.run()
    except RuntimeError:
        print("\tFailed on: ", src_path)

    return

for ISBI_DIR in [ISBI_TRAIN_DIR, ISBI_TEST_DIR]:
    parent_dir = os.path.dirname(os.getcwd())
    data_dir = os.path.join(parent_dir, "data")
    data_src_dir = os.path.join(data_dir, "{0}_brain".format(ISBI_DIR))
    data_dst_dir = os.path.join(data_dir, "{0}_denoise".format(ISBI_DIR))
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
    # bias_field_correction(data_src_paths[0], data_dst_paths[0])

    # Multi-processing
    paras = zip(data_src_paths, data_dst_paths)
    pool = Pool(processes=cpu_count())
    pool.map(unwarp_bias_field_correction, paras)
