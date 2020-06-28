import heapq
import random
import math
import sys
from grafo import Grafo
from cola import Cola
COMANDOS = ['similares','recomendar','camino','centralidad','distancias','estadisticas','comunidades','salir']
CANTIDAD_RECORRIDOS = 100
LARGO_RECORRIDO = 100
RECORRIDOS_COMUNIDADES = 10



'''************** FUNCION PRINCIPAL ************** '''	

def main():
	if len(sys.argv) != 2:
		print('cantidad de parametros incorrecta')
		return ValueError
	try:
		marvel = cargar_grafo(sys.argv[1])
	except IOError:
		print('Se ha producido un error al buscar/leer el archivo')
	menu_principal()
	while True :
		opcion = pedir_opcion()
		comando,parametros = validar_opcion(opcion)	
		ejecutar_comando(comando,parametros,marvel)


''' ********* FUNCIONES AUXILIARES  *********** '''		
		
def cargar_grafo(ruta):
	with open (sys.argv[1]) as archivo:
		linea = archivo.readline()
		ref = linea.split()
		cant_pers = int(ref[1])
		dicc_aux={}
		grafo = Grafo()
		for i in range(cant_pers):
			linea = archivo.readline()
			cadena = linea.split()
			vertice,personaje = cadena[0],' '.join(cadena[1:])
			dicc_aux[vertice]=personaje[1:-1]
			grafo[personaje[1:-1]] = True
		archivo.readline()
		linea = archivo.readline()
		while(linea != ''):
			arista = linea.split()
			pers1,pers2= dicc_aux[arista[0]],dicc_aux[arista[1]]
			grafo.agregar_arista(pers1,pers2,int(arista[2]))
			linea = archivo.readline()
		return grafo

def pedir_opcion():
	return input('> ').lower()

def menu_principal():
	print("Welcome to Wachenchauzer Studios!")
	print("\n        Menu principal        \n")
	print("-similares (personaje, cantidad)")
	print("-recomendar (personaje, cantidad)")
	print("-camino (personaje1, personaje2)")
	print("-centralidad (cantidad)")
	print("-distancias (personaje)")
	print("-estadisticas")
	print("-comunidades")
	print("-salir")
	
def validar_opcion(opcion):
	while(len(opcion)<5):
		print('Comando invalido ingrese de nuevo')
		opcion  = pedir_opcion()
	datos = opcion.split()
	while(datos[0] not in COMANDOS):
		print('El comando ingresado no es correcto')
		datos = pedir_opcion().split()
	return datos[0],' '.join(datos[1:])
		 
def ejecutar_comando(comando,parametros,grafo):
	if (comando == COMANDOS[0]):
		similares(grafo,parametros)
	elif(comando == COMANDOS[1]):
		recomendar(grafo,parametros)
	elif(comando == COMANDOS[2]):
		camino(grafo,parametros)
	elif(comando == COMANDOS[3]):
		centralidad(grafo,parametros)
	elif(comando == COMANDOS[4]):
		distancias(grafo,parametros)
	elif(comando == COMANDOS[5]):
		estadisticas(grafo,parametros)
	elif(comando == COMANDOS[6]):
		comunidades(grafo)
	else:
		sys.exit(0)		
	
def similares(grafo,parametros):
	verificacion = verif_param(grafo,parametros)
	if not verificacion:
		return
	pers,cant_simil = verificacion
	lista_aux = obtener_personajes_recorr(grafo,pers,cant_simil)
	heap_simil = []
	cont=0
	for personaje,cant in lista_aux:
		if(cont==cant_simil+1):
			if(heap_simil[0][0]<cant):
				heapq.heapreplace(heap_simil,(cant,personaje))
		else:
			heapq.heappush(heap_simil,(cant,personaje))
			cont+=1
	imprimir_recom_simil(heap_simil,pers,cont)
	return

def recomendar(grafo,parametros):
	verificacion = verif_param(grafo,parametros)
	if not verificacion:
		return
	pers,cant_simil = verificacion
	lista_aux = obtener_personajes_recorr(grafo,pers,cant_simil)
	heap_simil = []
	cont=0
	lista_ady = grafo.adyacentes(pers)
	for personaje,cant in lista_aux:
		if personaje in lista_ady:
			continue
		else:
			if(cont==cant_simil+1):
				if(heap_simil[0][0]<cant):
					heapq.heapreplace(heap_simil,(cant,personaje))
			else:
				heapq.heappush(heap_simil,(cant,personaje))
				cont+=1
	imprimir_recom_simil(heap_simil,pers,cont)
	return

def camino(grafo,parametro):
	lista_aux = parametro.split(',')
	if(len(lista_aux)!=2):
		print('cantidad de parametros incorretos')
		return None
	partida = lista_aux[0].upper().strip()
	llegada = lista_aux[1].upper().strip()
	if not partida in grafo or not llegada in grafo:
		print('parametros invalidos')
		return None
	recorrido = grafo.camino_minimo(partida,llegada)
	imprimir_camino(partida,llegada,recorrido)
	return

def centralidad(grafo,parametros):
	if (not parametros.isdigit()):
		print('parametros invalidos, ingrese como parametro un numero entero')
		return
	cantidad_personajes = int(parametros)
	cantidad_recorridos = int(len(grafo)/2)
	dicc = {}
	for i in range(cantidad_recorridos):
		recorrido = grafo.random_walk(LARGO_RECORRIDO,None)
		for pers in recorrido:
			if not pers in dicc:
				dicc[pers] = 1
			else:
				dicc[pers] += 1
	lista = dicc.items()
	heap_min = []
	cont=0
	for pers,cant in lista:
		if(cont==cantidad_personajes):
			if(heap_min[0][0]<cant):
				heapq.heapreplace(heap_min,(cant,pers))
		else:
			heapq.heappush(heap_min,(cant,pers))
			cont+=1
	imprimir_centralidad(heap_min)
	return

def estadisticas(grafo,parametros):
	if(parametros):
		print("el comandos estadisticas no recibe parametros")
		return
	cant_vertices = len(grafo)
	cant_aristas = grafo.obtener_cantidad_aristas()
	promedio_grado = calcular_promedio_grado(grafo)
	desvio_estandar = calcular_desvio_estandar(grafo,promedio_grado)
	densidad_grafo = calcular_densidad_grafo(grafo)
	resultados= (cant_vertices,cant_aristas,promedio_grado,desvio_estandar,densidad_grafo)
	imprimir_estadisticas(resultados)
	return
	
def calcular_desvio_estandar(grafo,promedio):
	suma = 0
	for vertice in grafo:
		grado =len(grafo.adyacentes(vertice))
		suma+=pow(grado-promedio,2)
	return math.sqrt(suma/(len(grafo)-1))
		
def calcular_promedio_grado(grafo):
	total_grado = 0
	for vertice in grafo:
		grado =len(grafo.adyacentes(vertice))
		total_grado+= grado
	return (total_grado/len(grafo))
	
def calcular_densidad_grafo(grafo):
	cant_vertices = len(grafo)
	cant_aristas = grafo.obtener_cantidad_aristas()
	return (2*cant_aristas)/(cant_vertices*(cant_vertices-1))
	
def imprimir_recom_simil(heap,pers,cont):
	while(cont!=1):
		if(heap[0][1]!=pers):
			print(heapq.heappop(heap)[1])
			cont-=1
		else:
			heapq.heappop(heap)
	return

def imprimir_camino(partida,llegada,recorrido):
	if not recorrido:
		print('No hay camino posible entre {} y {}'.format(partida,llegada))
		return
	if(len(recorrido)==1 and recorrido[0]==partida):
		print('El camino es directo entre {} y {}'.format(partida,llegada))
		return
	print(' {} ->'.format(partida),end='')
	for personaje in recorrido[::-1]:
		print(' {} ->'.format(personaje),end='')
	print(' {} '.format(llegada))
	return
		
def imprimir_estadisticas(resultados):
	print('Cantidad de vértices: {:d}'.format(resultados[0]))
	print('Cantidad de aristas: {:d}'.format(resultados[1]))
	print('Promedio del grado de cada vértice: {:.4}'.format(resultados[2]))
	print('Desvio estandar del grado de cada vertice: {:.4}'.format(resultados[3]))
	print('Densidad del grafo: {:.4}'.format(resultados[4]))
	return
	
def imprimir_centralidad(heap):
	lista =[]
	while(heap):
		cant,pers = heapq.heappop(heap)
		lista.append(pers)
	for personaje in lista[::-1]:	
		print(personaje)
	return
		
	
def verif_param(grafo,parametros):
	lista_aux = parametros.split(',')
	if(len(lista_aux)!=2):
		print('cantidad de parametros incorretos')
		return None
	pers = lista_aux[0].upper()
	cant_simil = lista_aux[1].split()
	if (not pers in grafo or not (cant_simil[0]).isdigit()):
		print('parametros invalidos')
		return None
	return (pers,int(cant_simil[0]))
	
def obtener_personajes_recorr(grafo,pers,cantidad):
	dicc_simil = {}
	for i in range(CANTIDAD_RECORRIDOS):
		recorrido = grafo.random_walk(LARGO_RECORRIDO,pers)
		for personaje in recorrido:
			if not personaje in dicc_simil:
				dicc_simil[personaje] = 1
			else:
				dicc_simil[personaje] += 1
	return dicc_simil.items()

def distancias_ady(grafo,origen,visitados,orden,dicc_dist):
	q = Cola()
	q.encolar(origen)
	visitados[origen] = True
	while not q.esta_vacia():
		v = q.desencolar()
		ady = list(grafo.adyacentes(v))
		for w in ady:
			if w not in visitados:
				visitados[w] = True
				orden[w] = orden[v] + 1
				if not orden[w] in dicc_dist:
					dicc_dist[orden[w]] = 1
				else:
					dicc_dist[orden[w]] += 1
				q.encolar(w)

def	distancias(grafo,personaje):
	'''dado un personaje, obtener la cantidad de personajes que se 
	encuentran a cada una de las distancias posibles, considerando las 
	distancias como la cantidad de saltos (no tenemos en cuenta los 
	eventuales pesos de las aristas del grafo).'''
	personaje = personaje.upper()
	visitados = {}
	dicc_dist = {}
	orden = {}
	if not personaje in list(grafo.obtener_vertices()):
		print("Error en el personaje...")
		return KeyError
	orden[personaje] = 0	
	distancias_ady(grafo,personaje,visitados,orden,dicc_dist)
	lista_distancias= dicc_dist.items()
	for dist,cant in lista_distancias:
		print("Distancia {}: {}".format(dist,cant))

def swap(lista,i,j):
	lista[i],lista[j] = lista[j],lista[i]	

def inicializar_etiquetas(personajes):
	etiquetas = {}
	cant = 0
	for personaje in personajes:
		 etiquetas[personaje] = cant
		 cant+=1
	return etiquetas

def mezclar_orden(lista):
	for x in range(len(lista)):
		swap(lista,x,random.randrange(len(lista)))

def mayor_frecuencia(ady,etiquetas):
	frecuencia = {}
	for clave in ady:
		etiqueta = etiquetas[clave]
		freq_ant = frecuencia.get(etiqueta,0)
		frecuencia[etiqueta] = freq_ant + 1
	
	freq_max = max(list(frecuencia.values()))
	for etiqueta in frecuencia:
		if frecuencia[etiqueta] == freq_max:
			return etiqueta

def obtener_comunidades(etiquetas):
	dicc_comunidades = {}
	etiqueta = list(etiquetas.values())
	for valor in etiqueta:
		dicc_comunidades[valor] = []
	for personaje in etiquetas:
		dicc_comunidades[etiquetas[personaje]].append(personaje)
	return dicc_comunidades

def comunidades(grafo):
	'''Nos permite mostrar las comunidades que se encuentren en la red.'''
	dicc_etiquetas = inicializar_etiquetas(list(grafo.obtener_vertices()))
	camino_aleatorio = list(grafo.obtener_vertices())
	mezclar_orden(camino_aleatorio)
	for comunidad in range(RECORRIDOS_COMUNIDADES):
		for personaje in camino_aleatorio:
			dicc_etiquetas[personaje] = mayor_frecuencia(list(grafo.adyacentes(personaje)),dicc_etiquetas)
		mezclar_orden(camino_aleatorio)
	dicc_comunidades = obtener_comunidades(dicc_etiquetas)	
	lista_comunidades = dicc_comunidades.items()
	for comunidad,miembros in lista_comunidades:
		if(len(miembros)<4 or len(miembros)>1000):
			continue
		print("")
		print("Cantidad integrantes: {}".format(len(miembros)))
		print("Integrantes:",end = " ")
		cant_miembros = len(miembros)
		for i in range(cant_miembros):
			if not i == cant_miembros-1:
				print(miembros[i],end = ", ")
			else:
				print(miembros[i])
main()	
