import os
import xml.etree.ElementTree as ET
import dpdata
import numpy as np
import shutil
import random

# Function to read POSCAR
def read_poscar(poscar_file):
    with open(poscar_file, "r") as file:
        lines = file.readlines()

    # Cell vectors
    cell_vectors = [list(map(float, lines[2].split())),
                    list(map(float, lines[3].split())),
                    list(map(float, lines[4].split()))]

    # Atom types
    atom_types = lines[5].split()
    atom_counts = list(map(int, lines[6].split()))

    # Atom coordinates
    atom_coords = []
    for line in lines[8:8 + sum(atom_counts)]:
        atom_coords.append(list(map(float, line.split()[:3])))

    return cell_vectors, atom_types, atom_counts, atom_coords

# Function to read OUTCAR
def read_outcar(outcar_file, num_atoms):
    with open(outcar_file, "r") as file:
        lines = file.readlines()

    # Find the line with the virial
    virial = None
    for i, line in enumerate(lines):
        if "FORCE on cell =-STRESS in cart. coord.  units (eV):" in line:
            # The virial is a few lines after the header
            virial_line = lines[i + 13].strip().split()
            virial = list(map(float, virial_line[1:7]))  # Take only XX, YY, ZZ, XY, YZ, ZX
            break

    # Find the lines with forces
    forces = []
    for i, line in enumerate(lines):
        if "POSITION                                       TOTAL-FORCE (eV/Angst)" in line:
            # Forces are a few lines after the header
            for j in range(i + 2, i + 2 + num_atoms):  # Read lines for each atom
                force_line = lines[j].strip().split()
                if len(force_line) >= 6:
                    # Extract force components
                    fx, fy, fz = map(float, force_line[3:6])
                    # Append forces to the list
                    forces.append([fx, fy, fz])
            break

    return virial, forces

# Function to convert 6 stress components to 9 components
def convert_stress_to_9(stress_6):
    """
    Convert the stress tensor from 6 components to 9 components.
    stress_6: [xx, yy, zz, xy, yz, zx]
    stress_9: [xx, xy, xz, yx, yy, yz, zx, zy, zz]
    """
    xx, yy, zz, xy, yz, zx = stress_6
    stress_9 = [xx, xy, zx,  # First row
                xy, yy, yz,  # Second row
                zx, yz, zz]  # Third row
    return stress_9

# Function to create a dpdata system from the data
def create_dpdata_system(cell_vectors, atom_types, atom_counts, atom_coords, vasp_energy, forces, virial):
    system = dpdata.System()

    # Set data
    system.data['atom_names'] = atom_types
    system.data['atom_numbs'] = atom_counts
    system.data['atom_types'] = np.array([i for i, count in enumerate(atom_counts) for _ in range(count)], dtype=int)
    system.data['coords'] = np.array([atom_coords], dtype=float)
    system.data['cells'] = np.array([cell_vectors], dtype=float)
    system.data['energies'] = np.array([vasp_energy], dtype=float)
    system.data['forces'] = np.array([forces], dtype=float)

    # Convert stress to 9 components
    stress_9 = convert_stress_to_9(virial)
    system.data['virials'] = np.array([stress_9], dtype=float)

    return system

# Function to process all files in a folder
def process_all_files(folder_path, output_dir):
    # Get the list of all files in the folder
    files = os.listdir(folder_path)

    # Find all .xml files
    xml_files = [f for f in files if f.endswith('.xml')]

    for xml_file in xml_files:
        # File name without .xml extension and (VASP) suffix
        base_name = xml_file.replace(" (VASP).xml", "")

        # Look for the corresponding files
        poscar_file = f"{base_name} (VASP)"  # POSCAR
        outcar_file = f"{base_name} (OUTCAR)"  # OUTCAR

        # Check if the files exist
        if poscar_file in files and outcar_file in files:
            # Full paths to the files
            poscar_path = os.path.join(folder_path, poscar_file)
            outcar_path = os.path.join(folder_path, outcar_file)
            xml_path = os.path.join(folder_path, xml_file)

            # Read data
            cell_vectors, atom_types, atom_counts, atom_coords = read_poscar(poscar_path)
            num_atoms = sum(atom_counts)  # Total number of atoms
            virial, forces = read_outcar(outcar_path, num_atoms)

            # Read energy from XML
            tree = ET.parse(xml_path)
            root = tree.getroot()
            vasp_energy = float(root.find(".//PropertyValue[@property='VASP energy']").text.strip())

            # Create dpdata system
            system = create_dpdata_system(cell_vectors, atom_types, atom_counts, atom_coords, vasp_energy, forces, virial)

            # Create a separate folder for each structure
            structure_output_dir = os.path.join(output_dir, base_name)
            os.makedirs(structure_output_dir, exist_ok=True)

            # Save the system in DeepMD format
            system.to_deepmd_npy(structure_output_dir)
            print(f"Data saved to {structure_output_dir}")
        else:
            print(f"No matching file found for {xml_file}")

# Function to split data into training and validation sets
def split_data(input_dirs, train_ratio=0.8):
    # Shuffle the list of folders
    random.shuffle(input_dirs)

    # Compute the number of folders for the training set
    train_size = int(len(input_dirs) * train_ratio)

    # Split folders into training and validation sets
    train_dirs = input_dirs[:train_size]
    val_dirs = input_dirs[train_size:]

    return train_dirs, val_dirs

# Function to merge all data folders
def merge_deepmd_folders(input_dirs, output_dir, folder_name):
    # Create a LabeledSystem object to merge the data
    system = dpdata.LabeledSystem()

    # Iterate over all data folders
    for input_dir in input_dirs:
        if os.path.isdir(input_dir):  # Check that it is a folder
            # Load the system from the folder
            current_system = dpdata.LabeledSystem(input_dir, fmt="deepmd/npy")
            # Append the data to the common system
            system.append(current_system)
            print(f"Added system from folder: {input_dir}")
        else:
            print(f"Skipped (not a folder): {input_dir}")

    # Create a folder with the given name
    final_output_dir = os.path.join(output_dir, folder_name)
    os.makedirs(final_output_dir, exist_ok=True)

    # Save the merged data to the output folder
    system.to_deepmd_npy(final_output_dir)
    print(f"All data merged and saved to {final_output_dir}")

# Main function
def main():
    # Folder with the source files
    folder_path = "path/to/def_omega"  # <-- replace with your actual path

    # Folder to save individual structures
    temp_output_dir = "path/to/temp_data"
    os.makedirs(temp_output_dir, exist_ok=True)

    # Folder to save the training set
    train_output_dir = "path/to/training_data"
    os.makedirs(train_output_dir, exist_ok=True)

    # Folder to save the validation set
    val_output_dir = "path/to/validation_data"
    os.makedirs(val_output_dir, exist_ok=True)

    # Process all files and save to individual folders
    process_all_files(folder_path, temp_output_dir)

    # Get the list of all data folders
    input_dirs = [os.path.join(temp_output_dir, d) for d in os.listdir(temp_output_dir) if os.path.isdir(os.path.join(temp_output_dir, d))]

    # Split data into training and validation sets
    train_dirs, val_dirs = split_data(input_dirs)

    # Merge the training set
    merge_deepmd_folders(train_dirs, train_output_dir, "def_omega")

    # Merge the validation set
    merge_deepmd_folders(val_dirs, val_output_dir, "def_omega")

    # Remove temporary folders (optional)
    for input_dir in input_dirs:
        shutil.rmtree(input_dir)  # Remove the folder and all its contents
    shutil.rmtree(temp_output_dir)  # Remove the temporary folder
    print("Temporary folders removed.")

# Run the main function
if __name__ == "__main__":
    main()
