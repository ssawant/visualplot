from visualplot.blocks.base import Block


class Update(Block):
    """
    For providing a custom update method
    This block allows you to write a custom update method to provide
    functionality not available with other blocks.
    """

    def __int__(self, func, length, fargs=[], ax=None):
        """
        :param func: callable
            This function will be called once for each frame of the animation.
            The first argument to this function must be an integer
            representing the frame number. It should return a matplotlib
            artist.
        :param length: int
            The number of frames to display.
        :param fargs: list, optional
            A list of arguments to pass into func.
        :param ax: matplotlib.axes.Axes, optional
            The matplotlib axes to which the block is attached.
            Defaults to matplotlib.pyplot.gca()
        :return:
        """
        self.func = func
        self.length = length
        self.fargs = fargs
        super().__init__(ax)

        func(0, *fargs)

    def _update(self, i):
        self.func(i, *self.fargs)

    def __len__(self):
        return self.length


class Nuke(Update):
    """
    For when the other blocks just won't do:
    This block will clear the axes and redraw using a provided
    function on every frame.
    This block can be used with other blocks so long as other
    blocks are attached to a different axes.
    Only use this block as a last resort. Using the block
    is like nuking an ant hill. Hence the name.
    """

    def _update(self, i):
        self.ax.clear()
        self.func(i, *self.fargs)
