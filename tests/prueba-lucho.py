import cmd

class MiPrompt(cmd.Cmd):
	def __init__(self, un_parametro):
		self.mi_parametro = un_parametro
		self.prompt = "> "
		super().__init__()
	
	def do_saludar(self, parametro):
		print ("Hola " + parametro)
	
	def do_sumar(self, parametro):
		parametro = parametro.split(',')
		
		a = int(parametro[0])
		b = int(parametro[1])
		
		print("La suma es " + str(a+b))
	
	def do_mostrar_param(self, parametro):
		print("El parametro inicial es " + self.mi_parametro)

	def do_salir(self, parametro):
		raise SystemExit

def principal():
	
	miprompt = MiPrompt("1234")
	
	miprompt.cmdloop()


principal()
