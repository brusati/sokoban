PARED = "#"
CAJA = "$"
JUGADOR = "@"
OBJETIVO = "."
OBJETIVO_Y_CAJA = "*"
OBJETIVO_Y_JUGADOR = "+"
CELDA_VACIA = " "

def crear_grilla(desc):
    '''Crea una grilla a partir de la descripción del estado inicial.

    La descripción es una lista de cadenas, cada cadena representa una
    fila y cada caracter una celda. Los caracteres pueden ser los siguientes:

    Caracter  Contenido de la celda
    --------  ---------------------
           #  Pared
           $  Caja
           @  Jugador
           .  Objetivo
           *  Objetivo + Caja
           +  Objetivo + Jugador

    Ejemplo:

    >>> crear_grilla([
        '#####',
        '#.$ #',
        '#@  #',
        '#####',
    ])
    '''
    grilla = desc[:]
    return grilla

def dimensiones(grilla):
    '''Devuelve una tupla con la cantidad de columnas y filas de la grilla.'''
    return (len(grilla[0]), len(grilla))

def hay_pared(grilla, c, f):
    '''Devuelve True si hay una pared en la columna y fila (c, f).'''
    return grilla[f][c] == PARED

def hay_objetivo(grilla, c, f):
    '''Devuelve True si hay un objetivo en la columna y fila (c, f).'''
    return grilla[f][c] == OBJETIVO or grilla[f][c] == OBJETIVO_Y_JUGADOR or grilla[f][c] == OBJETIVO_Y_CAJA

def hay_caja(grilla, c, f):
    '''Devuelve True si hay una caja en la columna y fila (c, f).'''
    return grilla[f][c] == CAJA or grilla[f][c] == OBJETIVO_Y_CAJA

def hay_jugador(grilla, c, f):
    '''Devuelve True si el jugador está en la columna y fila (c, f).'''
    return grilla[f][c] == JUGADOR or grilla[f][c] == OBJETIVO_Y_JUGADOR

def juego_ganado(grilla):
    '''Devuelve True si el juego está ganado.'''
    for c in grilla:
      if OBJETIVO in c or OBJETIVO_Y_JUGADOR in c:
        return False
    return True

def mover(grilla, direccion):
    '''Mueve el jugador en la dirección indicada.

    La dirección es una tupla con el movimiento horizontal y vertical. Dado que
    no se permite el movimiento diagonal, la dirección puede ser una de cuatro
    posibilidades:

    direccion  significado
    ---------  -----------
    (-1, 0)    Oeste
    (1, 0)     Este
    (0, -1)    Norte
    (0, 1)     Sur

    La función debe devolver una grilla representando el estado siguiente al
    movimiento efectuado. La grilla recibida NO se modifica; es decir, en caso
    de que el movimiento sea válido, la función devuelve una nueva grilla.
    '''
    dx, dy = direccion
    fila_jugador, columna_jugador = obtener_posicion_jugador(grilla)
    if not es_valido(grilla, columna_jugador, dx, fila_jugador, dy):
        return grilla
    nueva_grilla = grilla[:]
    nueva_grilla[fila_jugador] = borrar_jugador(grilla, fila_jugador) 
    nueva_grilla[fila_jugador + dy] = agregar_jugador(nueva_grilla, columna_jugador + dx, fila_jugador + dy)
    if hay_caja(grilla, columna_jugador + dx, fila_jugador + dy):
        nueva_grilla[fila_jugador + dy * 2] = mover_caja(nueva_grilla, columna_jugador + dx * 2, fila_jugador + dy * 2)
    return crear_grilla(nueva_grilla)
  
def obtener_posicion_jugador(grilla): 
    '''Recibe una grilla y devuelve la fila y la columna en la que se encuentra el jugador'''
    for f in range(len(grilla)):
        for c in range(len(grilla[0])):
            if hay_jugador(grilla, c, f):
                return f, c

def es_valido(grilla, columna_jugador, dx, fila_jugador, dy):
    '''Recibe una grilla, la columna y fila del jugador y la dirección a la que se mueve. 
    Devuelve True si el movimiento es válido y False si no lo es'''
    if hay_pared(grilla, columna_jugador + dx, fila_jugador + dy):
        return False
    elif hay_caja(grilla, columna_jugador + dx, fila_jugador + dy):
        if hay_pared(grilla, columna_jugador + dx * 2, fila_jugador + dy * 2):
            return False
        elif hay_caja(grilla, columna_jugador + dx * 2, fila_jugador + dy * 2):
            return False
    return True

def borrar_jugador(grilla, fila_jugador):
    '''Recibe una grilla y la fila en la que está el jugador. Devuelve esa fila sin el jugador'''
    fila_creada = ""
    for i in range(len(grilla[0])):
        if hay_jugador(grilla, i, fila_jugador) and hay_objetivo(grilla, i, fila_jugador):
            fila_creada += OBJETIVO
        elif hay_jugador(grilla, i, fila_jugador):
            fila_creada += CELDA_VACIA
        else:
            fila_creada += grilla[fila_jugador][i]
    return fila_creada

def agregar_jugador(nueva_grilla, nueva_columna_jug, nueva_fila_jug):
    '''Recibe una grilla, la fila y la columna a la que se mueve el jugador. 
    Devuelve esa fila con el jugador.'''
    fila_creada = ""
    for i in range(len(nueva_grilla[0])):
        if i == nueva_columna_jug and hay_objetivo(nueva_grilla, nueva_columna_jug, nueva_fila_jug):
            fila_creada += OBJETIVO_Y_JUGADOR
        elif i == nueva_columna_jug:
            fila_creada += JUGADOR
        else:
             fila_creada += nueva_grilla[nueva_fila_jug][i]
    return fila_creada

def mover_caja(nueva_grilla, columna_siguiente, fila_siguiente):
    '''Recibe una grilla, la fila y la columna a la que se mueve la caja. 
    Devuelve esa fila con la caja en la nueva posicion.'''
    fila_creada = ""
    for i in range(len(nueva_grilla[0])):
        if i == columna_siguiente and hay_objetivo(nueva_grilla, columna_siguiente, fila_siguiente):
            fila_creada += OBJETIVO_Y_CAJA
        elif i == columna_siguiente:
            fila_creada += CAJA
        else:
            fila_creada += nueva_grilla[fila_siguiente][i]
    return fila_creada