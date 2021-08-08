#!/usr/bin/env python3
from colorthief import ColorThief
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument('--alpha', default=0, type=int, help='%% of normal until pixelating [def=0]')
parser.add_argument('--avgpix', default=10, type=int, help='avg pixel size [def=10]')
parser.add_argument('--image', default='millie.jpg', type=str, help='image path')
parser.add_argument('--save', action='store_true', help='save image') 
parser.add_argument('--noplot', action='store_true', help='supress plot') 
args = parser.parse_args()

alpha = args.alpha/100
A = args.avgpix

img_path = args.image
orig = mpimg.imread(img_path)
color_thief = ColorThief(img_path)

h, w, _ = orig.shape

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
        pixelated[startx:stopx, starty:stopy, :] = mean_col
        startx = stopx
    starty = stopy

    print(f'{int((n+1)/N*100)}%', end='\r')
    
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
