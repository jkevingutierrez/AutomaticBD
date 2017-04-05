class Relacion:

    def __init__(self, atributos, dependencias):
        self.atributos = sorted(atributos)
        self.dependencias = dependencias

    def validar_atributos(self):
        for dependencia in self.dependencias:
            for atributo in dependencia.implicado:
                if atributo not in self.atributos:
                    return atributo
            for atributo in dependencia.implicante:
                if atributo not in self.atributos:
                    return atributo

        return True
