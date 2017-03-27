import os
from django.conf import settings


class Archivo:
    def __init__(self, nombre=None):
        if nombre is not None:
            self.nombre = nombre
            self.file = open(os.path.join(settings.BASE_DIR, self.nombre), "w+")
            self.file.close()

    def cambiarArchivo(self, nombre):
        self.nombre = nombre
        self.file = open(os.path.join(settings.BASE_DIR, self.nombre), "w+")
        self.file.close()

    def escribir(self, texto):
        self.file = open(os.path.join(settings.BASE_DIR, self.nombre), "a+")
        self.file.write(texto)
        self.file.close()

    def escribirSobreArchivoExistente(self, nombre, texto):
        self.file = open(os.path.join(settings.BASE_DIR, nombre), "a+")
        self.file.write(texto)
        self.file.close()
