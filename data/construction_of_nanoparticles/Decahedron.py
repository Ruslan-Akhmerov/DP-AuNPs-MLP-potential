from ase.cluster.decahedron import Decahedron
from ase.io import write
from ase.visualize import view

atoms = Decahedron('Au',
                   p=3,
                   q=1, 
                   r=0) 

# Visualize the decahedron
view(atoms)


write('Decahedron.car', atoms)
