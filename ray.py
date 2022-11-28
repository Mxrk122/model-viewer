import OpenGL.GL as gl
import numpy as np
import random

class Raycaster(object):

  ip = []

  def __init__(self, width, height, cell_size) -> None:
    self.width = width
    self.height = height
    self.cell_size = cell_size
  
  def setInitialLife(self, life = None):
    if life == None:
      # Si no se ingresa nada tener un grid random
      for y in range(40):
        row = []
        for x in range(40):
          number = random.random()
          if number >= 0.9:
            row.append(1)
          else:
            row.append(0)
        self.ip.append(row)
    else:
      self.ip = life

  # Dibujar un pixel con Opengl
  def pixel(self, x, y, color):
    gl.glEnable(gl.GL_SCISSOR_TEST)
    gl.glScissor(x, y, 10, 10)
    gl.glClearColor(*color)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glDisable(gl.GL_SCISSOR_TEST)

  # Inicialiar el juego
  def create_life(self):

    # Lista inicial de casillas del juego.
    initial_positions = [[0 for x in range(self.width)] for y in range(self.height)]

    # Intercambio y colocación de células en las casillas determinadas.
    y = 0
    for row in self.ip:
      # Encontrar los numeros 1 y colocarlos en el array correspondiente
      x = 0
      for cell in row:
        if cell == 1:
          initial_positions[y][x] = cell
        else:
          pass
        x += 1
      y += 1

    # Retorno del "tablero" inicial.
    return initial_positions

  # Función para actualizar el estado del juego.
  def update(self, current_state, living_cell_color, bg_color):

    # Generar el proximo estado
    nxt = [[0 for x in range(len(current_state[0]))]
    for y in range(len(current_state))]

    # Iteración sobre el estado a construir.
    for i in range(len(nxt)):
      for j in range(len(nxt[0])):

        # Encontrar coordendas en la pantalla
        x = j * self.cell_size
        y = i * self.cell_size
        prox_cells = []
        neighbors = []

        # Celdas cercanas a cada 1 y creacion de la matriz de cada 1
        celula = current_state[i][j]

        # PErimetro de la celula
        try:
          prox_cells.append(current_state[(i - 1)])
          prox_cells.append(current_state[(i)])
          prox_cells.append(current_state[(i + 1)])
          prox_cells.append(current_state[(i + 2)])
        except:
          pass

        # Analizar las celulas proximas a la actual
        try:
          for row in prox_cells:
            n = []
            n.append(row[j - 1])
            n.append(row[j])
            n.append(row[j + 1])
            n.append(row[j + 2])
            neighbors.append(n)
        except:
          pass

        sum_prox_cells = sum([sum(row) for row in neighbors])
        neighbor_count = sum_prox_cells - celula

        # Añadir los 1 segun el caso
        if ((current_state[i][j] == 1) and ((neighbor_count < 2) or (neighbor_count > 3))):
          paint_color = bg_color
        elif ((current_state[i][j] == 1) and (2 <= neighbor_count <= 3)) or ((current_state[i][j] == 0) and (neighbor_count == 3)):
          nxt[i][j] = 1
          paint_color = bg_color

        
        if current_state[i][j] == 1:
          pass
        else:
          paint_color = living_cell_color

        self.pixel(x, y, paint_color)

    # Retorno del nuevo estado creado.
    return nxt