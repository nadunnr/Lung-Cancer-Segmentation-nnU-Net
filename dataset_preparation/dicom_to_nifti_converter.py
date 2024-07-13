import dicom2nifti
import os
import glob
import pydicom
import nibabel
import shutil
import tqdm

def lenof_dicom_dir(curr_path):
    '''function to check if the current directory havin any daicom files'''
    num_dcm = len(glob.glob(os.path.join(curr_path, '*.dcm')))
    return num_dcm

count = 0 #number of nifti files
input_path = 'D:/ScholarX/Dataset/'  #input file path to NSCLC Radiogenomics directory
output_path = 'D:/ScholarX/Output/'                              #output directory
test_input = 'D:/ScholarX/Dataset/'

# Used recursive glob to find all subdirectories
dicom_files = glob.iglob(os.path.join(input_path, '**'), recursive=True)

for i, file in enumerate(dicom_files):
    if "PET" not in file.upper():

        dcm_quantity = lenof_dicom_dir(file)  #number of dicom files in the directory
        if dcm_quantity:

            # directory having dicom files
            input_dir = os.path.dirname(file)

            if len(os.listdir(input_dir)) == 2:

                # output directory of the corresponding nifti file
                new_dir = os.path.join(output_path, input_dir[24:])
                os.makedirs(new_dir, exist_ok=True)

                #checking the number of dcms
                if dcm_quantity > 1:
                    #converting dicom directory to nifti
                    dicom2nifti.convert_directory(file, new_dir)
                    count += 1

                elif dcm_quantity == 1:
                    dcm_file = os.listdir(file)
                    dicom_path = os.path.join(file, dcm_file[0])

                    parent_dir = os.path.basename(os.path.dirname(dicom_path))
                    out_path_2 = new_dir + '/' + str(parent_dir) + '.dcm'

                    shutil.copy(dicom_path, out_path_2)
                    #tried
                    #dicom2nifti.convert_dicom.dicom_array_to_nifti(glob.glob(os.path.join(file, '*.dcm')), new_dir)

                print(os.path.basename(os.path.dirname(input_dir)))

num_patients = len(os.listdir(output_path))
print(f"{count} files from {num_patients} patients, successfully converted")