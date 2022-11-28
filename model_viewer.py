import numpy
import random
import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import glm
import objloader as ol

pygame.init()

screen = pygame.display.set_mode(
    (1600, 1200),
    pygame.OPENGL | pygame.DOUBLEBUF
)
# Codigo apra el visor
vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 vertexColor;

uniform mat4 amatrix;

out vec3 ourColor;


void main()
{
    gl_Position = amatrix * vec4(position, 1.0f);
    ourColor = vertexColor;

}
"""

fragment_shader = """
#version 460

layout (location = 0) out vec4 fragColor;

uniform vec3 color;


in vec3 ourColor;

void main()
{
    // fragColor = vec4(ourColor, 1.0f);
    fragColor = vec4(color, 1.0f);
}
"""



# Uso de shaders
compiled_vertex_shader = compileShader(vertex_shader, GL_VERTEX_SHADER)
compiled_fragment_shader = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
shader = compileProgram(
    compiled_vertex_shader,
    compiled_fragment_shader
)

glUseProgram(shader)

#  segundo shader
vertex_shader2 = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 vertexColor;
uniform mat4 amatrix;
out vec3 ourColor;
void main()
{
    gl_Position = amatrix * vec4(position, 1.0f);
}
"""
fragment_shader2 = """
#version 460
layout (location = 0) out vec4 fragColor;
uniform vec3 color;
in vec3 ourColor;
void main()
{
    fragColor = (vec4(color, 1.0f) / vec4(ourColor, 2.5f)) * 0.0004f;
    
}
"""
compiled_vertex_shader2 = compileShader(vertex_shader2, GL_VERTEX_SHADER)
compiled_fragment_shader2 = compileShader(fragment_shader2, GL_FRAGMENT_SHADER)
shader2 = compileProgram(
    compiled_vertex_shader,
    compiled_fragment_shader2
)


# Cargar modelo -> cargar vertices e informacion del modelo
Ol = ol.ObjLoader()
index, vinfo = Ol.load_model("nu.obj")
# cargando vertices
vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(GL_ARRAY_BUFFER, vinfo.nbytes, vinfo, GL_STATIC_DRAW)

# Cargar los indices de los vertices
index_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, index_buffer_object)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, index.nbytes, index, GL_STATIC_DRAW)

# Vertex array object
slots = 8
bytes = 4
glEnableVertexAttribArray(0)
glVertexAttribPointer(
    0,
    3,
    GL_FLOAT,
    GL_FALSE,
    slots * bytes,
    ctypes.c_void_p(0)
)

glVertexAttribPointer(
    1,
    3,
    GL_FLOAT,
    GL_FALSE,
    slots * bytes,
    ctypes.c_void_p(3 * 4)
)
glEnableVertexAttribArray(1)

# Funcion que genera la matriz de vision
def calculateMatrix(angle, another_angle):
    i = glm.mat4(1)
    translate = glm.translate(i, glm.vec3(0, -1.5, 0))
    rotate = glm.rotate(i + another_angle, glm.radians(angle), glm.vec3(0, 1, 0))
    scale = glm.scale(i, glm.vec3(0.15, 0.15, 0.15))

    model = translate * rotate * scale

    view = glm.lookAt(
        glm.vec3(0, 0, 5),
        glm.vec3(0, 0, 0),
        glm.vec3(0, 1, 0)
    )

    projection = glm.perspective(
        glm.radians(45),
        1600/1200,
        0.1,
        1000.0
    )

    amatrix = projection * view * model

    glUniformMatrix4fv(
        glGetUniformLocation(shader, 'amatrix'),
        1,
        GL_FALSE,
        glm.value_ptr(amatrix)
    )

glViewport(250, 200, 1200, 1000)



running = True

glClearColor(0, 0, 0, 0)

angle = 0
y_angle = 0
#Generacion de color
color1 = random.random()
color2 = random.random()
color3 = random.random()

color = glm.vec3(color1, color2, color3)

glUniform3fv(
    glGetUniformLocation(shader,'color'),
    1,
    glm.value_ptr(color)
)

while running:
    
    glClear(GL_COLOR_BUFFER_BIT)

    calculateMatrix(angle, y_angle)

    pygame.time.wait(50)

    glDrawArrays(GL_TRIANGLES, 0, len(index))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Moveset de la camara
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                angle -= 10
            if event.key == pygame.K_d:
                angle += 10
            if event.key == pygame.K_w:
                y_angle += 1
            if event.key == pygame.K_s:
                y_angle -= 1
            if event.key == pygame.K_r:
                color4 = 1
                color5 = 1
                color6 = 1

                color1 = glm.vec3(color4, color5, color6)

                glUniform3fv(
                    glGetUniformLocation(shader2,'color'),
                    1,
                    glm.value_ptr(color1)
                )
            if event.key == pygame.K_t:
                color4 = 0.1
                color5 = 1
                color6 = 1

                color1 = glm.vec3(color4, color5, color6)

                glUniform3fv(
                    glGetUniformLocation(shader,'color'),
                    1,
                    glm.value_ptr(color1)
                )
