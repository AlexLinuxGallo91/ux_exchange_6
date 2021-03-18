import configparser
import json

from src.evaluacion_json import constantes_json


class FormatUtils:
    CADENA_VACIA = ''
    BACKSPACE = '&nbsp;'
    ESPACIO = ' '
    num_archivos_eliminados = 0

    # al usar el driver PhantomJS, las excepciones se muestran en un formato json,
    # la funcion detecta si la cadena de la excepcion es un json, de ser correcto,
    # intenta obtener solamente el mensaje general del error, ignorando las demas
    # propiedades que contengan el json
    @staticmethod
    def formatear_excepcion(ex):

        cadena_excepcion = str(ex)
        ex_json = None
        is_ex_json = False

        try:
            cadena_excepcion = ex.msg
        except AttributeError as e:
            pass

        try:
            ex_json = json.loads(cadena_excepcion)
            is_ex_json = True
        except ValueError as e:
            pass

        if is_ex_json:
            try:
                cadena_excepcion = ex_json['errorMessage']
            except KeyError as e:
                pass

        return cadena_excepcion

    # funcion encargada de leer las propiedades/secciones del archivo de configuracion config.ini
    @staticmethod
    def obtener_archivo_de_configuracion():
        config = None

        try:
            config = configparser.ConfigParser()
            config.read(constantes_json.PATH_ARCHIVO_CONFIG_INI)
        except configparser.Error as e:
            pass

        return config

    # funcion encargada de truncar un decimal en caso de tener una notacion cientifica, en caso de ser asi
    # se trunca el decimal a un maximo de 12 decimales
    @staticmethod
    def truncar_float_cadena(cifra_decimal):
        num = cifra_decimal

        if isinstance(cifra_decimal, str):
            try:
                num = float(cifra_decimal)
            except ValueError as e:
                num = 0

        num = round(num, 12)
        num = '{:.12f}'.format(num)

        return num

    # remueve los espacios en los textos de los elementos HTML
    @staticmethod
    def remover_backspaces(cadena):
        return cadena.replace(FormatUtils.BACKSPACE, FormatUtils.ESPACIO)

    # verifica que una cadena sea un formato valido JSON. En caso exitoso
    # la funcion devuelve True, en caso contrario False
    @staticmethod
    def cadena_a_json_valido(cadena=''):
        try:
            json.loads(cadena)
            return True
        except ValueError as e:
            return False

    @staticmethod
    def formatear_correo(correo):

        if correo is None:
            correo = ''
        else:
            correo = correo.strip()

        return correo.split('@')[0]
