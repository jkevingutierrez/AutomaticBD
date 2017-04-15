import os
from django.conf import settings


class Archivo:
    def __init__(self, nombre='') -> object:
        if nombre is not None and nombre != '':
            self.nombre = nombre
            self.file = open(os.path.join(settings.BASE_DIR, self.nombre), "w+")
            self.file.close()

    def cambiar_archivo(self, nombre):
        self.nombre = nombre
        self.file = open(os.path.join(settings.BASE_DIR, self.nombre), "w+")
        self.file.close()

    def escribir(self, texto):
        self.file = open(os.path.join(settings.BASE_DIR, self.nombre), "a+")
        self.file.write(texto)
        self.file.close()

    @staticmethod
    def escribir_sobre_archivo_existente(nombre, texto):
        file = open(os.path.join(settings.BASE_DIR, nombre), "a+")
        file.write(texto)
        file.close()
