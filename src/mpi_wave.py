"""
Università degli Studi Di Palermo
Corso di Laurea Magistrale in Informatica
Anno Accademico 2020/2021
Cloud e High Performance Computing
@author Salvatore Calderaro
MPI Concurrent Wave Equation - Python Version
"""

import os
import numpy as np
from numpy import pi
from mpi4py import MPI
from time import perf_counter as pc

comm = MPI.COMM_WORLD
taskid = comm.Get_rank()
numtasks=comm.Get_size()
master=0
nsteps=0
npoints=0
first=0
MAXP=10000
MAXSTEPS=10000
MINP=10
RtoL = 10
LtoR = 20
OUT1 = 30
OUT2 = 40

tp=0
ns=0
values=np.zeros(MAXP+2) #valori al tempo t
old_values=np.zeros(MAXP+2) #valori al tempo (t-dt)
new_values=np.zeros(MAXP+2) # valori al tempo (t+dt)
path_txt="res/txt/par/"

"""
This function allows the user to set the number of the points (tp)
and the number of the time steps (ns) and broadcasts the data to workers.
"""
def init_master():
	global tp,ns,comm
	while(True):
		x=input("Inserisci il numero di punti dell'onda [%d-%d]--->" %(MINP,MAXP))
		if(x.isdigit()==True):
			tp=int(x)
			if ((tp < MINP) or (tp > MAXP)):
				print("Errore ! Inserire valori compresi tra %d e %d " %(MINP,MAXP))
			else:
				os.system("clear")
				break

		else:
			print("Errore ! Inserire un numero intero")

	while(True):
		y=input("Inserisci il numero di time steps [1-%d]--->" %(MAXSTEPS))
		if(y.isdigit()==True):
			ns=int(y)
			if ((ns < 1) or (ns > MAXSTEPS)):
				print("Errore ! Inserire valori compresi tra 1 e %d " %(MAXSTEPS))
			else:
				os.system("clear")
				break

		else:
			print("Errore ! Inserire un numero intero")
	comm.bcast(tp, root=0)
	comm.bcast(ns, root=0)

"""
The workers recieve the data (tp,ns) from the master
"""
def init_workers():
	global comm,tp,ns
	tp=comm.bcast(tp, root=0)
	ns=comm.bcast(ns, root=0)
 
"""
This fuction identifies and returns left and right neighbors
"""
def identify_left_right_processors():
    global taskid,numtasks
    left=0
    right=0
    if(taskid == numtasks-1):
        right=0
    else:
        right=taskid+1
        
    if(taskid==0):
        left=numtasks-1
    else:
        left=taskid-1
        
    return (left,right)

"""
This function inizializes points on line calculating the initial
values based on sine curve. Each task calculates its point.
"""
def init_line():
	global tp,ns,numtasks,taskid,first,npoints
	nmin=tp//numtasks
	nleft=tp%numtasks
	f=2*pi
	k=0.0
	npts=0
	for i in range(numtasks):
		if(i<nleft):
			npts=nmin+1
		else:
			npts=nmin
		if(taskid==i):
			first=k+1
			npoints=npts
			print ("Task=%d \t  Primo punto=%d \t  numero di punti=%d\n" %(taskid,first, npts))
			tmp=tp-1
			for j in range(1,npts+1):
				x=k/tmp
				values[j]=np.sin(f * x)
				#print("%6.4f " %(values[j]), end=" ")
				old_values[j]=values[j]
				k=k+1
		else:
			k=k+npts

"""
All processes update their points a specified number of times
"""
def update():
	global ns,values,old_values,new_values,first,nsteps,comm,npoints,RtoL,LtoR,taskid

	left,right=identify_left_right_processors()
	dtime = 0.3
	c = 1.0
	dx = 1.0
	tau = (c * dtime / dx)
	sqtau = tau * tau
	"""
	print("-----------------------------------")
	print("Aggiornamento valori\n")
 	print(left,right,taskid)
	print ("Task=%d \t  Primo punto=%d \t  numero di punti=%d\n" %(taskid,first, npoints))
	print("-----------------------------------")
	"""
	for i in range(1,ns+1):
		if(first!=1):
			comm.send(values[1],dest=left,tag=RtoL)
			values[0]=comm.recv(source=left,tag=LtoR)

		if(first + npoints -1 != tp):
			comm.send(values[npoints],dest=right,tag=LtoR)
			values[npoints+1]=comm.recv(source=right,tag=RtoL)

		for j in range(1,npoints+1):
			if((first+j-1 == 1) or (first+j-1==tp)):
				new_values[j]=0
			else:
				new_values[j] = (2.0 * values[j]) - old_values[j] + (sqtau * (values[j-1]
				- (2.0 * values[j]) + values[j+1]))
		
		for j in range(1,npoints+1):
			old_values[j]=values[j]
			values[j]=new_values[j]



"""
Master receives results from workers and prints. The final result is saved in a txt file.
"""
def output_master():
	global tp,numtasks,comm,OUT1,OUT2,start,npts,values,start,first,npoints,path_txt
	result=np.zeros(tp)

	buffer=np.zeros(2)
	for i in range(1,numtasks):
		buffer=comm.recv(source=i,tag=OUT1)
		start=int(buffer[0])
		npts=int(buffer[1])
		data=comm.recv(source=i,tag=OUT2)
		"""
		print(buffer)
		print(data)
		"""
		result[start-1:start+npts-1]=data

	i=first
	for i in range(int(first+npoints)):
		result[i-1]=values[i]
	return result


"""
Workers send the updated values to the master
"""
def output_workers():
	global comm,first,npoints,values,OUT1,OUT2
	buffer=np.zeros(2)
	buffer[0]=first
	buffer[1]=npoints
	comm.send(buffer,dest=master,tag=OUT1)
	data=values[1:npoints+1]
	comm.send(data,dest=master,tag=OUT2)

def save_print_result(result):
	global tp,ns,path_txt
	print("Stampa dei risultati finali....")
	for i in range(0,tp):
		print("%6.4f " %(result[i]), end=" ")
		if((i+1) % 10 == 0):
				print("\n")

	path_txt=path_txt+"wawe_"+str(tp)+"_"+str(ns)+"_par"+".txt"
	np.savetxt(path_txt,result)

"""
Main routine
"""
def main():
	global comm,taskid,numtasks,master,comm,tp
	if(numtasks<2):
		print("Errore il numero di task MPI è %d" %(numtasks))
		print("Inserire almeno due task !")
		exit(0)
  
	if(taskid==master):
		init_master()
		print("Inizio, numtasks=%d \n" %(numtasks))
		print("Numero di punti scelti: %d , numero di steps: %d \n" %(tp,ns))
	else:
		init_workers()

	start_time=pc()
	init_line()
	update()
	if(taskid==master):
		result=output_master()
		end_time=pc()-start_time
		save_print_result(result)
		print("Eseguito in {} s ".format(end_time))
		exit(0)
	else:
		output_workers()

if __name__ == '__main__':
	main()