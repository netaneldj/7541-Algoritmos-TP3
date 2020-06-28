import heapq
import random
import sys
from grafo import Grafo


def main():
	g=Grafo()
	g["fer"]={}
	g["fer"]["flor"]="hna"
	g["fer"]["fds"]="hno"
	g["fer"]["emilia"]="mama"
	g["fer"]["tony"]="papa"
	lista = g.adyacentes("fer")
	print(lista)
	if("fer" in g):
		print("esta fer")
	else:
		print("no esta fer")
		
main()
	
