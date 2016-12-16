"""
A simple example of an animated plot
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import brownian as br
#time.strftime("%Y/%m/%d %X")

# fig, axes = plt.subplots(1, 1, squeeze=False)

# paths = 1
# x = np.arange(0, 61, 1)

# gbrm = br.gen_brownian_path(60)
# #print(rw)
# path_lines = [br.gen_brownian_path(60) for _ in range(paths)]
# lines = []
# for index, path in enumerate(path_lines):
#     line, = axes.flatten()[index].plot(x, path)
#     lines.append(line)
# #ax.set_yticklabels(['a' for _ in range(6)])

# # _max = max(rw)
# # _min = min(rw)
# # ax.set_ylim(_min - 15, _max + 15)


# def animate(par):
#     #print(par, args)
#     for index, line in enumerate(lines):
#         old_y = line.get_ydata()
#         new_y = br.gen_brownian_factor(60) * old_y[-1]
#         #print(new_y)
#         new_y_array = np.append(old_y[1:], np.array([new_y])) 

#     #ax.clear()
#     #ax.plot(x, new_y_array)

#         _max = max(new_y_array)
#         _min = min(new_y_array)
#         axes.flatten()[index].set_ylim(_min - _min * 0.01, _max + _max * 0.01)
    
#         line.set_ydata(new_y_array)  # update the data
#     return lines


# # Init only required for blitting to give a clean slate.
# def init():
#     #print('init was called')
#     line.set_ydata(np.ma.array(gbrm))
#     return line,
# # , np.arange(1, 200)
# # ani = animation.FuncAnimation(fig, animate, init_func=init,
# #                               fargs=[10], interval=20)
# fig.show()

# #time.sleep(100)
# ani = animation.FuncAnimation(fig, animate, init_func=init, interval=20)




class DashBoard(object):

    def __init__(self, aspect_ratio=(1,1), data=None):
        self.trackable_dictionary = {}
        self.aspect_ratio = aspect_ratio
        self.data = None
        self.lines = None
        self.animation_instance = None
        self.figure, self.axes = plt.subplots(*self.aspect_ratio, squeeze=False)

    def set_data(self, data):
        try:
            iter(data)
        except TypeError:
            print("data must be provided as an iterable of series, numpy arrays or lists to plot")
        self.data = data
        self._plot()

    # def set_trackable_data(self, series_lenght=60):
    #     for trackable in self.trackable_dictionary:
    #         self.element.get_last_datapoint()

    def set_brownian_data(self, number_of_series=None, series_lenght=60):
        if not number_of_series:
            number_of_series = self.aspect_ratio[0] * self.aspect_ratio[1]
        data = []
        for _ in range(number_of_series):
            data.append(br.gen_brownian_path(series_lenght))
        self.data = data

    def show_animated(self, interval=50, blit=False):
        self.figure, self.axes = plt.subplots(*self.aspect_ratio, squeeze=False)
        self._plot()
        self.animation_instance = animation.FuncAnimation(self.figure, self._animate, init_func=self._init_animate, interval=interval, blit=blit)
        self.figure.show()

    def _animate(self, default_frame):
            
        for index, line in enumerate(self.lines):
            old_y = line.get_ydata()
            new_y = br.gen_brownian_factor(len(old_y) - 1) * old_y[-1]

            new_y_array = np.append(old_y[1:], np.array(new_y))
            _max = max(new_y_array)
            _min = min(new_y_array)
            self.axes.flatten()[index].set_ylim(_min - _min * 0.01, _max + _max * 0.01)
            line.set_ydata(new_y_array)
        return self.lines

    def _init_animate(self):
        for index, line in enumerate(self.lines):
            line.set_ydata(np.ma.array(self.data[index]))
            return self.lines

    def _plot(self):
        lines =[]
        if self.data:
            for index, series in enumerate(self.data):
                line, = self.axes.flatten()[index].plot(np.arange(0, len(series), 1), series)
                lines.append(line)
            self.lines = lines
        else:
            print("There is no data to plot")

    def show(self):
        self.figure, self.axes = plt.subplots(*self.aspect_ratio, squeeze=False)
        self._plot()
        self.figure.show()


if __name__ == '__main__':
    db = DashBoard((3, 2))
    db.set_brownian_data()
    db.show_animated()