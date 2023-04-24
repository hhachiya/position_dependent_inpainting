import pickle
import os
import matplotlib.pylab as plt
from argparse import ArgumentParser
from PIL import Image
import numpy as np
import copy
import pdb

#%%%
def parse_args():
    parser = ArgumentParser(description="visualization of data used in position dependent inpainting")

    parser.add_argument('-data',type=str,default='quake-all',help='name of data, \'quake-all\', \'quake-east\', \'quake-west\', or \'toy\' (default=quake-all)')    
    parser.add_argument('-mode',type=str,default='train',help='name of mode, \'train\', \'test\', or \'valid\' (default=train)')
    parser.add_argument('-cv',type=int,default=0,help='number of cross validation 0-9 (default=0)')
    parser.add_argument('-start_ind',type=int,default=0,help='start index (default=0)')
    parser.add_argument('-display_num',type=int,default=5,help='number of images displayed (default=5)')

    return parser.parse_args()

args = parse_args()

#---------------------
# conver to data to path
if args.data == 'quake-all':
    root_path = f'data{os.sep}quakeData-all-crossVaridation{args.cv}'
elif args.data == 'quake-east':
    root_path = f'data{os.sep}quakeData-h04h05h09h10-crossVaridation{args.cv}'
elif args.data == 'quake-west':
    root_path = f'data{os.sep}quakeData-h01h02h06h07-crossVaridation{args.cv}'
elif args.data == 'toy':
    root_path = f'data{os.sep}stripe-rectData256_v2'

data_path = os.path.join(root_path,f'{args.mode}.pickle')
mask_path = os.path.join(root_path,f'{args.mode}_mask.pickle')
#---------------------

#---------------------
# load image, label, mask, and exist
with open(data_path,'rb') as fp:
    data = pickle.load(fp)

with open(mask_path,'rb') as fp:
    masks = pickle.load(fp)

imgs = np.squeeze(data['images'])
labels = np.array(data['labels'])
masks = np.squeeze(masks)

# load pixel-wise data exist flag
existPath = f"data{os.sep}sea.png" if "quake" in args.data else ""
exist = np.array(Image.open(existPath))/255 if existPath!="" else np.ones(data['images'].shape[1:3])

# sort by label
if args.data == 'toy':
    inds=labels.astype(int).argsort()
    labels = labels[inds]
    imgs = imgs[inds]
    masks = masks[inds]

print(f"# of images:{len(imgs)}")
#---------------------

#---------------------
# visualize image and mask
for ind in np.arange(args.start_ind,np.min([args.start_ind + args.display_num,len(imgs)])):
    img = np.squeeze(imgs[ind])
    mask = np.squeeze(masks[ind])    
    label = labels[ind]

    fig = plt.figure(figsize=(10,5),dpi=120)
    fig.suptitle(label)

    # plot image
    img[img<0]=0
    img[exist==0]=-1
    cmapred = copy.copy(plt.get_cmap("Reds"))
    cmapred.set_under('grey')
    fig.add_subplot(1,3,1).set_title('image')    
    plt.imshow(img,cmap=cmapred,interpolation="None",vmin=0,vmax=1)

    # plot mask
    fig.add_subplot(1,3,2).set_title('mask')    
    plt.imshow(mask,cmap="gray",interpolation="None",vmin=0,vmax=1)

    # plot masked image
    masked_img = img*mask
    masked_img[masked_img<=0]=-1
    cmapred = copy.copy(plt.get_cmap("Reds"))
    cmapred.set_under('black')
    fig.add_subplot(1,3,3).set_title('masked image')    
    plt.imshow(masked_img,cmap=cmapred,interpolation="None",vmin=0,vmax=1)

    fig.tight_layout()

    plt.show()
    
#---------------------
