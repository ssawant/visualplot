from visualplot.blocks.vectors import vector_comp
from visualplot.timeline import Timeline
from visualplot.visualization import Visualization


def vector_plot(X, Y, U, V, t, skip=5, *, t_axis=0, units='', fps=10,
                pcolor_kw={}, quiver_kw={}):
    """
    produces an animation of vector fields
    This takes 2D vector field, and plots the magnitude as a pcolomesh, and the
    normalized direction as a quiver plot. It then animates it.
    This is a convience function. It wraps around the Pcolormesh and Quiver
    blocks. It will be more restrictive than using the blocks themselves. If
    you need more control, or the ability to pass data in as a list, then use
    the individual blocks.

    :param X : 2D numpy array
        The x location of the vectors to be animated
    :param Y : 2D numpy array
        The x location of the vectors to be animated
    :param U : 3D numpy array
        The x components of the vectors to be animated.
    :param V : 3D numpy array
        The y components of the vectors to be animated.
    :param t : 1D numpy array
        The time values
    :param skip : int, optional
        The amount of values to skip over when making the quiver plot.
        Higher skip means fewer arrows. For best results, the skip should
        divide the length of the data-1. Defaults to 5.
    :param t_axis : int, optional
        The axis of the U, V array's the represent time. Defaults to 0. Note
        this is different from the defaults that blocks choose. This default
        is chosen to be consistent with 3D-meshgrids (meshgrid(x, y, t)).
    :param fps : int, optional
        The frames per second to display the animation at.
    :param units : str, optional
        The units to display on the timeline.
    :param pcolor_kw : dict, optional
        A dictionary of parameters to pass to pcolormesh.
    :param quiver_kw : dict, optional
        A dictionary of parameters to pass to quiver.

    :returns
    Visualplot.Visualization
        The complete animation
    list of Visualplot.blocks.Block
        A list of all the blocks used in the animation. The list
        contains a Pcolorblock, and a Quiver block in that order.
    Visualplot.Timeline
        The timeline that was generated for the animation.
    """
    # plot the magnitude of the vectors as a pcolormesh
    blocks = vector_comp(X, Y, U, V, skip, t_axis=t_axis,
                         pcolor_kw=pcolor_kw, quiver_kw=quiver_kw)

    # create the animation
    timeline = Timeline(t, units=units, fps=fps)
    anim = Visualization(blocks, timeline)

    return anim, blocks, timeline
