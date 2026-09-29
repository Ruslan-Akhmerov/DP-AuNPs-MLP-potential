from ase.cluster.icosahedron import Icosahedron
from ase.io import write
from ase.visualize import view

atoms = Icosahedron('Au', noshells=3)

# Визуализируем икосаэдр
view(atoms)

write('Icosahedron.car', atoms)
