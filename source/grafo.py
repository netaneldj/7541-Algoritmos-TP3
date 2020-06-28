visitar_nulo = lambda a,b,c,d: True
heuristica_nula = lambda actual,destino: 0
import random
import math
import heapq

class Grafo(object):
	'''Clase que representa un grafo. El grafo sera no dirigido, y puede no indicarsele peso a las aristas
	(se comportara como peso = 1). Implementado como "diccionario de diccionarios"'''
	def __init__(self,es_dirigido = False):
		'''Crea el grafo.'''
		self.vertices = {}
		self.cant_vertices = 0
		self.cant_aristas = 0
		self.dirigido = es_dirigido
	
	def __len__(self):
		'''Devuelve la cantidad de vertices del grafo'''
		return self.cant_vertices

	def __iter__(self):
		'''Devuelve un iterador de vertices, sin ningun tipo de relacion entre los consecutivos'''
		return iter(self.vertices)
		
	def __setitem__(self, id, valor):
		'''Agrega un nuevo vertice con el par <id, valor> indicado. ID debe ser de identificador unico del vertice.
		En caso que el identificador ya se encuentre asociado a un vertice, se actualizara el valor.'''
		if not id in self.vertices:
			self.vertices[id] = ({},valor)
		else:
			self.vertices[id] = (self.vertices[id][0],valor)
		self.cant_vertices += 1
	
	def __getitem__(self, id):
		'''Devuelve el valor del vertice asociado, del identificador indicado. Si no existe el identificador en el grafo, lanzara KeyError.'''
		if not id in self.vertices:
			return KeyError
		return self.vertices[id][1]
        
	def __contains__(self, id):
		''' Determina si el grafo contiene un vertice con el identificador indicado.'''
		return (id in self.vertices)
	
	def obtener_vertices(self):
		'''Devuelve una lista con los vertices del grafo'''
		return self.vertices.keys()
				
	def agregar_arista(self, desde, hasta, peso = 1):
		'''Agrega una arista que conecta los vertices indicados. 
        Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            - Peso: valor de peso que toma la conexion. Si no se indica, valdra 1.'''
		
		if not desde in self.vertices or not hasta in self.vertices:
			return KeyError
		if(self.dirigido):
			self.vertices[desde][0][hasta] = peso
		else:
			self.vertices[desde][0][hasta] = peso
			self.vertices[hasta][0][desde] = peso
		self.cant_aristas += 1
		
	def borrar_arista(self, desde, hasta):
		'''Borra una arista que conecta los vertices indicados. 
        Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
           En caso de no existir la arista, se lanzara ValueError.'''
		
		if not desde in self.vertices or not hasta in self.vertices:
			return KeyError
		if(self.dirigido):	
			if not desde in self.vertices[hasta]:
				return ValueError
			self.vertices[desde][0].pop(desde)
		else:
			self.vertices[hasta][0].pop(desde)
			self.vertices[desde][0].pop(hasta)
		self.cant_aristas -= 1
	
	def obtener_cantidad_aristas(self):
		'''Obtiene la cantidad de aristas dentro del grafo '''
		return self.cant_aristas
			
	def obtener_peso_arista(self, desde, hasta):
		'''Obtiene el peso de la arista que va desde el vertice 'desde', hasta el vertice 'hasta'. 
		Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            En caso de no existir la union consultada, se devuelve None.
        '''
		if not desde in self.vertices or not hasta in self.vertices:
			return KeyError
			
		if not desde in self.vertices[hasta]:
			return None
		return self.vertices[desde][hasta]
	
	def adyacentes(self, id):
		'''Devuelve una lista con los vertices (identificadores) adyacentes al indicado. 
		   Si no existe el vertice, se lanzara KeyError'''
		if not id in self.vertices:
			return KeyError
		return self.vertices[id][0].keys()
	
	def camino_minimo(self, origen, destino):
		'''Devuelve el recorrido minimo desde el origen hasta el destino, aplicando el algoritmo de Dijkstra. 
		Parametros:
            - origen y destino: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
        Devuelve:
            - Listado de vertices (identificadores) ordenado con el recorrido, incluyendo a los vertices de origen y destino. 
            En caso que no exista camino entre el origen y el destino, se devuelve None.'''
		if not origen in self.vertices or not destino in self.vertices:
			raise KeyError
		visitados = {}
		padre = {}
		dist = {}		
		heap = []
		camino = []
		for vert in self.vertices:
			dist[vert]=math.inf
			padre[vert]=None
			visitados[vert]=False
		dist[origen] = 0
		heapq.heappush(heap,(dist[origen],origen))
		while heap:
			u,v = heapq.heappop(heap)
			visitados[v]=True
			if(v==destino):
				break
			adyacentes = self.adyacentes(v)
			for ady in adyacentes:
				if not visitados[ady] and dist[ady] > dist[v] + (1/self.vertices[v][0][ady]):
					dist[ady] = dist[v] + (1/self.vertices[v][0][ady])
					padre[ady] = v
					heapq.heappush(heap,(dist[ady],ady))
		if(dist[destino]==math.inf):
			return None
		vertice = padre[destino]
		if(vertice==origen):
			camino.append(vertice)
		while(vertice!=origen):
			camino.append(vertice)
			vertice = padre[vertice]
		return camino

	def random_walk(self, largo, origen = None):
		''' Devuelve una lista con un recorrido aleatorio de grafo.
            Parametros:
                - largo: El largo del recorrido a realizar. Si el numero no es valido devuelve ValueError.
                - origen: Vertice (id) por el que se debe comenzar el recorrido. Si origen = None, se comenzara por un vertice al azar.
            Devuelve:
                Una lista con los vertices recorridos, en el orden del recorrido.'''
		if largo<1:
			return ValueError
		recorrido =[]
		if not origen:
			lista = list(self.vertices.keys())
			origen = random.choice(lista)
		for i in range(largo):
			adyacente = vertice_aleatorio(self.vertices[origen][0])
			recorrido.append(adyacente)
			origen = adyacente
		return recorrido



''' ********* FUNCIONES AUXILIARES  *********** '''

		
def vertice_aleatorio(aristas):
	'''Aristas es un diccionario de pesos, clave vértice vecino, valor el peso.'''
	total = sum(aristas.values())
	rand = random.uniform(0, total)
	acum = 0
	for vertice, peso_arista in aristas.items():
		if acum + peso_arista >= rand:
			return vertice
		acum += peso_arista		
		
