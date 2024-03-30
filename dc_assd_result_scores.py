import sys
import os
import time
import pandas as pd
# import utils
import nibabel as nib

from medpy.metric import dc, assd
#I had to change "Path to python\Lib\site-packages\medpy\metric\binary.py" script to get it run.
#Try these changes in above file if this gives this error "FutureWarning: In the future `np.bool` will be defined as the corresponding NumPy scalar."
#If this error happens, "`np.bool` was a deprecated alias for the builtin `bool`."
#Change "astype(numpy.bool)" to "astype(numpy.bool)" in lines 68,69, 1200, 1201.

import numpy as np
import glob

MAX_VALUE_ASSD = 350 #mm
DEBBUGING =  False


#add corresponding paths
segmentation_path = 'D:/ScholarX/nnU-Net/Results/'
path_2d = 'D:/ScholarX/nnU-Net/Results/2d/190/nnUNetTrainerASSDLoss/gamma_0.0/'
path_3dfullres = 'D:/ScholarX/nnU-Net/Results/3dfullres/190/nnUNetTrainerASSDLoss/gamma_0.0/'
path_3dlowres = 'D:/ScholarX/nnU-Net/Results/3dlowres/190/nnUNetTrainerASSDLoss/gamma_0.0/'
path_groundtruth = 'D:/ScholarX/nnU-Net/nnUNet_raw/Dataset001_LungCancer/labelsTs/'
results_path = "D:/ScholarX/nnU-Net/" 

def score(labels_seg_path, pred_list):

    """Compute and return scores for each scan."""
    # scores = []
    df_metric = {
        'scan_id':[],
        'tumour_Dice':[],
        'tumour_ASSD':[],
        }
    
    for pred in pred_list:
        
        scan_id = os.path.basename(pred)[-15:-7]
        label = os.path.join(labels_seg_path, f"{scan_id}.nii.gz")

        # try:
        print(scan_id)
        print(f"label: {label}")
        df_metric['scan_id'].append(scan_id)

        #run_captk(captk_path, pred, label, tmp_output)
        label_seg_array = np.round(nib.load(label).get_fdata())
        pred_array = nib.load(pred).get_fdata()
        
        # Voxel spacing
        affine = nib.load(label).affine
        voxel_spacing = [abs(affine[k, k]) for k in range(3)]

        # whole tumour VS 
        label_VS = (label_seg_array == 1).astype(int) 
        pred_VS = (pred_array == 1).astype(int) 

        df_metric['tumour_Dice'].append(dc(pred_VS, label_VS))

        if DEBBUGING:
            df_metric['tumour_ASSD'].append(10)
        else:
            if np.sum(pred_VS) > 0:
                df_metric['tumour_ASSD'].append(assd(pred_VS, label_VS, voxelspacing=voxel_spacing))
            else:
                df_metric['tumour_ASSD'].append(MAX_VALUE_ASSD)

    return pd.DataFrame.from_dict(df_metric).set_index('scan_id')   #.sort_values(by="")


def main():
    """Main function."""
    #add path to the predicted segmentation files of the required configuration
    configurations = [path_2d, path_3dlowres, path_3dfullres]

    for config in configurations:

        input_config_preds = config
        print(f"{input_config_preds.split('/')[4]}\n")

        preds = glob.glob('%s/*.nii.gz'%(input_config_preds))

        print("Preds")
        for pred in preds:
            print(pred)
        
        print("\nResults...\n")
        results = score(path_groundtruth, preds)

        # Get number of segmentations predicted by participant, number of
        # segmentation that could not be scored, and number of segmentations
        # that were scored.
        
        print(results)
        results.loc["mean"] = results.mean()
        results.loc["sd"] = results.std()
        results.loc["median"] = results.median()
        results.loc["25quantile"] = results.quantile(q=0.25)
        results.loc["75quantile"] = results.quantile(q=0.75)

        # CSV file of scores for all scans.
        file_name = str(input_config_preds.split('/')[4]) + "_results.csv"
        current_directory = os.getcwd()
        results_path = os.path.join(current_directory,'/result_scores/')
        out_path = os.path.join(results_path, file_name)
        results.to_csv(out_path)

    print('Succesfully evaluated!')

if __name__ == "__main__":
    main()
