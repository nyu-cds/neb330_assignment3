# -*- coding: utf-8 -*-
"""
Created on Wed May  3 19:23:57 2017

@author: norabarry

Spark program that counts the number of distinct words in 
the text file pg2701.txt.

"""

from pyspark import SparkContext
import re

# remove any non-words and split lines into separate words
# finally, convert all words to lowercase
def splitter(line):
    line = re.sub(r'^\W+|\W+$', '', line)
    return map(str.lower, re.split(r'\W+', line))

if __name__ == '__main__':
    sc = SparkContext("local", "distinctwordcount")
    text = sc.textFile('pg2701.txt')
    uniq_words = text.flatMap(splitter).distinct().count()
    print("Number of unique words: %d" % uniq_words)