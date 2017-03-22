from app.Entities.DependenciaFuncional import DependenciaFuncional
from app.Entities.RT import RT


class ConversorART:
    def transformar(self, j):
        dependencias = []
        variables = []
        dependenciasFuncionales = []

        if 'variables' in j:
            variables = j['variables']
        if 'dependencias' in j:
            dependencias = j['dependencias']

        for dependencia in dependencias:
            if 'implicante' in dependencia and 'implicado' in dependencia:
                dependenciaFuncional = DependenciaFuncional(dependencia['implicante'], dependencia['implicado'])
                dependenciasFuncionales.append(dependenciaFuncional)

        rt = RT(variables, dependenciasFuncionales)
        return rt
