from matplotlib import pyplot as plt


class Block:
    def __init__(self, ax=None, t_axis=None):
        self.ax = ax if ax is not None else plt.gca()
        self.t_axis = t_axis
        self._is_list = False

    def _init(self):
        pass

    def _update(self, i):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()

    def _make_slice(self, i, dim):
        if self._is_list:
            return i
        slice_d = [slice(None)] * dim
        slice_d[self.t_axis] = i
        return tuple(slice_d)
