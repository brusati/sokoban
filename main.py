import soko
import gamelib
from pila import Pila

DIMENSION_CELDA = 63
SALTO_DE_LINEA = "\n"
REINICIAR = "REINICIAR"
SALIR = "SALIR"
CONTINUAR = "CONTINUAR"
DESHACER = "DESHACER"
SOLUCION = "SOLUCION"

def copiar_niveles(ruta_archivo):
	"""
	Recibe la ruta de un archivo que contiene muchos niveles. Devuelve una lista con 
	todos los niveles que se encuentran en el archivo.
	"""
	niveles = []
	with open(ruta_archivo) as archivo:
		for linea in archivo:
			if "Level" in linea:
				nivel = []
			elif linea == SALTO_DE_LINEA:
				completar_lineas(nivel)
				niveles.append(nivel)
			elif "'" not in linea:
				nivel.append(linea.rstrip())
	return niveles

def copiar_teclas(ruta_archivo):
	"""
	Recibe la ruta de un archivo que contiene la referencia a las teclas. Devuelve un
	diccionario en el que las claves son las teclas y sus valores correspondientes son
	las acciones.
	"""
	teclas = {}
	with open(ruta_archivo) as archivo:
		for linea in archivo:
			if linea == SALTO_DE_LINEA:
				continue
			tecla, referencia = linea.rstrip().split("=")
			teclas[tecla.rstrip()] = referencia.lstrip(" ")
	return teclas

def completar_lineas(grilla):
	"""
	Recibe una grilla en forma de lista. Si las filas de la grilla no tienen la
	misma cantidad de columnas, modifica la grilla para que ahora todas las filas
	tengan la misma longitud.  
	"""
	ancho = 0
	for fila in grilla:
		if len(fila) > ancho:
			ancho = len(fila)
	for i, fila in enumerate(grilla):
		incompletas = ancho - len(fila)
		grilla[i] = fila + (" " * incompletas)

def obtener_grilla(nivel, niveles):
	"""Recibe un nivel y devuelve la grilla correspondiente a ese nivel"""
	grilla = niveles[nivel]
	grilla = soko.crear_grilla(grilla)
	return grilla

def dibujar_grilla(grilla):
	"""Recibe una grilla y dibuja cada celda de la grilla"""
	ancho, largo = soko.dimensiones(grilla)
	gamelib.resize(DIMENSION_CELDA * ancho, DIMENSION_CELDA * largo)
	gamelib.draw_begin()
	for f in range(largo):
		fila = DIMENSION_CELDA * f
		for c in range(ancho):
			columna = DIMENSION_CELDA * c
			gamelib.draw_image('img/ground.gif', columna, fila)
			if soko.hay_caja(grilla, c, f):
				gamelib.draw_image('img/box.gif', columna, fila)
			if soko.hay_objetivo(grilla, c, f):
				gamelib.draw_image('img/goal.gif', columna, fila)
			if soko.hay_jugador(grilla, c, f):
				if soko.hay_objetivo(grilla, c, f):
					gamelib.draw_image('img/player_2.gif', columna, fila)
				else:
					gamelib.draw_image('img/player.gif', columna, fila)
			if soko.hay_pared(grilla, c, f):
				gamelib.draw_image('img/wall.gif', columna, fila)
	gamelib.draw_end()

def pedir_tecla(teclas):
	"""
	Recibe una diccionario cuyas claves son las teclas v??lidas y sus valores son
	las acciones correspondientes a las teclas. Espera que el usuario presione una 
	tecla. Devuelve la acci??n que le corresponde a la tecla presionada. 
	"""
	ev = gamelib.wait(gamelib.EventType.KeyPress)
	if not ev:
		return SALIR
	tecla_presionada = ev.key
	accion = teclas.get(tecla_presionada, CONTINUAR)
	return accion



def buscar_solucion(estado_inicial):
	"""
	Recibe el estado del juego y busca una soluci??n al mismo.
	Si encuentra una soluci??n devuelve True y una lista con los
	movimientos de dicha soluci??n. Caso contrario, devuelve False
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
	Recibe la nueva direcci??n y las direcciones anteriores.
	Concatena esta nueva direcci??n a las direcciones anteriores,
	devolviendo el resultado de dicha acci??n.
	"""
	acciones.apilar(direccion)
	return acciones

def backtrack(estado, visitados):
	"""
	Recibe el estado actual y una lista de los estados visitados.
	Si en dicho estado el juego est?? ganado, devuelve True y una lista
	vac??a. Caso contrario, analiza las posibles direcciones del jugador
	llamando recursivamente a esta funci??n en cada una de las direcciones.
	Si en alguna de las direcciones se encuentra una soluci??n, devuelve True
	y una pila de las acciones realizadas. En caso de que el juego no 
	se pueda solucionar devuelve False y None.
	"""
	direcciones = ((0, -1), (0, 1), (1, 0), (-1, 0))
	agregar(visitados, str(estado))
	if soko.juego_ganado(estado):
		return True, Pila()
	for direccion in direcciones:
		nuevo_estado = soko.mover(estado, direccion)
		if pertenece(visitados, str(nuevo_estado)):
			continue
		soluci??n_encontrada, acciones = backtrack(nuevo_estado, visitados)
		if soluci??n_encontrada:
			return True, concatenar(direccion, acciones)
	return False, None



def encontrar_solucion(grilla, solucion):
	"""
	Recibe la grilla actual y la pila 'soluci??n' (la cual se encuentra vac??a).
	Busca la soluci??n. En caso de que no haya soluci??n no realiza cambios. En cambio,
	si encuentra una soluci??n, apila cada uno de los movimientos a 'soluci??n'.
	"""
	hay_solucion, movimientos = buscar_solucion(grilla)
	gamelib.get_events() #elimina las teclas apretadas mientras se buscaba la soluci??n
	if hay_solucion:
		pila_auxiliar = Pila()
		while not movimientos.esta_vacia():
			pila_auxiliar.apilar(movimientos.desapilar())
		while not pila_auxiliar.esta_vacia():
			solucion.apilar(pila_auxiliar.desapilar())

def obtener_pista(solucion):
	"""
	Recibe la pila 'soluci??n' y devuelve la direcci??n correspondiente
	al pr??ximo movimiento.
	"""
	direccion = solucion.desapilar() 
	return direccion

def obtener_grilla_anterior(movimientos_realizados):
	"""
	Recibe los movimientos realizados y devuelve la grilla correspondiente
	al estado de juego anterior.
	"""
	grilla = movimientos_realizados.desapilar()
	return grilla

def guardar_movimiento(movimientos_realizados, grilla):
	"""Recibe los movimientos realizados y apila la grilla actual"""
	movimientos_realizados.apilar(grilla)

def dibujar_pensando(grilla):
	"""Dibuja en pantalla la grilla y la frase 'Pensando...'"""
	gamelib.draw_begin()
	dibujar_grilla(grilla)
	gamelib.draw_text("Pensando...", 55, 10)
	gamelib.draw_end()

def dibujar_pista_disponible(grilla):
	"""Dibuja en pantalla la grilla y la frase 'Pista disponible'"""
	gamelib.draw_begin()
	dibujar_grilla(grilla)
	gamelib.draw_text("Pista disponible", 70, 10)
	gamelib.draw_end()



def manejar_solucion(grilla, accion, solucion, movimientos_validos):
	"""
	Recibe la grilla, la pila 'solucion', la accion y los movimientos v??lidos.
	Si la accion es 'SOLUCION', en caso de que ya haya una soluci??n, obtiene
	una pista. Si no hay soluci??n, la busca. Adem??s, si la accion no es SOLUCION
	pero la accion anterior s??, borra la soluci??n encontrada. Devuelve la pila
	'soluci??n' y la acci??n.
	"""
	if accion == SOLUCION:
		if solucion.esta_vacia():
			dibujar_pensando(grilla)
			try:
				encontrar_solucion(grilla, solucion)
			except RecursionError:
				accion = CONTINUAR
				return solucion, accion
			if not solucion.esta_vacia():
				accion = CONTINUAR
			else:
				accion = REINICIAR #si no hay soluci??n, reinicia el nivel
		else:
			movimientos_validos[SOLUCION] = obtener_pista(solucion)
	elif not solucion.esta_vacia():
		solucion = Pila()
	return solucion, accion

def manejar_deshacer(grilla, movimientos_realizados):
	"""
	Recibe la grilla y los movimientos realizados. Si hay movimientos
	anteriormente realizados, obtiene la grilla inmediatamente anterior 
	y la devuelve. Caso contrario, devuelve la misma grilla recibida.
	"""
	if not movimientos_realizados.esta_vacia():
		grilla = obtener_grilla_anterior(movimientos_realizados)
	return grilla

def manejar_reiniciar(grilla, movimientos_realizados, nivel, niveles):
	"""
	Recibe la grilla, los movimientos realizados, el nivel actual y la
	lista de niveles. Devuelve la grilla correspondiente a ese nivel y
	'limpia' los movimientos realizados.
	"""
	grilla = obtener_grilla(nivel, niveles)
	movimientos_realizados = Pila()
	return grilla, movimientos_realizados

def manejar_otro_caso(grilla, accion, movimientos_validos, movimientos_realizados):
	"""
	Recibe la grilla, la acci??n, los movimientos v??lidos, los movimientos realizados.
	Devuelve la grilla correspodiente luego de realizar la accion obtenida. Adem??s,
	si la grilla recibida es distinta de la nueva grilla, guarda ese estado en los 
	movimientos realizados.
	"""
	grilla_anterior = grilla
	movimiento = movimientos_validos[accion]
	grilla = soko.mover(grilla, movimiento)
	if not grilla_anterior == grilla:
		guardar_movimiento(movimientos_realizados, grilla_anterior)
	return grilla

def manejar_accion(grilla, accion, solucion, movimientos_realizados, nivel, niveles):
	"""
	Recibe la grilla, la accion, la pila 'solucion', los movimientos realizados, el nivel
	actual y la lista de niveles. Seg??n la accion recibida realiza acciones pertinentes.
	Devuelve la grilla, la accion, la pila 'solucion' y los movimientos realizados.
	"""
	movimientos_validos = {"NORTE": (0, -1), "SUR": (0, 1), "ESTE": (1, 0), "OESTE": (-1, 0), "CONTINUAR": (0,0)}
	solucion, accion = manejar_solucion(grilla, accion, solucion, movimientos_validos)	
	if accion == DESHACER:
		grilla = manejar_deshacer(grilla, movimientos_realizados)
	elif accion == REINICIAR:
		grilla, movimientos_realizados = manejar_reiniciar(grilla, movimientos_realizados, nivel, niveles)
	else:
		grilla = manejar_otro_caso(grilla, accion, movimientos_validos, movimientos_realizados)
	return grilla, accion, solucion, movimientos_realizados



def main():
	niveles = copiar_niveles("niveles.txt")
	teclas = copiar_teclas("teclas.txt")
	nivel = 0
	movimientos_realizados = Pila()
	solucion = Pila()
	grilla = obtener_grilla(nivel, niveles)
	while gamelib.is_alive():
		if soko.juego_ganado(grilla):
			gamelib.play_sound('win_sound.wav')
			movimientos_realizados = Pila()
			if nivel == len(niveles):
				gamelib.say("Ganaste!")
				break
			nivel += 1
			grilla = obtener_grilla(nivel, niveles)
		gamelib.title(f"Sokoban Nivel {nivel}")
		dibujar_grilla(grilla)
		if not solucion.esta_vacia():
			dibujar_pista_disponible(grilla)
		accion = pedir_tecla(teclas)
		if accion == SALIR:
			break
		grilla, accion, solucion, movimientos_realizados = manejar_accion(grilla, accion, solucion, movimientos_realizados, nivel, niveles)


gamelib.init(main)
