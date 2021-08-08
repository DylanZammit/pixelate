#!/usr/bin/env python3
from colorthief import ColorThief
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os

def get_closest(c, cols, ord=2):
    closest = None
    mindist = 1e9

    for col in cols:
        d = np.linalg.norm(c-col, ord=ord)
        if d < mindist:
            mindist = d
            closest = col
    return closest

parser = argparse.ArgumentParser()

parser.add_argument('--ncol', default=8, type=int, help='Num of cols [def=8]')
parser.add_argument('--pixize', default=30, type=int, help='pixel size [def=30]')
parser.add_argument('--image', default='millie.jpg', type=str, help='image path')
parser.add_argument('--save', action='store_true', help='save image') 
parser.add_argument('--noplot', action='store_true', help='supress plot') 
args = parser.parse_args()

ncol = args.ncol
pixel_size = args.pixize

img_path = args.image
orig = mpimg.imread(img_path)
color_thief = ColorThief(img_path)

w, h, _ = orig.shape

pixel_size = pixel_size+min([w%pixel_size, h%pixel_size])

cols = color_thief.get_palette(color_count=ncol)
cols = [list(x) for x in cols]


N, M = w//pixel_size, h//pixel_size

pixelated = np.zeros(orig.shape)
for n in range(N):
    for m in range(M):
        print(f'{int((n*M+m+1)/(N*M)*100)}%', end='\r')
        startx, starty = n*pixel_size, m*pixel_size
        batch = orig[startx:startx+pixel_size, starty:starty+pixel_size, :]
        mean_col = np.mean(batch, axis=(0, 1)).astype(np.uint8)

        closest = get_closest(mean_col, cols)

        pixelated[startx:startx+pixel_size, starty:starty+pixel_size, :] = closest

pixelated = pixelated.astype(np.uint8)

if not args.noplot:
    fig, ax = plt.subplots(1, 2)
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0, hspace=0)
    ax[0].axis('off')
    ax[1].axis('off')
    ax[0].imshow(orig)
    ax[1].imshow(pixelated)
    plt.show()

if args.save:
    path = os.path.dirname(args.image)
    fn = os.path.basename(args.image).split('.')
    fn=fn[0]+'_pix.'+fn[1]
    mpimg.imsave(os.path.join(path, fn), pixelated)
