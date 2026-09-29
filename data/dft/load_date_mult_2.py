import dpdata
import numpy as np
import os

# List of files to process
vasprun_files = ['lq_90.xml', '113_bcc_vac.xml', '113_bcc_adatoms.xml', '135_fcc_vac.xml', '135_fcc_adatoms.xml', 'Decahedron_vac.xml', 
                 'Icosahedron_vac.xml', 'Icosahedron_adatoms.xml', 'Decahedron_adatoms.xml', 'supercell_adatoms_97.xml', 
                 'supercell_adatoms_97_2.xml', 'supercell_adatoms_121.xml', 'supercell_adatoms_121_2.xml', 'supercell_vac_95.xml', 
                 'supercell_vac_95_1.xml', 'supercell_vac_119.xml', 'supercell_vac_119_2.xml',
                 'surface_adatoms_Au65_done.xml','surface_adatoms_Au97_done.xml','surface_adatoms_Au129_2_done.xml','surface_adatoms_Au129_done.xml','surface_adatoms_Au193_done.xml',
                 'surface_steps_Au56_done.xml','surface_steps_Au88_done.xml','surface_steps_Au116_done.xml', 'surface_steps_Au180_done.xml',  'surface_steps_Au120_done.xml',
                 'surface_vac_Au63_done.xml', 'surface_vac_Au95_done.xml','surface_vac_Au127_2_done.xml','surface_vac_Au127_done.xml', 'surface_vac_Au191_done.xml']

total_frames_all = 0
total_training_frames = 0
total_validation_frames = 0
# Create directories for training and validation data
if not os.path.exists('training_data'):
    os.makedirs('training_data')
if not os.path.exists('validation_data'):
    os.makedirs('validation_data')

for file in vasprun_files:
    total_frames_all += total_frames_all
    # Load data from the current file
    data = dpdata.LabeledSystem(file, fmt='vasp/xml')
    print(f'# file {file} contains {len(data)} frames')

    # Compute the number of frames for the validation set (20%)
    total_frames = len(data)
    validation_size = int(total_frames * 0.20)

    # Randomly select indices for the validation set
    index_validation = np.random.choice(total_frames, size=validation_size, replace=False)

    # All remaining indices are used for training
    index_training = list(set(range(total_frames)) - set(index_validation))
    data_training = data.sub_system(index_training)
    data_validation = data.sub_system(index_validation)

    # Save training data for the current file
    training_dir = os.path.join('training_data', os.path.splitext(file)[0])
    if not os.path.exists(training_dir):
        os.makedirs(training_dir)
    data_training.to_deepmd_npy(training_dir)

    # Save validation data for the current file
    validation_dir = os.path.join('validation_data', os.path.splitext(file)[0])
    if not os.path.exists(validation_dir):
        os.makedirs(validation_dir)
    data_validation.to_deepmd_npy(validation_dir)
    
    total_training_frames += len(data_training)
    total_validation_frames += len(data_validation)

    print(f'# training data from file {file} contains {len(data_training)} frames')
    print(f'# validation data from file {file} contains {len(data_validation)} frames')



print(f"\n======= SUMMARY =======")
print(f"Total frames across all files: {total_frames_all}")
print(f"Frames in the training set: {total_training_frames}")
print(f"Frames in the validation set: {total_validation_frames}")