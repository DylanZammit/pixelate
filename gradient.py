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

parser.add_argument('--ncol', default=0, type=int, help='Num of cols [def=0]')
parser.add_argument('--alpha', default=0, type=int, help='%% of normal until pixelating [def=0]')
parser.add_argument('--avgpix', default=10, type=int, help='avg pixel size [def=10]')
parser.add_argument('--image', default='millie.jpg', type=str, help='image path')
parser.add_argument('--save', action='store_true', help='save image') 
args = parser.parse_args()

alpha = args.alpha/100
A = args.avgpix
ncol = args.ncol

img_path = args.image
orig = mpimg.imread(img_path)
color_thief = ColorThief(img_path)
if ncol: cols = [list(x) for x in color_thief.get_palette(color_count=ncol)]

h, w, rgb = orig.shape
if rgb == 4: orig = orig[:,:,:3]

N = int(w*(1-alpha)/A)

a = 2*((1-alpha)*w-N)/(N*(N-1))

pixelated = np.zeros(orig.shape)

batch_sizes = [int(a*i+1)+1 for i in range(N)]

starty = int(w*alpha)
pixelated[:, :starty, :] = orig[:, :starty, :]
for n, batch_size in enumerate(batch_sizes):
    startx = 0
    M = int(h/batch_size)+1
    for m in range(M):
        stopx, stopy = startx+batch_size, starty+batch_size
        batch = orig[startx:stopx, starty:stopy, :]
        mean_col = np.mean(batch, axis=(0, 1)).astype(np.uint8)

        if ncol: closest = get_closest(mean_col, cols)

        pixelated[startx:stopx, starty:stopy, :] = closest if ncol else mean_col
        startx = stopx
    starty = stopy

    print(f'{int((n+1)/N*100)}%', end='\r')
    
pixelated = pixelated.astype(np.uint8)

if not args.save:
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
