import json
import sys

from src.evaluacion_json import constantes_json
from src.evaluacion_json.generador_json_log_base import GeneradorJsonBaseEvaluacion
from src.evaluacion_json.llenado_log_json import EvaluacionStepsJson
from src.models.correo import Correo
from src.models.validaciones_list_json import ValidacionResultList
from src.utils.main_utils import UtilsMain
from src.utils.format_utils import FormatUtils
from src.webdriver_actions.evaluaciones_step_html import EvaluacionesHtml
from src.webdriver_config.config_webdriver import ConfiguracionWebDriver

web_driver = None


def generar_test_json(driver, url_a_navegar, correo):

    # objeto con lista de objetos result el cual verificara cada una de las validaciones para cada uno de los steps y
    # el cual nos permitira adjuntar el resultado en el JSON
    lista_validaciones = ValidacionResultList()

    # genera la estructura del archivo JSON (resultado/salida)
    objeto_json = GeneradorJsonBaseEvaluacion.generar_nuevo_template_json()

    # establece el datetime de inicio dentro del json
    objeto_json = EvaluacionStepsJson.establecer_fecha_tiempo_de_inicio(objeto_json)

    # empieza la primera validacion de ingresar a la url del portal
    lista_validaciones = EvaluacionesHtml.navegar_a_portal_principal_owa(driver, url_a_navegar, lista_validaciones)

    # intenta ingresar las credenciales de la cuenta dentro del portal, verificando el acceso del correo desde el portal
    lista_validaciones = EvaluacionesHtml.iniciar_sesion_en_owa(driver, correo, lista_validaciones)

    # empieza la validacion de la navegacion en cada una de las carpetas que se obtuvieron en la linea anterior
    lista_validaciones = EvaluacionesHtml.navegacion_de_carpetas_por_segundos(correo, driver, lista_validaciones)

    # se valida el cierre de sesion desde el OWA
    lista_validaciones = EvaluacionesHtml.cerrar_sesion(driver, lista_validaciones, correo)

    # establece los datos en el json con los resultados de cada una de las validaciones
    objeto_json = EvaluacionStepsJson.formar_cuerpo_json(lista_validaciones, objeto_json, correo)

    # establecen el json generado dentro de otra structura JSON con el correo como nodo
    objeto_json = GeneradorJsonBaseEvaluacion.establecer_estructura_principal_json(correo.correo, objeto_json)

    return objeto_json


def iniciar_prueba(correo):
    # obtiene los datos del archivo de configuracion
    global web_driver
    archivo_configuracion = FormatUtils.obtener_archivo_de_configuracion()

    web_driver_por_utilizar = archivo_configuracion.get('Driver', 'driverPorUtilizar')
    path_web_driver = archivo_configuracion.get('Driver', 'ruta')

    # establece el driver por utilizar (chrome o firefox)
    config_web_driver = ConfiguracionWebDriver(path_web_driver, web_driver_por_utilizar)
    web_driver = config_web_driver.configurar_obtencion_web_driver()

    # se generan las validaciones y el resultado por medio de un objeto JSON
    objeto_json = generar_test_json(web_driver, correo.url, correo)

    # cierre del web_driver
    if web_driver is not None:
        web_driver.close()
        web_driver.quit()

    # se retorna el objeto json como cadena
    return json.dumps(objeto_json)


# Punto de partida/ejecucion principal del script
def main():
    argumentos_script = sys.argv[1:]

    if len(argumentos_script) == 0:
        print('Favor de establecer el JSON con los argumentos necesarios para la ejecucion correcta del script')
        sys.exit(1)

    constantes_json.configurar_paths_constantes(__file__)

    archivo_config = FormatUtils.obtener_archivo_de_configuracion()

    # verifica que el archivo config contenga todos los parametros de configuracion correctamente
    if not UtilsMain.verificacion_correcta_archivo_config(archivo_config):
        sys.exit(1)

    # obtiene el primer argumento del script el cual es el objeto JSON con los datos de la cuenta Exchange por
    # testear
    argumento_cadena_json = argumentos_script[0]

    # verifica que la cadena sea un json valido en caso contrario se omite la experiencia de usuario
    argumento_cadena_json = argumento_cadena_json.strip()

    # verifica que la cadena del argumento sea un JSON valido
    if not FormatUtils.cadena_a_json_valido(argumento_cadena_json):
        print('El argumento {} no es un JSON valido, favor de verificar nuevamente el argumento.'.format(
            argumento_cadena_json))
        sys.exit()

    # una vez pasando todos los filtros correctos, se obtienen del objeto JSON el correo, url y password por verificar
    objeto_argumento_json = json.loads(argumento_cadena_json)

    portal_url_exchange = objeto_argumento_json['url']
    correo_exchange = objeto_argumento_json['user']
    password_cuenta_exchange = objeto_argumento_json['password']

    correo_por_probar = Correo(correo_exchange, password_cuenta_exchange, portal_url_exchange)

    salida_log_json = iniciar_prueba(correo_por_probar)

    print(salida_log_json)


main()

