class Archivo:
    def __init__(self, nombre=None):
        if nombre is not None:
            self.nombre = nombre
            self.file = open(self.nombre, "w+")
            self.file.close()

    def cambiarArchivo(self, nombre):
        self.nombre = nombre
        self.file = open(self.nombre, "w+")
        self.file.close()

    def escribir(self, texto):
        self.file = open(self.nombre, "a+")
        self.file.write(texto)
        self.file.close()

    def escribirSobreArchivoExistente(self, nombre, texto):
        self.file = open(nombre, "a+")
        self.file.write(texto)
        self.file.close()
