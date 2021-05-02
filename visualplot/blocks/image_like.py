import matplotlib.pyplot as plt
import numpy as np

from visualplot.blocks.base import Block


class Pcolormesh(Block):
    """ Animates a pcolormesh """

    def __init__(self, *args, ax=None, t_axis=0, **kwargs):
        """
        :param X : 1D or 2D np.ndarray, optional
        :param Y : 1D or 2D np.ndarray, optional
        :param C : list of 2D np.ndarray or a 3D np.ndarray
        :param ax : matplotlib.axes.Axes, optional
            The matplotlib axes to attach the block to.
            Defaults to matplotlib.pyplot.gca()
        :param t_axis : int, optional
            The axis of the array that represents time. Defaults to 0.
            No effect if C is a list.

        All other keyword arguments get passed to ``axis.pcolormesh``
        see :meth:`matplotlib.axes.Axes.pcolormesh` for details.
        """
        if len(args) == 1:
            self.C = args[0]
            self._arg_len = 1
        elif len(args) == 3:
            self.X, self.Y, self.C = args
            self._arg_len = 3
            if len(self.X.shape) not in [1, 2]:
                raise TypeError('X must be a 1D or 2D arrays')
            if len(self.Y.shape) not in [1, 2]:
                raise TypeError('Y must be a 1D or 2D arrays')
        else:
            raise TypeError('Illegal arguments to pcolormesh; see help(pcolormesh)')

        super().__init__(ax, t_axis)

        self._is_list = isinstance(self.C, list)
        self.C = np.asanyarray(self.C)

        slice_c = self._make_slice(0, 3)

        # replicate matplotlib logic for setting default shading value because
        # matplotlib resets the _shading member variable of the QuadMesh to "flat" after
        # interpolating X and Y to corner positions
        self.shading = kwargs.get('shading', plt.rcParams.get('pcolor.shading', 'flat'))
        Nx = self.X.shape[-1]
        Ny = self.Y.shape[0]
        if self.shading == 'auto':
            if (Ny, Nx) == self.C[slice_c].shape:
                self.shading = 'nearest'
            else:
                self.shading = 'flat'
        if self.shading == "flat" and ((Ny - 1, Nx - 1) == self.C[slice_c].shape):
            # Need to slice without the workaround in _update()
            self.shading = "flat_corner_grid"

        if self._arg_len == 1:
            self.quad = self.ax.pcolormesh(self.C[slice_c], **kwargs)
        elif self._arg_len == 3:
            self.quad = self.ax.pcolormesh(self.X, self.Y, self.C[slice_c], **kwargs)

    def _update(self, i):
        if self.shading == "flat":
            slice_c = self._make_pcolormesh_flat_slice(i, 3)
            self.quad.set_array(self.C[slice_c].ravel())
        else:
            slice_c = self._make_slice(i, 3)
            self.quad.set_array(self.C[slice_c])
        return self.quad

    def __len__(self):
        if self._is_list:
            return self.C.shape[0]
        return self.C.shape[self.t_axis]

    def _make_pcolormesh_flat_slice(self, i, dim):
        if self._is_list:
            return i
        slice_c = [slice(-1)] * 3  # weird thing to make animation work
        slice_c[self.t_axis] = i
        return tuple(slice_c)
