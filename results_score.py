#!/usr/bin/env python3
import sys
import os
import subprocess
import argparse
import json
import time
import pandas as pd
# import utils
import nibabel as nib
from medpy.metric import dc, assd
import numpy as np
from skimage.segmentation import find_boundaries
import glob

MAX_VALUE_ASSD = 350 #mm
DEBBUGING =  False


def score(parent, pred_lst, tmp_output="tmp.csv"):
    """Compute and return scores for each scan."""
    # scores = []
    df_metric = {
        'scan_id':[],
        'tumour_Dice':[],
        'tumour_ASSD':[],
        }
    for pred in pred_lst:
        start = time.process_time()
        scan_id = os.path.basename(pred)[-15:-7]
        gold = os.path.join(parent, f"{scan_id}.nii.gz")
        # try:
        print(scan_id)
        df_metric['scan_id'].append(scan_id)
        #run_captk(captk_path, pred, gold, tmp_output)
        gt_array = np.round(nib.load(gold).get_fdata())
        pred_array = nib.load(pred).get_fdata()
        # Voxel spacing
        affine = nib.load(gold).affine
        vxlspacing = [abs(affine[k, k]) for k in range(3)]
        # whole tumour VS 
        gt_VS = (gt_array == 1).astype(int) 
        pred_VS = (pred_array == 1).astype(int) 

        df_metric['tumour_Dice'].append(dc(pred_VS, gt_VS))

        if DEBBUGING:
            df_metric['tumour_ASSD'].append(10)
        else:
            if np.sum(pred_VS) > 0:
                df_metric['tumour_ASSD'].append(assd(pred_VS, gt_VS, voxelspacing=vxlspacing))
            else:
                df_metric['tumour_ASSD'].append(MAX_VALUE_ASSD)

        # except subprocess.CalledProcessError:
        #     # If no output found, give penalized scores.
        #     df_metric = {
        #             "scan_id": [f"{scan_id}"],
        #             'VS_intraDice': [0], 'VS_intraASSD': [374],
        #             'VS_extraDice': [0], 'VS_extraASSD': [374],
        #             'VS_Dice': [0], 'VS_ASSD': [374], 'boundary_ASSD': [374],
        #             'Cochlea_Dice': [0], 'Cochlea_ASSD': [374],
        #         }
        # print(df_metric)
    return pd.DataFrame.from_dict(df_metric).set_index('scan_id')   #.sort_values(by="")


def main():
    """Main function."""
    preds = glob.glob('%s/*.nii.gz'%(sys.argv[1]))
    golds = glob.glob('%s/*.nii.gz'%(sys.argv[2]))
    print(preds)
    print(golds)
    dir_name = os.path.split(golds[0])[0]
    results = score(dir_name, preds)

    # Get number of segmentations predicted by participant, number of
    # segmentation that could not be scored, and number of segmentations
    # that were scored.
    # cases_predicted = len(results.index)
    # flagged_cases = int(results.reset_index().scan_id.str.count(r"\*").sum())
    # cases_evaluated = cases_predicted - flagged_cases
    print(results)
    results.loc["mean"] = results.mean()
    results.loc["sd"] = results.std()
    results.loc["median"] = results.median()
    results.loc["25quantile"] = results.quantile(q=0.25)
    results.loc["75quantile"] = results.quantile(q=0.75)

    # CSV file of scores for all scans.
    results.to_csv("./CSV_files/%s_%s_%s_all_scores.csv"%(sys.argv[1].split('/')[-3],sys.argv[2].split('/')[-3],sys.argv[1].split('/')[-2]))


if __name__ == "__main__":
    main()
