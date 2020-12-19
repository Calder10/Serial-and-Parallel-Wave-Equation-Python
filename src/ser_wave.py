"""
=================================================
Università degli Studi Di Palermo
Corso di Laurea Magistrale in Informatica
Anno Accademico 2020/2021
Cloud e High Performance Computing
@author Salvatore Calderaro
Serial Concurrent Wave Equation - Python Version
=================================================
"""

import os
from tqdm import tqdm
import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
from celluloid import Camera
from time import perf_counter as pc

MAXP=10000
MAXSTEPS=10000
MINP=10
values=np.zeros(MAXP+2) #valori al tempo t
old_values=np.zeros(MAXP+2) #valori al tempo (t-dt)
new_values=np.zeros(MAXP+2) # valori al tempo (t+dt)
plot_values=[]
tp=0
ns=0
t=0
path_txt="res/txt/ser/"
path_gif="res/gif/"
path_img="res/img/"


"""
This function allows the user to set the number of the points (tp)
and the number of the time steps (ns).
"""
def init_param():
	global tp,ns,ta,t
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
	if(ns<1000):
		t=10
	else:
		t=100
	print("Numero di punti scelti: %d , numero di steps: %d \n" %(tp,ns))


"""
This function inizializes points on line calculating the initial
values based on sine curve.
"""
def create_line():
	global tp,values,plot_values
	f=2 * pi
	k=0.0
	tmp = tp-1
	for i in range(1,tp+1):
		x=k/tmp
		values[i]=np.sin(f * x)
		old_values[i]=values[i]
		k=k+1
	#plot_values.append(list(values[1:tp+1]))


"""
This fuction update all values along line a specified number of times (ns)
"""
def update():
	global ns,tp,values,old_values,new_values,t,plot_values
	dt=0.3
	c=1
	dx=1
	tau=(c*dt/dx)
	sqtau=tau*tau
	for i in tqdm(range(1, ns+1)):
		for j in range(1,tp+1):
			if (j==1 or j==tp):
				new_values[j]=0
			else:
				new_values[j] = (2.0 * values[j]) - old_values[j] + (sqtau * (values[j-1]
				- (2.0 * values[j]) + values[j+1]))

		for j in range(1,tp+1):
			old_values[j]=values[j]
			values[j]=new_values[j]

	"""
		if((i % t)==0):
			plot_values.append(list(values[1:tp+1]))
	
	if((ns % t) !=0):
		plot_values.append(list(values[1:tp+1]))
	"""

"""
This function prints the final values of the wave's amplitude
"""
def print_values():
	global values,tp
	for i in range(1,tp+1):
		print("%6.4f " %(values[i]), end=" ")
		if(i % 10 == 0):
			print("\n")

"""
This function saves the final result in a txt file.
"""
def save_result():
	global values,tp,ns,plot_values,path_txt
	result=np.zeros(tp)
	result=values[1:tp+1]
	path_txt=path_txt+"wawe_"+str(tp)+"_"+str(ns)+"_ser"+".txt"
	np.savetxt(path_txt,result)

"""
This function plots the initial and the final wave.
"""
def plot_initial_final_wave():
	global values,tp,ns,plot_values,path_img
	path_img=path_img+"wawe_"+str(tp)+"_"+str(ns)+".png"
	position=np.arange(1,tp+1,1)
	amplitude=values[1:tp+1]
	fig,axs=plt.subplots(2)
	fig.suptitle("Wave, tpoints=%d, nsteps=%d: initial and final wave" %(tp,ns))
	axs[0].set_title("Initial wave")
	axs[0].set_xlabel("Position")
	axs[0].set_xlim(1,tp)
	axs[0].set_ylabel("Amplitude")
	axs[0].grid(True, which='both')
	axs[0].axhline(y=0, color='k')
	axs[0].plot(position,plot_values[0],linewidth=2)

	axs[1].set_title("Final wave")
	axs[1].set_xlabel("Position")
	axs[1].set_xlim(1,tp)
	axs[1].set_ylabel("Amplitude")
	axs[1].grid(True, which='both')
	axs[1].axhline(y=0, color='k')
	axs[1].plot(position,plot_values[-1],linewidth=2)
	plt.tight_layout()
	plt.show()
	fig.savefig(path_img)

"""
This function shows the
"""
def plot_animate_wave():
	global tp,ns,plot_values,path_gif
	path_gif=path_gif+"wawe_"+str(tp)+"_"+str(ns)+".gif"
	position=np.arange(1,tp+1,1)
	fig=plt.figure()
	plt.title("Wave, tpoints=%d, nsteps=%d" %(tp,ns))
	plt.xlabel("Position")
	plt.xlim(1,tp)
	plt.ylabel("Amplitude")
	plt.grid(True, which='both')
	plt.axhline(y=0, color='k')
	camera = Camera(fig)
	for amplitude in plot_values:
		plt.plot(position,amplitude,linewidth=2)
		camera.snap()
	animation = camera.animate()
	plt.tight_layout()
	plt.show()
	animation.save(path_gif,writer = 'imagemagick')


"""
Main routine.
"""
def main():
	print("Inserimento dei parametri....")
	init_param()
	print("Inizio.....\n")
	print("Inizializzazione dei punti sull'onda....\n")
	start_time = pc()
	create_line()
	print("Aggiornamento di tutti i valori per ogni istante di tempo....\n")
	update()
	end_time=pc()-start_time
	print("Stampa dei risultati finali....\n")
	print_values()
	#plot_initial_final_wave()
	#plot_animate_wave()
	#save_result()
	print("Eseguito in {} s ".format(end_time))
	exit(0)

if __name__ == "__main__":
    main()
