#Necessary imports
import numpy as np
import random
import sys
from mpi4py import MPI

#initiate MPI communicator
comm = MPI.COMM_WORLD

#get the rank of the process
rank = comm.Get_rank()

#find the number of processes
NUM_PROCESSES = comm.Get_size()

#How many elements to sort
N = 10000


"""

Author: Nora Barry

Date: April 21, 2017

This program is written as an MPI program, and can be run with different number of processes.  
The program will generate a large unsorted group of integers, and by using collective communication,
distributes ranges of integers to different processes to sort.  After the processes are done sorting,
the root process gathers the sorted arrays of integers, concatenates them, and prints out the final 
sorted array. 

"""

def generate_numbers(n):
    '''Generates random list of numbers of length n.'''
    numbers = [np.random.randint(-n,n) for i in range(n)]
    return numbers
    
def split_numbers(nums, num_processes):
    '''
    Takes list of numbers and finds the optimal places to split numbers
    into a certain number of sublists (one for each process)
    
    Args:
        nums: list of random numbers
    Returns:
        range_maxs: list of the the maximum values for each range.
    '''
    rnge = max(nums) - min(nums)
    range_lst = np.array_split(np.array(range(rnge+1)), num_processes)
    range_maxs = [max(x) for x in range_lst]
    return range_maxs
    
def create_to_sort_array(nums, ranges, num_processes):
    '''
    Creates final array of sets of numbers to send to each process.
    Args:
        nums: list of random numbers
        ranges: list of the the maximum values for each range.
    Returns:
        to_sort: np array with each element being a list of numbers
        for process i to sort
    '''
    to_sort = []
    to_sort.append([x for x in nums if x in range(min(nums), ranges[0]+1)])
    for i in range(1, num_processes):
        last_max = ranges[i-1]
        to_sort.append([x for x in nums if x in range(last_max + 1, ranges[i]+1)])
        
    #change list into array so we can use scatter method
    return np.array(to_sort)

    
if rank == 0:
    #generate random group of integers
    numbers = generate_numbers(N)
    
    #find the range of integers so we can split between processes
    range_maxs = split_numbers(numbers, NUM_PROCESSES)
    
    #put together the final list with integers to send to each process
    to_sort = create_to_sort_array(numbers, range_maxs, NUM_PROCESSES)
    
else:
    to_sort = None

#scatter to_sort to other processes
to_sort = comm.scatter(to_sort, root = 0)

#sort 
process_sort = np.sort(to_sort)

#process 0 gathers
final_sort = comm.gather(process_sort, root=0)

if rank == 0:
    final_sort = np.concatenate(final_sort)
    print(final_sort)

    



