from vispy import app, scene
import numpy as np
from mol2_pack import file_to_molwrap
from vispy.visuals.transforms import STTransform


def build_surface(data, view, color=(0.8, 0.8, 0.8, 0.8)):
    N = len(data)

    surface = scene.visuals.Isosurface(data, level=0,
                                   color=color, shading='smooth',
                                   parent=view.scene)
    surface.transform = scene.transforms.STTransform(translate=(-N/2, -N/2, -N/2))
