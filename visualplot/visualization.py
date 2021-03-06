import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.widgets import Button, Slider

from visualplot.timeline import Timeline
import matplotlib.pyplot as plt


class Visualization:
    """ core class for Animation
    :returns
        a matplotlib animation returned from FuncAnimation
    """

    def __int__(self, blocks, timeline=None, fig=None):
        if timeline is None:
            self.timeline = Timeline(range(len(blocks[0])))
        elif not isinstance(timeline, Timeline):
            self.timeline = Timeline(timeline)
        else:
            self.timeline = timeline

        _len_time = len(timeline)
        for block in blocks:
            if len(block) != _len_time:
                raise ValueError("All blocks must animate for the same amount of time")

        self.blocks = blocks
        self.fig = plt.gcf() if fig is None else fig
        self._has_slider = False
        self._pause = False

        def animate(i):
            updates = []
            for block in self.blocks:
                updates.append(block._update(self.timeline.index))
            if self._has_slider:
                self.slider.set_val(self.timeline.index)
            self.timeline._update()
            return updates

        self.animation = FuncAnimation(
            self.fig,
            animate,
            frames=self.timeline._len,
            interval=1000 / self.timeline.fps
        )

    def toggle(self, ax=None):
        """
        Create pause/play button to start/stop animation
        :param ax: matplotlib.axes.Axes, optional
            The matplotlib axes to attach the button to.
        :return:
        """
        if ax is None:
            adjust_plot = {'bottom': .2}
            rect = [.78, .03, .1, .07]

            plt.subplots_adjust(**adjust_plot)
            self.button_ax = plt.axes(rect)
        else:
            self.button_ax = ax

        self.button = Button(self.button_ax, "Pause")
        self.button.label2 = self.button_ax.text(
            0.5, 0.5, 'Play',
            verticalalignment='center',
            horizontalalignment='center',
            transform=self.button_ax.transAxes
        )
        self.button.label2.set_visable(False)

        def pause(event):
            if self._pause:
                self.animation.event_source.start()
                self.button.label.set_visible(True)
                self.button.label2.set_visible(False)
            else:
                self.animation.event_source.stop()
                self.button.label.set_visible(False)
                self.button.label2.set_visible(True)
            self.fig.canvas.draw()
            self._pause ^= True

        self.button.on_clicked(pause)

    def save_gif(self, filename):
        """
        Save the animation to git

        :param filename: str
            the name of the file to be created without the file extension
        :return:
        """
        self.timeline.index -= 1  # required for proper starting point for save
        self.animation.save(filename + '.gif', writer=PillowWriter(fps=self.timeline.fps))

    def save(self, *args, **kwargs):
        """
        Save an animation
                A wrapper around :meth:`matplotlib.animation.Animation.save`
        """
        self.timeline.index = -1  # required for proper starting point for save
        self.animation.save(*args, **kwargs)

    def timeline_slider(self, text='Time', ax=None, valfmt=None, color=None):
        """
        Create a timline slider.

        :param text: str, optional
            The text to display for the slider. Defaults to 'Time'
        :param ax: matplotlib.axes.Axes, optional
            The matplotlib axes to attach the slider to.
        :param valfmt: str, optional
            a format specifier used to print the time
        :param color:
            The color of the slider.
        :return: matplotlib.widget.Slider object
        """
        if ax is None:
            adjust_plot = {'bottom': .2}
            rect = [.18, .05, .5, .03]

            plt.subplots_adjust(**adjust_plot)
            self.slider_ax = plt.axes(rect)
        else:
            self.slider_ax = ax

        if valfmt is None:
            if (np.issubdtype(self.timeline.t.dtype, np.datetime64)
                    or np.issubdtype(self.timeline.t.dtype, np.timedelta64)):
                valfmt = '%s'
            else:
                valfmt = '%1.2f'

        if self.timeline.log:
            valfmt = f'$10^{valfmt}$'

        self.slider = Slider(
            self.slider_ax, text, 0, self.timeline._len - 1,
            valinit=0,
            valfmt=(valfmt + self.timeline.units),
            valstep=1, color=color
        )
        self._has_slider = True

        def set_time(t):
            self.timeline.index = int(self.slider.val)
            self.slider.valtext.set_text(
                self.slider.valfmt % (self.timeline[self.timeline.index]))
            if self._pause:
                for block in self.blocks:
                    block._update(self.timeline.index)
                self.fig.canvas.draw()

        self.slider.on_changed(set_time)
