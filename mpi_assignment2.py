#Necessary imports
import numpy
import sys
from mpi4py import MPI

#initiate MPI communicator
comm = MPI.COMM_WORLD

#get the rank of the process
rank = comm.Get_rank()

#find the number of processes
num_processes = comm.Get_size()


"""This program is written as an MPI program, and can be run with different number of processes.  The program will prompt the user to input an integer less than 100 and each process will then multiply that number by its rank.  At the end, the final number is printed out."""

if rank == 0:
    while(1):
        #prompt user to enter a number
        num = input("Please enter an integer less than 100: ")
        try:
            #test is number is an integer in a try statement to catch any exceptions
            num = int(num)
        except:
            print("Please enter a number.")
            continue
        
        #check if entered integer is less than 100
        if num >= 100:
            print("Please enter an integer less than 100.")
            continue
        else:
            #send the number to the next process
            comm.send(num, dest=1)
            
            #receive the final number in the end and print it out
            num = comm.recv(source=num_processes - 1)
            print(num)
            break

for i in range(1, num_processes):
    if rank == i:
        #receive number from prior process
        num = comm.recv(source=i-1)
        num *= i
        
        #send altered number to next process.
        if i == num_processes - 1:
            comm.send(num, dest=0)
        else:
            comm.send(num, dest=i+1)



