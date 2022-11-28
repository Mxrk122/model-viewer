import numpy as np

class ObjLoader(object):
    buffer = []

    def add_faces(self, value, destiny):
        for f in value:
            if f == 'f':
                continue
            else:
                destiny.append(int(f)-1)

    # Metodo para cargar el modelo
    def load_model(self, file):

        # Arrays para almacenar los valores del archivo
        vertex = []
        texture_vertex = []
        normal_vertex = []
        all_indices = []
        indices = []


        with open(file, 'r') as f:
            line = f.readline()
            while line:
                values = line.split()
                if values[0] == 'v':
                    vertex.append(float(values[1]))
                    vertex.append(float(values[2]))
                    vertex.append(float(values[3]))
                elif values[0] == 'vt':
                    texture_vertex.append(float(values[1]))
                    texture_vertex.append(float(values[2]))
                    texture_vertex.append(float(values[3]))
                elif values[0] == 'vn':
                    normal_vertex.append(float(values[1]))
                    normal_vertex.append(float(values[2]))
                    normal_vertex.append(float(values[3]))
                elif values[0] == 'f':
                    for value in values[1:]:
                        val = value.split('/')
                        self.add_faces(val, all_indices)
                        indices.append(int(val[0])-1)
                else:
                    pass

                line = f.readline()

        
        self.sort_buffer(all_indices, vertex, texture_vertex, normal_vertex)

        # Realizar una copia del buffer
        buffer = self.buffer.copy()
        self.buffer = []

        # Devolver el array de indices y vertices
        return np.array(indices, dtype='uint32'), np.array(buffer, dtype='float32')

    def sort_buffer(self, indices_data, vertices, textures, normals):
        for i, ind in enumerate(indices_data):
            if i % 3 == 0: # ordenar las coordenadas de vertices
                start = ind * 3
                end = start + 3
                self.buffer.extend(vertices[start:end])
            elif i % 3 == 1: # ordenar las coordenadas de vertices de textura
                start = ind * 2
                end = start + 2
                self.buffer.extend(textures[start:end])
            elif i % 3 == 2: # ordenar las coordenadas de vertices de normal
                start = ind * 3
                end = start + 3
                self.buffer.extend(normals[start:end])