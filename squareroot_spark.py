# -*- coding: utf-8 -*-
"""
Created on Wed May  3 19:20:44 2017

@author: norabarry

Spark program that computes the mean of the square roots of all numbers 
in range(1000)

"""

from pyspark import SparkContext
import numpy as np

if __name__ == '__main__':
    sc = SparkContext("local", "squareroot")
    sqr_roots = sc.parallelize(range(1, 1000)).map(lambda x: np.sqrt(x)).fold(0, lambda x,y: x+y)
    print(sqr_roots/999)