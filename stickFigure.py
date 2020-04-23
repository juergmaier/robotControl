
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3
import numpy as np

import config
import ik

'''
def zoom_factory(ax,base_scale = 2.):
    def zoom_fun(event):
        # get the current x and y limits
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
        cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
        xdata = event.xdata # get event x location
        ydata = event.ydata # get event y location
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1/base_scale
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1
            print (event.button)
        # set new limits
        ax.set_xlim([xdata - cur_xrange*scale_factor,
                     xdata + cur_xrange*scale_factor])
        ax.set_ylim([ydata - cur_yrange*scale_factor,
                     ydata + cur_yrange*scale_factor])
        plt.draw() # force re-draw

    fig = ax.get_figure() # get the figure of interest
    # attach the call back
    fig.canvas.mpl_connect('scroll_event',zoom_fun)

    #return the function
    return zoom_fun
'''

def updateStickFigure(i, data, lines):

    #config.log(f"servoCurrent for leftArm.rotate: {config.servoCurrent['leftArm.rotate'].position}")

    lineIndex = 1
    for chainName, chain in ik.dhChains.items():
        links = chain['chain']
        pos1 = links.positions()[:-1]
        pos2 = links.positions()[1:]

        for point_pairs in zip(pos1, pos2):
            xs, ys, zs, linesize = zip(*point_pairs)
            lines[lineIndex].set_data(xs,ys)
            lines[lineIndex].set_3d_properties(zs)
            lines[lineIndex].set_linewidth(linesize[1])
            lineIndex += 1
            if lineIndex == len(lines): return lines

    return lines


def showRobot():

    # Attaching 3D axis to the figure
    fig = plt.figure()
    ax = p3.Axes3D(fig)

    allData = np.array([[[0.0,0.0],[0.0,0.0],[0.0,0.0],[1.0,1.0]]])

    # lines to plot, each link is a line
    for chainName, chain in ik.dhChains.items():
        links = chain['chain']
        pos1 = links.positions()[:-1]
        pos2 = links.positions()[1:]

        for point_pairs in zip(pos1, pos2):
            xs, ys, zs, linesize = zip(*point_pairs)
            lineData = np.array([[xs,ys,zs,linesize]])
            allData = np.concatenate((allData, lineData))

    lines = [ax.plot(line[0], line[1], line[2], linewidth=line[3][1])[0] for line in allData]

    # Setting the axes properties
    ax.set_xlim3d([-1.0, 1.0])
    ax.set_xlabel('X')

    ax.set_ylim3d([-1.0, 1.0])
    ax.set_ylabel('Y')

    ax.set_zlim3d([0.0, 2.0])
    #ax.set_zlabel('Z')

    ax.set_title('Marvin 3D Positions')

    #anim = animation.FuncAnimation(fig, updateStickFigure, fargs=(allData, lines), repeat_delay=500, blit=True)

    plt.show()
