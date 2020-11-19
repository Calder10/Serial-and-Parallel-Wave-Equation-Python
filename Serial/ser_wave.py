"""
Serial Concurrent Wave Equation - Python Version
"""
import numpy as np
from numpy import pi
import os


MAXP=1000
MAXSTEPS=1000
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
		tp=int(x)
		if ((tp<MINP) or (tp>MAXP)):
			print("Errore ! Inserire valori compresi tra %d e %d " %(MINP,MAXP))
		else:
			break
			os.system("clear")


	while(True):
		y=input("Inserisci il numero di time steps [1-%d]--->" %(MAXSTEPS))
		ns=int(y)
		if ((ns < 1) or (ns > MAXSTEPS)):
			print("Errore ! Inserire valori compresi tra 1 e %d " %(MAXSTEPS))
		else:
			break
			os.system("clear")

	print("Numero di punti scelti: %d , numero di steps: %d" %(tp,ns))


"""
Calcolo dei valori iniziali basati su una sinusoide
"""
def create_line():
	global tp,values,old_values
	f=2 * pi
	k=0.0
	tmp = tp-1
	for i in range(1,tp+1):
		x=k/tmp
		values[i]=np.sin(f * x)
		old_values[i]=values[i]
		k=k+1


def print_values():
	global values,tp,old_values
	for i in range(1,tp+1):
		print("%6.4f \t" %(values[i]), end=" ")
		if(i % 10 ==0):
			print("\n")

def main():
	init_param()
	create_line()
	print_values()

if __name__ == "__main__":
    main()

