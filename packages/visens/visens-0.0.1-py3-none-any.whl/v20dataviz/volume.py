import numpy as np
from .load import load


def volume(filename, colormap="viridis", nbins=256):
    """
    Make a 3D volume rendering using ipyvolume
    """

    import ipyvolume as ipv

    data = load(filename, ids=True, tofs=True)

    nx, ny = np.shape(data.x)
    t = np.linspace(0.0, 7.2e4, nbins + 1)
    z, xe, ye = np.histogram2d(data.ids, data.tofs/1.0e3,
                               bins=[np.arange(nx * ny + 1), t])
    z = np.transpose(z.reshape(nx, ny, nbins), axes=[2, 1, 0])
    ipv.quickvolshow(z,
        extent=[[data.x[0, 0]*100.0, data.x[0, -1]*100.0],
                [data.y[0, 0]*100.0, data.y[-1, 0]*100.0],
                [t[0], t[-1]]])
    ipv.pylab.xlabel("x [cm]")
    ipv.pylab.ylabel("y [cm]")
    ipv.pylab.zlabel("Tof [us]")
    ipv.show()

    return
