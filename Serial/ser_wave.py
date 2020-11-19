"""
Serial Concurrent Wave Equation - Python Version
"""
import numpy as np
from numpy import pi
import os


MAXP=10000
MAXSTEPS=1000
MINP=20

values=np.zeros(MAXP+2) #valori al tempo t
old_values=np.zeros(MAXP+2) #valori al tempo (t-dt)
new_values=np.zeros() # valori al tempo (t+dt)

def init_param():
	ns=0;
	tp=0;
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

	print("Numero di punti scelti: %d , numero di steps: %d"(tp,ns))

def create_line():
	f=2 * pi
	k=0.0
	tmp = tp-1

def main():
	init_param()

main()

x=np.zeros(10)
for i in range(10):
	x[i]=i
x
