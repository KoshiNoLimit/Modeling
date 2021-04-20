from collections import namedtuple
import csv
import numpy as np
from matplotlib import pyplot as plt

from matplotlib import use

use('macosx')

Town = namedtuple('Town', ['name', 'area', 'density', 'index'])

with open('towns/towns.csv') as f:
    next(f)
    reader = csv.reader(f)
    towns = [Town(x[0], float(x[1]), float(x[2]), int(x[3])) for x in reader]

import plotly.graph_objects as go

xs = np.array([t.area for t in towns])
ys = np.array([t.density for t in towns])
zs = np.array([t.index for t in towns])


# fig = go.Figure(data=[go.Mesh3d(x=xs, y=ys, z=zs, alphahull=1, intensity=zs, colorscale='magma')])
# fig.update_layout(scene=dict(
#                     xaxis_title='area',
#                     yaxis_title='density',
#                     zaxis_title='index'))
# fig.show()

ax = plt.axes(projection="3d")
ax.plot_trisurf(xs, ys, zs, cmap='magma', edgecolor='none')
#ax.scatter(xs, ys, zs, cmap='hot')
ax.set_xlabel('area')
ax.set_ylabel('density')
ax.set_zlabel('index')
plt.show()
