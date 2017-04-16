from app.Entities.ListHelper import ListHelper


class Buscador:
    @staticmethod
    def buscar_dependencia(dependencia, dependencias):
        for dependencia_actual in dependencias:
            if ListHelper.son_iguales(dependencia.implicado, dependencia_actual.implicado) and \
                    ListHelper.son_iguales(dependencia.implicante, dependencia_actual.implicante):
                return True

        return False
