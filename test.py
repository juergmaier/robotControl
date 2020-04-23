
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

def update_lines(num, dataLines, lines):
    for line, data in zip(lines, dataLines):
        # NOTE: there is no .set_data() for 3 dim data...
        line.set_data(data[0:2, :num])
        line.set_3d_properties(data[2, :num])
        line.set_marker("o")
    return lines

# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

# Lines to plot in 3D
t = np.linspace(-2*np.pi,2*np.pi,50)
x1, y1, z1 = np.cos(t), np.sin(t), t/t.max()
x2, y2, z2 = t/t.max(), np.cos(t), np.sin(t)
data = np.array([[x1,y1,z1],[x2,y2,z2]])

# NOTE: Can't pass empty arrays into 3d version of plot()
lines = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0] for dat in data]

ax.set_xlim(-1.1,1.1)
ax.set_ylim(-1.1,1.1)
ax.set_zlim(-1.1,1.1)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
#plt.rcParams['animation.html'] = 'html5'

line_ani = animation.FuncAnimation(fig, update_lines, 50, fargs=(data, lines),
                                   interval=100, blit=True, repeat=True)

plt.show()