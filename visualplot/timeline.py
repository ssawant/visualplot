import numpy as np

from utils import demeshgrid


class Timeline:
    """:return Object to control and content all of the time"""

    def __init__(self, t, units='', fps=10, log=False):
        """
        :param t: array_like
            Gets converted into a numpy array representing the time at each frame of the animation.
        :param units:  str, optional
            The units in which the time is measured.
        :param fps: float, optional
            Indicates the number of frames per second of the animation. Defaults to 10.
        :param log: bool, optional
            Displays the time scale logarithmically (base 10). Defaults to False.
        """
        t = np.asanyarray(t)
        if len(t.shape) > 1:
            self.t = demeshgrid(t)
            if self.t is None:
                raise ValueError("Unable to interpret time values. Please try passing a 1D array instead.")
        else:
            self.t = t

        self.fps = fps
        self.units = units
        self.log = log

        if self.log:
            self.t = np.log10(self.t)
        self.index = 0

        self._len = len(self.t)

    def __getitem__(self, item):
        return self.t.__getitem__(item)

    def __repr__(self):
        time = repr(self.t)
        units = repr(self.units)
        return f"visualplot.visualization.Timeline(t={time}, units={units}, fps={self.fps}"

    def __len__(self):
        return self.__len__()

    def _update(self):
        """ increment the current timeline"""
        self.index = (self.index + 1) % self._len
