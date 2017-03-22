import json
from django.views.generic import ListView
from django.views.generic.base import View
from django.http import JsonResponse, HttpResponseBadRequest
from app.Entities.ConversorART import ConversorART
from app.Entities.ConversorATexto import ConversorATexto
from app.Entities.Archivo import Archivo


class IndexView(ListView):
    template_name = "index.html"
    queryset = 'AutomaticBD'
    context_object_name = 'projectName'


class ServiceView(View):

    @staticmethod
    def get(request):
        to_json = {
            "key1": "value1",
            "key2": "value2"
        }
        return JsonResponse(to_json)

    @staticmethod
    def post(request, *args, **kwargs):
        separador = ', '

        conversor_art = ConversorART()
        conversor_texto = ConversorATexto()
        # print('Raw Data: "%s"' % request.META)
        to_json = json.loads(request.body)

        rt = conversor_art.transformar(to_json)

        variableInvalida = rt.validarVariables()

        if variableInvalida == True:
            archivo = Archivo('Recubrimiento.txt')
            archivo.escribir('RECUBRIMIENTO MÍNIMO\n')
            archivo.escribir('____________________\n\n')
            archivo.escribir('Modelo Original:\n')
            archivo.escribir('RT(t, l)=\n')
            archivo.escribir('\tt = [')
            archivo.escribir(separador.join(rt.t))
            archivo.escribir(']\n')
            archivo.escribir('\tl = [')
            archivo.escribir(separador.join(conversor_texto.transformarDependencias(rt.l)))
            archivo.escribir(']\n\n')

            l1 = rt.dependenciasElementales()
            texto_l1 = conversor_texto.transformarDependencias(l1)
            archivo.escribir('\tl1 = [')
            archivo.escribir(separador.join(texto_l1))
            archivo.escribir(']\n\n')

            l2 = rt.atributosExtranos()
            texto_l2 = conversor_texto.transformarDependencias(l2)
            archivo.escribir('\tl2 = [')
            archivo.escribir(separador.join(texto_l2))
            archivo.escribir(']\n\n')

            l3 = rt.dependenciasRedundantes()
            texto_l3 = conversor_texto.transformarDependencias(l3)
            archivo.escribir('\tl3 = [')
            archivo.escribir(separador.join(texto_l3))
            archivo.escribir(']\n\n')

            response = {
                'original' : to_json,
                'l1': [],
                'l2': [],
                'l3': []
            }

            for dependencia in l1:
                elem = {
                    'variablesImplicado': dependencia.variablesImplicado,
                    'variablesImplicante': dependencia.variablesImplicante
                }
                response['l1'].append(elem)

            for dependencia in l2:
                elem = {
                    'variablesImplicado': dependencia.variablesImplicado,
                    'variablesImplicante': dependencia.variablesImplicante
                }
                response['l2'].append(elem)

            for dependencia in l3:
                elem = {
                    'variablesImplicado': dependencia.variablesImplicado,
                    'variablesImplicante': dependencia.variablesImplicante
                }
                response['l3'].append(elem)

            return JsonResponse(response)

        return HttpResponseBadRequest('La variable "' + variableInvalida + '" no se encuentra definida')

        # response_json = json.dumps([ob.__dict__ for ob in l1], sort_keys=True)
        # return JsonResponse(response_json, safe=False)
