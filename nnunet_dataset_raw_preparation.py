import os
import shutil
import glob

#define training and test data set size
tr_set_last_idx = 79

#directories
input_path = 'D:/ScholarX/Dataset_77/'
output_path = 'D:/ScholarX/nnU-Net/nnUNet_raw/Dataset001_LungCancer/'

def file_type(file_name):
    '''To check the file type from the name'''
    if "nii.gz" in file_name:
        if "main" in file_name:
            return "image"
        elif "segmentation" in file_name:
            return "label"
        
def patient_id(file_name):
    id = os.path.basename(os.path.dirname(file_name))
    return id

def destination_path(file):
    '''generating the destination path according to the file'''

    id = patient_id(file)
    
    if int(id) <= tr_set_last_idx:
        if file_type(file) == "image":
            extension = "imagesTr/lung_" + id + "_0000.nii.gz"
            dest = os.path.join(output_path, extension)
        elif file_type(file) == "label":
            extension = "labelsTr/lung_" + id + ".nii.gz"
            dest = os.path.join(output_path, extension)

    elif int(id) > tr_set_last_idx:
        if file_type(file) == "image":
            extension = "imagesTs/lung_" + id + "_0000.nii.gz"
            dest = os.path.join(output_path, extension)
        elif file_type(file) == "label":
            extension = "labelsTs/lung_" + id + ".nii.gz"
            dest = os.path.join(output_path, extension)   

    return dest    

# Used recursive glob to find all subdirectories
in_files = glob.iglob(os.path.join(input_path, '**'), recursive=True)

#define needed constants
error_cases = 0
success_images = 0
success_labels = 0

for i, file in enumerate(in_files):

    if os.path.isfile(file):

        dest_path = destination_path(file)

        try:
            shutil.copy(file, dest_path)
        except:
            print("An error occured.")
            error_cases += 1
        else:
            if file_type(file) == "image":
                success_images += 1
            elif file_type(file) == "label":
                success_labels += 1

print(f"error cases: {error_cases}")
print(f"successfully copied images: {success_images}")
print(f"successfully copied labels: {success_labels}")
                 
