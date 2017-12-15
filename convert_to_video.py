# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 16:10:51 2017

@author: tom-16s2
"""

import os
os.system("ffmpeg -f image2 -r 10 -i ./Sim_with_table/Cloth1/contour/Contour_%d.jpg -vcodec mpeg4 -y ./Sim_with_table/Cloth1/contour/contour.mp4")