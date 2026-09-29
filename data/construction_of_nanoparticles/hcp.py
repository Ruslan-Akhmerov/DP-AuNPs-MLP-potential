import ase
from ase.cluster.cubic import FaceCenteredCubic
from ase.visualize import view
from ase.io import write

surfaces = [(1, 0, 0), (1, 1, 1), (1, -1, 1)]
layers = [5, 4, 5] # 6 5 6
lc = 4.17
atoms = FaceCenteredCubic('Au', surfaces, layers, latticeconstant=lc)

print('#atoms = {}'.format(len(atoms)))
view(atoms)

write('hcp.car', atoms)