from vis_mol2_pack import mp, vis_mol_wrap, build_surface
import numpy as np
from vispy import scene, app
from vispy import visuals, scene
from vispy.gloo.util import _screenshot
from vispy.io import imsave


class ColorIter():
    def __init__(self, n=2):
        self.n = n

    def __next__(self):
        if self.n == 0:
            return
        self.n -= 1

        if self.n == 0:
            return (0.9, 0.1, 0.1, 0.8)
        if self.n == 1:
            return (0.1, 0.9, 0.1, 0.8)

        return (np.random.rand()/2+0.1,
                np.random.rand()/2+0.1,
                np.random.rand()/2+0.5
                , 0.8)

class myXYZAxisVisual(visuals.LineVisual):
    """
    Simple 3D axis for indicating coordinate system orientation. Axes are
    x=red, y=green, z=blue.
    """
    def __init__(self, length,**kwargs):
        verts = np.array([[0, 0, 0],
                          [length, 0, 0],
                          [0, 0, 0],
                          [0, length, 0],
                          [0, 0, 0],
                          [0, 0, length]])
        color = np.array([[1, 0, 0, 1],
                          [1, 0, 0, 1],
                          [0, 1, 0, 1],
                          [0, 1, 0, 1],
                          [0, 0, 1, 1],
                          [0, 0, 1, 1]])
        visuals.LineVisual.__init__(self, pos=verts, color=color, connect='segments',
                            method='gl', **kwargs)

myXYZAxis = scene.visuals.create_visual_node(myXYZAxisVisual)


def show_mol_surf(mol_obj=None, surf_datas=None, l_par=None, reduced_mol=False, **kwargs):
    canvas = scene.SceneCanvas(keys='interactive', bgcolor=(1,1,1,1))
    view = canvas.central_widget.add_view()

    num = None
    if surf_datas is not None:
        if isinstance(surf_datas,tuple):
            colors = ColorIter(len(surf_datas))
            for data in surf_datas:
                if num is not None and len(data)!=num:
                    raise TypeError("different dimensions of surfaces")
                num = len(data)
                build_surface(data=data, view=view, color=next(colors))
        else:
            build_surface(data=surf_datas, view=view, color=next(ColorIter(1)))
            num = len(surf_datas)

    if mol_obj is not None:
        mol = mol_obj.copy()
        if surf_datas is not None:
            if l_par is not None:
                mol.pos /= l_par
                mol.pos *= num
        vis_mol_wrap(mol, view=view, reduced_mol=reduced_mol)

    if num is None:
        num = 50
    sr = kwargs.get('setrange', num)
    cam = scene.TurntableCamera(elevation=30, azimuth=30)
    if kwargs.get('show_axis', True):
        axis = myXYZAxis(length=num+10, parent=view.scene)
    cam.set_range((-sr, sr), (-sr, sr), (-sr, sr))
    view.camera = cam
    cube_size = kwargs.get ('cube_size', 0.)
    scene.visuals.Cube(size=cube_size*num/2,
                       color=(0.9, 0.9, 0.3, 0.4),
                       edge_color="black",
                       parent=view.scene)
    canvas.show()


    if kwargs.get('quit', False ):
            app.process_events()
    else:
        app.run()

    if kwargs.get('screenshot', False):
        name = kwargs.get("screenname", 'screenshot.png')
        im = _screenshot((0, 0, canvas.size[0], canvas.size[1]))
        imsave(name, im)


