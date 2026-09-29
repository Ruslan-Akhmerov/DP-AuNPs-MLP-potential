from ase.cluster import wulff_construction
from ase.cluster.cubic import BodyCenteredCubic
from ase.visualize import view
from ase.io import read, write

# ===== BCC particle with 135 atoms =====
# For BCC we use the same directions, but the structure is 'bcc'
surfaces = [(1, 0, 0), (1, 1, 0), (1, 1, 1)]
energies = [1.0, 1.0, 1.0]  # relative surface energies
target_atoms = 1000  # desired number of atoms

# Create a particle with a BCC structure
atoms = wulff_construction('Au', surfaces, energies,
                           target_atoms, 'bcc',  
                           rounding='closest', 
                           latticeconstant=3.315) 

# Visualize
view(atoms)

# Save to .car
write('Au_bcc_113atoms.car', atoms)

# ===== ADD A 20x20x20 CELL =====
atoms.set_cell([20.0, 20.0, 20.0])  # 20 Å cell
atoms.set_pbc(True)                  # Enable PBC
atoms.center()                       # Center the particle

# Save to POSCAR
write('Au_bcc_113atoms_POSCAR', atoms, format='vasp', vasp5=True, direct=False)
write('Au_bccNPs_atoms.lmp', atoms, format='lammps-data', atom_style='atomic')
print(f"Atoms: {len(atoms)}")
