from tqdm import tqdm
from pathlib import Path
from preprocess import PreprocessFMRI


def main():
    ayam_nifti_files_path = r'C:\Users\YaelAlon\Desktop\Yael\TAU\Master\Data'
    assert ayam_nifti_files_path is not None
    preprocess = PreprocessFMRI(ayam_nifti_files_path,atlases=['harvard_oxford_cort','harvard_oxford_sub'])
    use_confound_regressors = False
    count = 0
    for file in tqdm(Path(preprocess.main_path).rglob('*preproc_bold.nii.gz')):
        if 'fcmri' not in file.name: #rest
            continue
        f = str(file)
        subject = f[f.find('sub'):f.find('sub') + 8]
        task = f[f.find('task')+5:f.find('task') + 11]
        session = f[f.find('ses'):f.find('ses') + 5].replace('-','_')
        if use_confound_regressors:
            confounds = file.parent.joinpath('{}_{}_task-{}_desc-confounds_regressors.tsv'.format(subject,session,task))
            confounds = confounds if confounds.exists() else None
        else:
            confounds = None
        count += 1
        g_norm_path = preprocess.main_path.joinpath('MNI_to_TRs', subject, task, session, 'global_normalize')
        pv_norm_path = preprocess.main_path.joinpath('MNI_to_TRs', subject, task, session, 'per_voxel_normalize')
        fc_path = preprocess.main_path.joinpath('functional_connectivity_{}'.format(preprocess.fc_atlas_name), subject, task,session, 'per_parcel_normalize')
        g_norm_path.mkdir(exist_ok=True, parents=True)
        pv_norm_path.mkdir(exist_ok=True, parents=True)
        fc_path.mkdir(exist_ok=True, parents=True)
        print('start working on subject %s, session %s' %(subject,session))
        try:
            preprocess.run_preprocess_on_scan(file,g_norm_path=g_norm_path,pv_norm_path=pv_norm_path,fc_path=fc_path,confounds_path=confounds)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()