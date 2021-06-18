import pandas as pd
import os
import sys

def stiching_denoised_patches(input_path, output_fn = None):
    cts_files = sorted([x for x in os.listdir(input_path) if 'Counts.txt' in x])
    denoised_fns = sorted([x for x in os.listdir(input_path) if 'denoised' in x])
    assert(len(cts_files) == len(denoised_fns)), 'Slideseq patch data not properly denoised'

    denoised_mtx = pd.DataFrame()
    for cts_fn in cts_files:
        abs_cts_fn = os.path.join(input_path,cts_fn)
        core_name = cts_fn.replace('_Counts.txt','')
        metadata_fn = abs_cts_fn.replace('Counts.txt','Spot_metadata.csv')
        denoised_fn = abs_cts_fn.replace('Counts.txt', 'denoised/Denoised_matrix.txt')
        metadata = pd.read_csv(metadata_fn, index_col=0)
        denoised_cts = pd.read_csv(denoised_fn, index_col=0, sep='\t')
        core_idx = metadata[metadata.patch_core == core_name].index
        denoised_mtx = denoised_mtx.append(denoised_cts.loc[core_idx])
    
    if output_fn is None:
        output_fn = input_path.replace('/patches','/denoised_cts.h5df')

    denoised_mtx.to_hdf(output_fn, key='denoised')

if __name__ == '__main__':
    input_path = sys.argv[1]
    try:
        output_fn = sys.argv[2]
    except IndexError:
        output_fn = None
    stiching_denoised_patches(input_path, output_fn)

