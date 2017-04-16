
#Necessary imports
import numpy
from mpi4py import MPI

'''
   This program is written as an MPI program, and prints different statements based on the rank of the process.  If the rank is odd, the program will print "Goodbye from process x" where x = rank of the process.  If the rank is even, the program will print "Hello"
    '''
#define communicator
comm = MPI.COMM_WORLD

#get the rank of the process
rank = comm.Get_rank()

#check if rank is even
if rank % 2 == 0:
        print("Hello")

#if rank is odd
else:
    print("Goodbye from process", rank)