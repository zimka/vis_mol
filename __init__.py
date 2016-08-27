import mol2_pack as mp
from vis_mol2_pack.points_plot import vis_mol_wrap
from vis_mol2_pack.surface_plot import build_surface
from vis_mol2_pack.wrap import show_mol_surf
from vispy import app, scene
__version__ = '0.0.1'
"""
example:
    f2 = lambda x,y,z:-gyroid(x,y,z, C=-1.3)
    cube2 = cube_lattice(N, f2)

    mol = mp.file_to_molwrap(film)
    l_par = 140
    vmp.show_mol_surf(surf_datas=(cube,cube2), mol_obj=mol, l_par=l_par, reduced_mol=True)
"""
