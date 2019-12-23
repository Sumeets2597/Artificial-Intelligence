#!/usr/local/bin/python3
#
# Authors: Ruta (rutture), Rushikesh (rgawande), Sumeet (ssarode)
#
# Mountain ridge finder
# Based on skeleton code by D. Crandall, Oct 2019
#

from PIL import Image
from numpy import *
import numpy
from scipy.ndimage import filters
import sys
import imageio
import pandas as pd

# calculate "Edge strength map" of an image
#
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_edge(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return numpy.array(image)

# main program
#
(input_filename, gt_row, gt_col) = sys.argv[1:]

# load in image 
input_image = Image.open(input_filename)

# compute edge strength mask
edge_strength = edge_strength(input_image)
imageio.imwrite('edges.jpg', uint8(255 * edge_strength / (amax(edge_strength))))

# You'll need to add code here to figure out the results! For now,
# just create a horizontal centered line.
#ridge = [ edge_strength.shape[0]/2 ] * edge_strength.shape[1]
df = pd.DataFrame(data=edge_strength, index=None)
ridge = df.idxmax().tolist()
# output answer part 1
imageio.imwrite("output_simple.jpg", draw_edge(input_image, ridge, (0, 0, 255), 5))

df=(df-df.min())/(df.max()-df.min())
obs = []
states = []
start_p = {}
n = 1/len(df)
ones = [n]*len(df.columns)

for i in range(0,len(df.columns)):
    obs.append(i)
for i in range(0,len(df)):
    states.append(i)
for i in range(0,len(df.columns)):
    start_p[i] = 1 - i*n

trans={}
for i in range(0,len(df)): 
    trans[i] = start_p
emit_p = df.T.to_dict()

#trans_p = numpy.zeros(shape=(len(df),len(df.columns)))  
#for i in range(0,len(df)):
#    k = 0
#    for j in range(i,0,-1):
#        if i==j:
#            trans_p[i][j] = 1
#        else:
#            trans_p[i][j] = 1 - n*k
#            k += 1
#    k = 0
#    for j in range(i+1,len(df.columns)):
#        trans_p[i][j] = 1 - n*k
#        k += 1
#trans_p = numpy.square(trans_p)

#The pseudocode for viterbi function is referenced from Wikipedia
def viterbi(ob, hid, startp, transp, emitp):
    T = [{}]
    for h in hid:
        T[0][h] = {"prob": startp[h] * emitp[h][ob[0]], "prev": None}
 
    for t in range(1, len(ob)):
        T.append({})
        for h in hid:
            max_trp = T[t-1][hid[0]]["prob"]*transp[hid[0]][h]
            prev = hid[0]
            for prev_st in hid[1:]:
                tr_prob = T[t-1][prev_st]["prob"]*transp[prev_st][h]
                if tr_prob > max_trp:
                    max_trp = tr_prob
                    prev = prev_st
        
            maxp = max_trp * emitp[h][ob[t]]
            T[t][h] = {"prob": maxp, "prev": prev}                
    opt = []

    maxp = max(value["prob"] for value in T[-1].values())
    p = None

    for st, data in T[-1].items():
        if data["prob"] == maxp:
            opt.append(st)
            p = st
            break

    for t in range(len(T) - 2, -1, -1):
        opt.insert(0, T[t + 1][p]["prev"])
        p = T[t + 1][p]["prev"]

    return opt
       
ridge = viterbi(obs, states, start_p, trans, emit_p)
imageio.imwrite("output_map.jpg", draw_edge(input_image, ridge, (255, 0, 0), 5))


def viterbi_human(ob, hid, startp, transp, emitp):
    T = [{}]
    for h in hid:
        if h == gt_row:
            pr = 1
        else:
            pr = startp[h] * emitp[h][ob[0]]
        T[0][h] = {"prob": pr, "prev": None}

    for t in range(1, len(ob)):
        T.append({})
        for h in hid:
            max_trp = T[t-1][hid[0]]["prob"]*transp[hid[0]][h]
            prev = hid[0]
            for prev_st in hid[1:]:
                tr_prob = T[t-1][prev_st]["prob"]*transp[prev_st][h]
                if tr_prob > max_trp:
                    max_trp = tr_prob
                    prev = prev_st
        
            maxp = max_trp * emitp[h][ob[t]]
            if t == gt_col and h == gt_row:
                T[t][h] = {"prob": 1, "prev": prev}
            else:
                T[t][h] = {"prob": maxp, "prev": prev}                
    opt = []

    maxp = max(value["prob"] for value in T[-1].values())
    p = None

    for st, data in T[-1].items():
        if data["prob"] == maxp:
            opt.append(st)
            p = st
            break

    for t in range(len(T) - 2, -1, -1):
        opt.insert(0, T[t + 1][p]["prev"])
        p = T[t + 1][p]["prev"]
        
    return opt

ridge = viterbi_human(obs, states, start_p, trans, emit_p)
imageio.imwrite("output_human.jpg", draw_edge(input_image, ridge, (0, 255, 0), 5))

