import random
import heapq
from grafo import Grafo
'''

lista=[8,4,3,1,5,6,7,2,9]
#print(max(lista))
heapq.heapify(lista)
for elemento in lista:
	print(elemento)

lista2=[(1,"fer"),(20,"neta"),(12,"mati"),(7,"agus"),(13,"flor")]
heapq.heapify(lista2)
for elemento in lista2:
	print(elemento[1])

	
lista3=[("fer",1),("neta",20),("mati",12),("agus",7),("flor",13)]
heapq.heapify(lista3)
for elemento in lista3:
	print(elemento[0])	
print(min(lista3))	


for clave,valor in dicci.items():
	heapq.heapush((lista4,(valor,clave)))
	
	'''
dicc={}
dicc["neta"]=20
dicc["fer"]=1
dicc["agus"]=7
dicc["mati"]=12
dicc["flor"]=13

lista_tuplas=dicc.items()
heap=[]
for clave,valor in lista_tuplas:
		heapq.heappush(heap,(-valor,clave))

for i in range(5):
	print(heapq.heappop(heap)[1])
	
print(len(dicc))
