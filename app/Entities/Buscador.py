class Buscador:

    @staticmethod
    def buscar_dependencia(dependencia, dependencias):
        for dependenciaActual in dependencias:
            if sorted(dependencia.atributos_implicado) == sorted(dependenciaActual.atributos_implicado) and \
                    sorted(dependencia.atributos_implicante) == sorted(dependenciaActual.atributos_implicante):
                return True

        return False
