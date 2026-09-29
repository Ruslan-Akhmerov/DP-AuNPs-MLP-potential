from ase.cluster import wulff_construction
from ase.cluster.cubic import FaceCenteredCubic
from ase.visualize import view
from ase.io import read, write

# Create a particle with an exact number of atoms
surfaces = [(1, 0, 0), (1, 1, 0), (1, 1, 1)]
energies = [1.0, 1.0, 1.0]  # relative surface energies
target_atoms = 1000  # desired number of atoms

atoms = wulff_construction('Au', surfaces, energies,
                           target_atoms, 'fcc',
                           rounding='closest', 
                           latticeconstant=4.17)
view(atoms)
write('Au_fcc_135atoms.car', atoms)

# ===== ADD A CELL =====
atoms.set_cell([50.0, 50.0, 50.0])  # 50 Å cell
atoms.set_pbc(True)                  # Enable PBC
atoms.center()                       # Center the particle

# Now save to POSCAR
write('Au_fcc_135atoms_POSCAR', atoms, format='vasp', vasp5=True, direct=False)
write('Au_fccNPs_atoms.lmp', atoms, format='lammps-data', atom_style='atomic')
print(f"Atoms: {len(atoms)}")


"""
from ase.cluster.cubic import FaceCenteredCubic
from ase.visualize import view

# Create a 113-atom particle
surfaces = [(1,0,0), (1,1,0), (1,1,1)]
layers = [6, 9, 5]
atoms = FaceCenteredCubic('Au', surfaces, layers, latticeconstant=4.08)

print(f"Number of atoms: {len(atoms)}")  # Should be 113
print(atoms)
view(atoms)
"""



"""
from ase.cluster.cubic import FaceCenteredCubic
from ase.visualize import view

# Создаём частицу 113 атомов
surfaces = [(1,0,0), (1,1,0), (1,1,1)]
layers = [6, 9, 5]
atoms = FaceCenteredCubic('Au', surfaces, layers, latticeconstant=4.08)

print(f"Количество атомов: {len(atoms)}")  # Должно быть 113
print(atoms)
view(atoms)
"""
