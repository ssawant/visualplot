import numpy as np

from visualplot.blocks.base import Block
from visualplot.blocks.image_like import Pcolormesh


class Quiver(Block):
    """
    A block or animated quiver plots
    """

    def __init__(self, X, Y, U, V, ax=None, t_axis=0, **kwargs):
        """
        :param X: 1D or 2D numpy array
            The x positions of the arrows. Cannot be animated.
        :param Y: 1D or 2D numpy array
            The y positions of the arrows. Cannot be animated.
        :param U: 2D or 3D numpy array
            The U displacement of the arrows. 1 dimension
        higher than the X, Y arrays.
        :param V: 2D or 3D numpy array
            The V displacement of the arrows. 1 dimension
        higher than the X, Y arrays.
        :param ax: matplotlib.axes.Axes, optional
            The matplotlib axes to the block to.
        Defaults to matplotlib.pyplot.gca()
        :param t_axis: int, optional
            The axis of the array that represents time. Defaults to 0.
        No effect if U, V are lists.
        :param kwargs:
        """
        self.X = X
        self.Y = Y
        self.U = np.asanyarray(U)
        self.V = np.asanyarray(V)
        if X.shape != Y.shape:
            raise ValueError("X, Y must have the same shape")
        if self.U.shape != self.V.shape:
            raise ValueError("U, V must have the same shape")

        super().__init__(ax, t_axis)

        self._dim = len(self.U.shape)
        self._is_list = isinstance(U, list)

        slice_s = self._make_slice(0, self._dim)
        self.Q = self.ax.quiver(self.X, self.Y, self.U[slice_s], self.V[slice_s], **kwargs)

    def _update(self, i):
        slice_s = self._make_slice(i, self._dim)
        self.Q.set_UVC(self.U[slice_s], self.V[slice_s])
        return self.Q

    def __len__(self):
        if self._is_list:
            return self.U.shape[0]
        return self.U.shape[self.t_axis]


def vector_comp(X, Y, U, V, skip=5, *, t_axis=0, pcolor_kw={}, quiver_kw={}):
    """
    produces an animation of vector fields
    This takes 2D vector field, and plots the magnitude as a pcolomesh, and the
    normalized direction as a quiver plot. It then animates it.
    This is a convince function. It wraps around the Pcolormesh and Quiver
    blocks. It will be more restrictive than using the blocks themselves. If
    you need more control, or the ability to pass data in as a list, then use
    the individual blocks.

    :param X: 2D numpy array
        The x location of the vectors to be animated
    :param Y: 2D numpy array
        The y location of the vectors to be animated
    :param U: 3D numpy array
        The x components of the vectors to be animated.
    :param V: 3D numpy array
        The y components of the vectors to be animated.
    :param skip: int, optional
        The amount of values to skip over when making the quiver plot.
        Higher skip means fewer arrows. For best results, the skip should
        divide the length of the data-1. Defaults to 5.
    :param t_axis: int, optional
        The axis of the U, V array's the represent time. Defaults to 0. Note
        this is different from the defaults that blocks choose. This default
        is chosen to be consistent with 3D-meshgrids (meshgrid(x, y, t)).
    :param pcolor_kw: dict, optional
        A dictionary of parameters to pass to pcolormesh.
    :param quiver_kw:
        A dictionary of parameters to pass to quiver.

    :return: list of Animatplot.blocks.Block
        A list of all the blocks used in the animation. The list
        contains a Pcolorblock, and a Quiver block in that order.
    """
    # plot the magnitude of the vectors as a pcolormesh
    magnitude = np.sqrt(U ** 2 + V ** 2)
    pcolor_block = Pcolormesh(X, Y, magnitude, t_axis=t_axis, **pcolor_kw)

    # use a subset of the data to plot the arrows as a quiver plot.
    xy_slice = tuple([slice(None, None, skip)] * len(X.shape))

    uv_slice = [slice(None, None, skip)] * len(U.shape)
    uv_slice[t_axis] = slice(None)
    uv_slice = tuple(uv_slice)

    quiver_block = Quiver(X[xy_slice], Y[xy_slice],
                          U[uv_slice] / magnitude[uv_slice],
                          V[uv_slice] / magnitude[uv_slice],
                          t_axis=t_axis, **quiver_kw)

    return [pcolor_block, quiver_block]
