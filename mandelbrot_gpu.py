# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 09:25:38 2017

Author: Nora Barry, with starter code from NYU Advanced Python class.

"""

#
# Simple Python program to calculate elements in the Mandelbrot set.
#
from __future__ import division
from numba import cuda
import numpy as np
from pylab import imshow, show
import math

@cuda.jit(device=True)
def mandel(x, y, max_iters):
    '''
    Given the real and imaginary parts of a complex number,
    determine if it is a candidate for membership in the 
    Mandelbrot set given a fixed number of iterations.
    '''
    c = complex(x, y)
    z = 0.0j
    for i in range(max_iters):
        z = z*z + c
        if (z.real*z.real + z.imag*z.imag) >= 4:
            return i
            
    return max_iters

@cuda.jit
def compute_mandel(min_x, max_x, min_y, max_y, image, iters):
    '''
    CUDA function to calculate the mandel value for each element in the 
    image array. The real and imag variables contain a 
    value for each element of the complex space defined 
    by the X and Y boundaries (min_x, max_x) and 
    (min_y, max_y).
    '''
    #Obtain starting x and y coordinates for the particular grid
    x_init, y_init = cuda.grid(2)    
    
    #Find height and width of the 2D image array 
    height = image.shape[0]
    width = image.shape[1]

    #Calculate pixel size for x and y dimensions
    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height
    
    #Calculate ending x and y coordinates for the particular grid
    x_final, y_final = cuda.gridDim.x * cuda.blockDim.x, cuda.gridDim.y * cuda.blockDim.y    
    
    #Finally, iterate through grid and calculate the values for image[y,x] 
    #using mandel(x,y)
    for x in range(x_init, width, x_final):
        real = min_x + x * pixel_size_x
        for y in range(y_init, height, y_final):
            imag = min_y + y * pixel_size_y
            image[y, x] = mandel(real, imag, iters)

            
if __name__ == '__main__':
    image = np.zeros((1024, 1536), dtype = np.uint8)
    blockdim = (32, 8)
    griddim = (32, 16)
    image_global_mem = cuda.to_device(image)
    compute_mandel[griddim, blockdim](-2.0, 1.0, -1.0, 1.0, image_global_mem, 20) 
    image_global_mem.copy_to_host()
    imshow(image)
    show()