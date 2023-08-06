import pathlib
import numpy as np
from scipy.io import loadmat
from pysoc.soc import helm


MAT_FILES_FOLDERPATH = pathlib.Path(__file__).parent.parent / 'mat_files'

HEN_INPUT_FOLDERPATH = MAT_FILES_FOLDERPATH / 'input'

input_contents = loadmat(HEN_INPUT_FOLDERPATH / 'column_soc_input.mat')

# input variables
Gy = input_contents["Gy"]
Gyd = input_contents["Gyd"]
Juu = input_contents["Juu"]
Jud = input_contents["Jud"]
md = input_contents["md"].flatten()
me = input_contents["me"].flatten()


worst_loss_py, avg_loss_py, index_CV_py, *_ = helm(Gy, Gyd, Juu, Jud,
                                                   md, me, ss_size=1,
                                                   nc_user=5)

a = 1
