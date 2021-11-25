import soko
from pila import Pila

def buscar_solucion(estado_inicial):
	"""
	Recibe el estado del juego y busca una solución al mismo.
	Si encuentra una solución devuelve True y una lista con los
	movimientos de dicha solución. Caso contrario, devuelve False
	y None.
	"""
	visitados = set()
	return backtrack(estado_inicial, visitados)

def agregar(visitados, estado):
	"""
	Recibe un diccionario con los estados visitados y el estado actual.
	Devuelve ese mismo diccionario con el estado agregado.
	"""
	visitados.add(estado)

def pertenece(visitados, nuevo_estado):
	"""
	Recibe un diccionario con los estados visitados y el estado actual.
	Si el estado actual se encuentra dentro de los visitados devuelve True.
	Caso contrario, False.
	"""
	return nuevo_estado in visitados

def concatenar(direccion, acciones):
	"""
	Recibe la nueva dirección y las direcciones anteriores.
	Concatena esta nueva dirección a las direcciones anteriores,
	devolviendo el resultado de dicha acción.
	"""
	acciones.apilar(direccion)
	return acciones

def backtrack(estado, visitados):
	"""
	Recibe el estado actual y una lista de los estados visitados.
	Si en dicho estado el juego está ganado, devuelve True y una lista
	vacía. Caso contrario, analiza las posibles direcciones del jugador
	llamando recursivamente a esta función en cada una de las direcciones.
	Si en alguna de las direcciones se encuentra una solución, devuelve True
	y una lista de las acciones realizadas. En caso de que el juego no se pueda 
	solucionar devuelve False y None.
	"""
	direcciones = ((0, -1), (0, 1), (1, 0), (-1, 0))
	agregar(visitados, str(estado))
	if soko.juego_ganado(estado):
		pila = Pila()
		return True, pila
	for direccion in direcciones:
		nuevo_estado = soko.mover(estado, direccion)
		if pertenece(visitados, str(nuevo_estado)):
			continue
		solución_encontrada, acciones = backtrack(nuevo_estado, visitados)
		if solución_encontrada:
			return True, concatenar(direccion, acciones)
	return False, None

