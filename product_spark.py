# -*- coding: utf-8 -*-
"""
Created on Wed May  3 19:45:40 2017

@author: norabarry

Spark program that computes the product of all numbers in range(1000)

"""

from pyspark import SparkContext

if __name__ == '__main__':
    sc = SparkContext("local", "product")
    print(sc.parallelize(range(1, 1000)).fold(1, lambda a,b:a*b))