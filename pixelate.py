import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from IPython import embed
import pdb

from colorthief import ColorThief

def get_closest(c, cols, ord=2):
    closest = None
    mindist = 1e9

    for col in cols:
        d = np.linalg.norm(c-col, ord=ord)
        if d < mindist:
            mindist = d
            closest = col

    return closest

img_path = 'millie.jpg'
orig = mpimg.imread(img_path)
color_thief = ColorThief(img_path)

ncol = 8
pixel_size = 30

w, h, _ = orig.shape

pixel_size = pixel_size+min([w%pixel_size, h%pixel_size])

cols = color_thief.get_palette(color_count=ncol)
cols = [list(x) for x in cols]


N, M = w//pixel_size, h//pixel_size

pixelated = np.zeros(orig.shape)
for n in range(N):
    for m in range(M):
        startx, starty = n*pixel_size, m*pixel_size
        batch = orig[startx:startx+pixel_size, starty:starty+pixel_size, :]
        mean_col = np.mean(batch, axis=(0, 1)).astype(np.uint8)
        #batch_thief = ColorThief(batch)
        #mean_col = color_thief.get_color(quality=1)

        closest = get_closest(mean_col, cols)

        pixelated[startx:startx+pixel_size, starty:starty+pixel_size, :] = closest

fig, ax = plt.subplots(1, 2)
ax[0].axis('off')
ax[1].axis('off')
ax[0].imshow(orig)
ax[1].imshow(pixelated.astype(np.uint8))
plt.show()
