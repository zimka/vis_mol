import numpy as np
import sys
from vispy import app, visuals, scene
import mol2_pack as mp


def vis_mol_wrap(mol, view=None, scale=None, reduced_mol=False):
    """
    visualises MolWrap points
    :param mol:
    :return:
    """
    if view is None:
        canvas = scene.SceneCanvas(keys='interactive', title='plot3d', show=True)
        view = canvas.central_widget.add_view()
        view.camera = 'turntable'

    print(np.max(mol.pos), np.min(mol.pos))
    posx, posy, posz = mol.pos
    postypes = mol.atoms
    type_colors = {"C": (0.4, 0.4, 0.4, 0.9),
                   "O": (0.9, 0.3, 0.3, 0.6),
                   "N": (0.1, 0.9, 0.2, 0.6),
                   "H": (0.9, 0.9, 0.9, 0.9),
                   "Na": (0.3, 0.9, 0.8, 0.6),
                   "S": (0.8, 0.9, 0.2, 0.6)}
    type_radi = {"C": 10,
                 "O": 12,
                 "N": 12,
                 "H": 6,
                 "S": 20,
                 "Na": 16}

    Plot3D = scene.visuals.create_visual_node(visuals.LinePlotVisual)

    pos = np.c_[posx, posy, posz]

    for t in type_colors:
        if reduced_mol and t=='H':
            continue
        if type_radi is not None:
            market_size = type_radi[t]
        else:
            market_size = 10
        ind = postypes == t
        pos_temp = pos[ind, :]
        if pos_temp.shape[0] == 0:
            continue
        Plot3D(pos_temp, width=0.0, color=(0, 0, 0, 0), marker_size=market_size,
               edge_color='w', symbol='o', face_color=type_colors[t],
               parent=view.scene)
    bonds = mol.link#.transpose()
    if not reduced_mol:
        Plot3D(pos, width=4.0, color=(0.5, 0.5, 0.5, .9), marker_size=0,
               edge_color='w', symbol='o', face_color=(0, 0, 0, 0),
               connect=bonds, parent=view.scene)

