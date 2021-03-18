import src.utils.constantes_utils as constantes_utils
from src.utils.temporizador import Temporizador
from selenium.webdriver.remote.webdriver import WebDriver
from src.webdriver_actions.html.validaciones_html import ValidacionesHTML
import src.webdriver_actions.constantes_webdriver_actions as constantes_webdriver_actions
import time
import selenium.common.exceptions as sel_excep


class EvaluacionesUtils:

    @staticmethod
    def validar_ingreso_de_sesion(tiempo_de_espera: 10=int, driver=WebDriver):

        mensaje_de_error = ''
        tiempo_inicio = Temporizador.obtener_tiempo_timer()
        tiempo_fin = tiempo_inicio + tiempo_de_espera
        ingreso_correcto_al_buzon_del_portal = False

        while tiempo_inicio < tiempo_fin:
            tiempo_inicio = Temporizador.obtener_tiempo_timer()

            if ValidacionesHTML.verificar_elemento_encontrado_por_clase_js(
                    driver, constantes_webdriver_actions.OBTENER_CARPETAS_EN_SESION_CSS_CARPETA_OWA_2016):
                constantes_utils.owa_descubierto = 2016
                ingreso_correcto_al_buzon_del_portal = True

            elif ValidacionesHTML.verificar_elemento_encontrado_por_clase_js(
                    driver, constantes_webdriver_actions.OBTENER_CARPETAS_EN_SESION_CSS_CARPETA_OWA_2013):
                constantes_utils.owa_descubierto = 2013
                ingreso_correcto_al_buzon_del_portal = True

            elif ValidacionesHTML.verificar_elemento_encontrado_por_xpath(
                    driver, constantes_webdriver_actions.OBTENER_CARPETAS_EN_SESION_XPATH_CARPETA_OWA_2010):
                constantes_utils.owa_descubierto = 2010
                ingreso_correcto_al_buzon_del_portal = True

            if ingreso_correcto_al_buzon_del_portal is True:
                break

            time.sleep(1)

        return  ingreso_correcto_al_buzon_del_portal

    @staticmethod
    def existencia_de_mensaje_de_error_credenciales_en_portal(webdriver: WebDriver):

        mensaje_de_error = ''
        se_encontro_mensaje = False

        try:
            if constantes_utils.owa_descubierto == 2010:
                mensaje_de_error = webdriver.find_element_by_xpath(
                    constantes_webdriver_actions.INICIAR_SESION_EN_OWA_XPATH_ERROR_CREDENCIALES_OWA_2010)

                mensaje_de_error = mensaje_de_error.get_attribute('innerHTML')

            elif constantes_utils.owa_descubierto == 2016 or constantes_utils.owa_descubierto == 2013:
                mensaje_de_error = webdriver.execute_script(
                    constantes_webdriver_actions.INICIAR_SESION_JS_LOCATE_ID_MSG_ERROR_CREDENCIALES_OWA_2016_2013)

            if isinstance(mensaje_de_error, str):
                msg_comprimido = mensaje_de_error.strip()

                if len(msg_comprimido) > 0:
                    se_encontro_mensaje = True

        except sel_excep.NoSuchElementException:
            pass
        except sel_excep.JavascriptException:
            pass

        return se_encontro_mensaje, mensaje_de_error
