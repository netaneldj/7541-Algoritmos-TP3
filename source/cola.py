class _Nodo:
	def __init__(self, dato=None, prox=None):
		self.dato = dato
		self.prox = prox
	def __str__(self):
		return str(self.dato)

class Cola:
	def __init__(self):
		self.primero=None
		self.ultimo=None
	def __str__(self):
		impresion=""
		actual=self.primero
		while actual is not None:
			impresion+=str(actual)+" "
			actual=actual.prox
		return impresion
	def encolar(self,x):
		nuevo=_Nodo(x)
		if self.ultimo:
			self.ultimo.prox=nuevo
			self.ultimo=nuevo
		else:
			self.ultimo=nuevo
			self.primero=nuevo
	def desencolar(self):
		if self.primero is None:
			raise ValueError("La cola esta vacía")
		valor=self.primero.dato
		self.primero=self.primero.prox
		if not self.primero:
			self.ultimo=None
		return valor
	def esta_vacia(self):
		return self.primero is None	
