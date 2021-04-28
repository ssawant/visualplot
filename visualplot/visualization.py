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

        def visualize(i):
            updates = []
            for block in self.blocks:
                updates.append(block._update(self.timeline.index))
            if self._has_slider:
                self.slider.set_val(self.timeline.index)
            self.timeline._update()
            return updates
