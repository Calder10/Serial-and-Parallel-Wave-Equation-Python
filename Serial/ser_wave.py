"""
Serial Concurrent Wave Equation - Python Version
"""
import os
import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
from time import perf_counter as pc

MAXP=10000
MAXSTEPS=10000
MINP=20
values=np.zeros(MAXP+2) #valori al tempo t
old_values=np.zeros(MAXP+2) #valori al tempo (t-dt)
new_values=np.zeros(MAXP+2) # valori al tempo (t+dt)
tp=0
ns=0

"""
Funzione che permette l'inserimento del numero di punti dell'onda
e il numero di time steps.
"""
def init_param():
	global tp,ns
	while(True):
		x=input("Inserisci il numero di punti dell'onda [%d-%d]--->" %(MINP,MAXP))
		if(x.isdigit()==True):
			tp=int(x)
			if ((tp < MINP) or (tp > MAXP)):
				print("Errore ! Inserire valori compresi tra %d e %d " %(MINP,MAXP))
			else:
				break
				os.system("clear")
		else:
			print("Errore ! Inserire un numero intero")

	while(True):
		y=input("Inserisci il numero di time steps [1-%d]--->" %(MAXSTEPS))
		if(y.isdigit()==True):
			ns=int(y)
			if ((ns < 1) or (ns > MAXSTEPS)):
				print("Errore ! Inserire valori compresi tra 1 e %d " %(MAXSTEPS))
			else:
				break
				os.system("clear")
		else:
			print("Errore ! Inserire un numero intero")

	print("Numero di punti scelti: %d , numero di steps: %d" %(tp,ns))


"""
Calcolo dei valori iniziali basati su una sinusoide
"""
def create_line():
	global tp,values
	f=2 * pi
	k=0.0
	tmp = tp-1
	for i in range(1,tp+1):
		x=k/tmp
		values[i]=np.sin(f * x)
		old_values[i]=values[i]
		k=k+1


"""
Aggiorna tutti i valori lungo la linea per un numero di volte specificato
"""
def update():
	global ns,tp,values,old_values,new_values
	dt=0.3
	c=1
	dx=1
	tau=(c*dt/dx)
	sqtau=tau*tau
	for i in range(1, ns+1):
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
Funzione che stampa i valori
"""
def print_values():
	global values,tp
	for i in range(1,tp+1):
		print("%6.4f " %(values[i]), end=" ")
		if(i % 10 == 0):
			print("\n")

"""
Funzione che salva i risultati in in un file txt e
esegue il plot dell'onda.
"""
def save_result():
	global values,tp
	result=np.zeros(tp)
	result=values[1:tp+1]
	path="res/wawe.txt"
	np.savetxt(path,result)

def plot_wave():
	global values,tp,ns
	time=np.arange(1,tp+1,1)
	amplitude=values[1:tp+1]
	plt.title("Wave")
	plt.xlabel("Position")
	plt.ylabel("Amplitude")
	plt.grid(True, which='both')
	plt.axhline(y=0, color='k')
	plt.plot(time,amplitude)
	plt.show()


def main():
	print("Inizio versione seriale dell'equazione d'onda...\n")
	init_param()
	print("Inizializzazione dei punti sull'onda...\n")
	start_time = pc()
	create_line()
	print("Aggiornamento di tutti i valori per ogni istante di tempo...\n")
	update()
	end_time=pc()-start_time
	print("Stampa dei risultati finali...\n")
	print_values()
	plot_wave()
	save_result()
	print("Eseguito in {} s ".format(end_time))
	exit(0)


if __name__ == "__main__":
    main()

