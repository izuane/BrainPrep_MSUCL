import os
import glob
import shutil
from tqdm import *
from subprocess import check_call

ISBI_TRAIN_DIR = 'ISBI_train'
ISBI_TEST_DIR = 'ISBI_test'

NII_EXT = '.nii'
NII_GZ_EXT = '.nii.gz'

'''
This script helps reorganise the ISBI dataset downloaded from https://smart-stats-tools.org/lesion-challenge-2015
into a directory structure that the remaining scripts of this project are programmed to handle.

You can simply download the training and test data from smart-stats-tools.org, extract them into the /data directory
of this project. BUT you MUST make sure to rename the names names of the (extracted) train and test sets to "train" 
and "test respectively before you place them into the /data directory of this project.
'''


def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return

parent_dir = os.path.dirname(os.getcwd())
data_dir = os.path.join(parent_dir, "data")

create_dir(os.path.join(data_dir, ISBI_TRAIN_DIR))
create_dir(os.path.join(data_dir, ISBI_TEST_DIR))

for sub_dir, dirs, files in os.walk(data_dir):
    for f in tqdm(files):
        ext = f.split('.')

        # Get ".nii" extension
        if len(ext) == 2:
            ext = '.{0}'.format(ext[1])

        # Get ".nii.gz" extension
        elif len(ext) == 3:
            ext = '.{0}.{1}'.format(ext[1], ext[2])
        
        
        # Only look at the original/unprocessed MR scans
        dir = sub_dir.split('/')[-1]
        if dir == 'orig':

            # Find out if the "orig" directory we're in is for the training data or test data
            dir = sub_dir.split('/')[-3]
            is_train_dir = (dir == 'train')

            if (ext == NII_EXT) or (ext == NII_GZ_EXT):
                    f_path = os.path.join(sub_dir, f)

                    # Create 01_01, 01_02, etc. dirs in ISBI_TRAIN_DIR or ISBI_TEST_DIR and copy respect files over to this

                    subject, scan_num, _  = f.split('_')
                    subject_num = subject[-2] + subject[-1]

                    if is_train_dir:
                        out_f_dir = os.path.join(data_dir, ISBI_TRAIN_DIR, '{0}_{1}'.format(subject_num, scan_num))
                    else:
                        out_f_dir = os.path.join(data_dir, ISBI_TEST_DIR, '{0}_{1}'.format(subject_num, scan_num))
                    create_dir(out_f_dir)

                    out_f_path = os.path.join(out_f_dir, f)

                    shutil.copyfile(f_path, out_f_path)