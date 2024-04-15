import os
import glob
import nibabel as nib
import numpy as np

def is_segmentation_nii(curr_path):

    if os.path.isfile(curr_path):
        file_name = os.path.basename(curr_path)

        if ("3D Slicer segmentation" in file_name) and (".nii" in file_name):
            return True
        else:
            return False

def generate_mask(curr_path):
    return os.path.dirname(curr_path) + '/Masked - ' + os.path.basename(curr_path)


count = 0
data_path = 'D:/ScholarX/Output/'

# Used recursive glob to find all subdirectories
files = glob.iglob(os.path.join(data_path, '**'), recursive=True)

for i, file in enumerate(files):
    if is_segmentation_nii(file):
        try:
            nifti_file = nib.load(file)
            pixel_array = nifti_file.get_fdata()
    
            #converting white colour segmented pixels for dark colour
            pixel_array[pixel_array == 255] = 1
    
            #In this dataset, segmentation files are being flipped when loaded
            #Therefore we flip the segmentation mask to obtain the wanted one
            pixel_array = np.flip(pixel_array, axis = 1)
    
            #Save the pixel array as a nifti file
            array_image = nib.Nifti1Image(pixel_array, nifti_file.affine)
    
            #save path
            nifti_out_path = generate_mask(file)
            nib.save(array_image, nifti_out_path)

            count += 1
            print(count)

        except:
            print("There was a error when converting.")
            print(file)


