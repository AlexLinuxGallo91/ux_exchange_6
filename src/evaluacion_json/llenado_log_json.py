from src.models.result_step import ResultStep
from src.evaluacion_json import constantes_json
from src.utils.temporizador import Temporizador
from src.utils.format_utils import FormatUtils


class EvaluacionStepsJson:

    # validacion para verificar el inicio de sesion correctamente
    @staticmethod
    def validacion_json_inicio_sesion(result_url,
                                      result_sesion,
                                      objeto_json):
        result_final = ResultStep()

        # valida el estatus de ambos steps
        if not result_url.validacion_correcta:
            result_final.mensaje_error = result_url.mensaje_error
            result_final.validacion_correcta = False
        elif not result_sesion.validacion_correcta:
            result_final.mensaje_error = result_sesion.mensaje_error
            result_final.validacion_correcta = False
        else:
            result_final.mensaje_error = result_sesion.mensaje_error
            result_final.validacion_correcta = True

        # establece el datetime de inicio
        result_final.datetime_inicial = result_url.datetime_inicial

        # establece el datetime final
        result_final.datetime_final = result_sesion.datetime_final

        # establece el tiempo total de la ejecucion de ambos steps
        result_final.tiempo_inicio_de_ejecucion = result_url.tiempo_inicio_de_ejecucion
        result_final.tiempo_fin_de_ejecucion = result_sesion.tiempo_fin_de_ejecucion

        # establece el tiempo total de ejecucion
        result_final.establecer_tiempo_de_ejecucion()

        objeto_json['steps'][0]['status'] = constantes_json.STATUS_CORRECTO if \
            result_final.validacion_correcta else constantes_json.STATUS_FALLIDO

        objeto_json['steps'][0]['output'][0]['output'] = result_final.mensaje_error

        objeto_json['steps'][0]['output'][0]['status'] = constantes_json.STATUS_CORRECTO if \
            result_final.validacion_correcta else constantes_json.STATUS_FALLIDO

        objeto_json['steps'][0]['start'] = result_final.datetime_inicial
        objeto_json['steps'][0]['end'] = result_final.datetime_final
        objeto_json['steps'][0]['time'] = result_final.tiempo_total_de_la_ejecucion

        return objeto_json

    # validacion para verificar el inicio de sesion correctamente
    @staticmethod
    def validacion_json_navegacion_carpetas(validacion_result, objeto_json):

        objeto_json['steps'][1]['status'] = constantes_json.STATUS_CORRECTO if \
            validacion_result.validacion_correcta else constantes_json.STATUS_FALLIDO

        objeto_json['steps'][1]['output'][0]['output'] = validacion_result.mensaje_error
        objeto_json['steps'][1]['output'][0]['status'] = constantes_json.STATUS_CORRECTO if \
            validacion_result.validacion_correcta else constantes_json.STATUS_FALLIDO

        objeto_json['steps'][1]['start'] = validacion_result.datetime_inicial
        objeto_json['steps'][1]['end'] = validacion_result.datetime_final
        objeto_json['steps'][1]['time'] = validacion_result.tiempo_total_de_la_ejecucion

        return objeto_json

    # validacion para verificar el inicio de sesion correctamente
    @staticmethod
    def validacion_json_cierre_sesion(validacion_result, objeto_json):

        objeto_json['steps'][2]['status'] = constantes_json.STATUS_CORRECTO if \
            validacion_result.validacion_correcta else constantes_json.STATUS_FALLIDO

        objeto_json['steps'][2]['output'][0]['output'] = validacion_result.mensaje_error
        objeto_json['steps'][2]['output'][0]['status'] = constantes_json.STATUS_CORRECTO if \
            validacion_result.validacion_correcta else constantes_json.STATUS_FALLIDO

        objeto_json['steps'][2]['start'] = validacion_result.datetime_inicial
        objeto_json['steps'][2]['end'] = validacion_result.datetime_final
        objeto_json['steps'][2]['time'] = validacion_result.tiempo_total_de_la_ejecucion

        return objeto_json

    @staticmethod
    def establecer_fecha_tiempo_de_inicio(objeto_json):
        objeto_json['start'] = Temporizador.obtener_fecha_tiempo_actual()
        return objeto_json

    @staticmethod
    def establecer_tiempo_de_finalizacion(objeto_json):
        objeto_json['time'] = Temporizador.obtener_tiempo_timer()
        objeto_json['end'] = Temporizador.obtener_fecha_tiempo_actual()

        return objeto_json

    @staticmethod
    def formateo_de_tiempos(objeto_json):
        for i in range(3):
            objeto_json['steps'][i]['time'] = FormatUtils.truncar_float_cadena(objeto_json['steps'][i]['time'])

        objeto_json['time'] = FormatUtils.truncar_float_cadena(objeto_json['time'])

        return objeto_json

    @staticmethod
    def formar_cuerpo_json(result_list, objeto_json, correo):

        # se establece el tiempo final de ejecucion
        objeto_json = EvaluacionStepsJson.establecer_tiempo_de_finalizacion(objeto_json)

        # validaciones de cada step
        objeto_json = EvaluacionStepsJson.validacion_json_inicio_sesion(
            result_list.result_validacion_ingreso_url,
            result_list.result_validacion_acceso_portal_owa,
            objeto_json)

        objeto_json = EvaluacionStepsJson.validacion_json_navegacion_carpetas(
            result_list.result_validacion_navegacion_carpetas, objeto_json)

        objeto_json = EvaluacionStepsJson.validacion_json_cierre_sesion(
            result_list.result_validacion_cierre_sesion, objeto_json)

        tiempo_inicio_de_sesion = objeto_json['steps'][0]['time']
        tiempo_navegacion_carpetas = objeto_json['steps'][1]['time']
        tiempo_cierre_de_sesion = objeto_json['steps'][2]['time']

        suma_total_tiempo = tiempo_inicio_de_sesion + tiempo_navegacion_carpetas + tiempo_cierre_de_sesion

        objeto_json['time'] = suma_total_tiempo

        bool_ingreso_sesion = objeto_json['steps'][0]['status'] == constantes_json.STATUS_CORRECTO
        bool_navegacion_carpetas = objeto_json['steps'][1]['status'] == constantes_json.STATUS_CORRECTO
        bool_cierre_sesion = objeto_json['steps'][2]['status'] == constantes_json.STATUS_CORRECTO

        # Verifica si todos los estatus fueron exitosos o faliidos
        objeto_json['status'] = constantes_json.STATUS_CORRECTO if bool_ingreso_sesion and \
            bool_navegacion_carpetas and bool_cierre_sesion else constantes_json.STATUS_FALLIDO

        # Establece el correo concatenandolo en cada ouput en el objeto JSON
        objeto_json['steps'][0]['output'][0]['name'] += ' : {}'.format(correo.correo)
        objeto_json['steps'][1]['output'][0]['name'] += ' : {}'.format(correo.correo)
        objeto_json['steps'][2]['output'][0]['name'] += ' : {}'.format(correo.correo)

        # Formatea los tiempos a doce decimales (con el fin de no notificar con notacion cientifica)
        objeto_json = EvaluacionStepsJson.formateo_de_tiempos(objeto_json)

        return objeto_json
