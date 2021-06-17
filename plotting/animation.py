import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def createAnimation(filename: str, outputfile: str, frames: int):
    data = pd.read_csv(filename)
    fig, ax = plt.subplots()
    ax.set_aspect('equal', 'box')
    times = np.unique(data.time)
    if frames > times.shape[0]:
        print('Frames must be smaller or equal to the number of time steps')
        return
    else:
        increment = int(times.shape[0]/frames)
        animationInd = np.arange(0, times.shape[0], increment)

    def init():
        return [fig]

    def animate(i):
        frameData = data[data.time == times[animationInd[i]]]
        if len(ax.patches) > 0:
            [p.remove() for p in reversed(ax.patches)]
        for row in frameData.iterrows():
            ax.add_patch(plt.Circle((row[1].x, row[1].y),
                                    radius=row[1].radius, fill=False, linewidth=1.5, edgecolor='r'))
        plt.title('Time = {} s'.format(np.round(times[animationInd[i]], 1)))

        return [fig]

    anim = FuncAnimation(fig, animate, init_func=init, frames=frames, interval=20, blit=True)
    anim.save(outputfile, writer='imagemagick')
