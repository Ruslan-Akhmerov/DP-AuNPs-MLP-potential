from ase.cluster.octahedron import Octahedron
from ase.io import write
from ase.visualize import view

atoms = Octahedron('Au', length=11)
print(atoms)
view(atoms)
write('Truncated octahedron.car', atoms)