# Librerías importantes para el desarrollo del raycaster.
import OpenGL.GL as gl
import pygame
from color import *
from ray import *

# Medidas de la ventana del raycaster.
w = 600
h = 600
cell_size = 10

# Inicialización de la librería pygame.
pygame.init()

r = Raycaster(w, h, cell_size)
screen = pygame.display.set_mode((w, h), pygame.OPENGL | pygame.DOUBLEBUF)


# Variables necesarias para el juego
r.setInitialLife()
state = r.create_life()
playing = True

while (playing):
  for event in pygame.event.get():
    if (event.type == pygame.QUIT):
      playing = False

  gl.glClearColor(*background_color)
  gl.glClear(gl.GL_COLOR_BUFFER_BIT)

  # Cambio de estado hacia un nuevo estado del juego.
  state = r.update(state, background_color, px_color)

  # Flip del framebuffer de pygame.
  pygame.display.flip()