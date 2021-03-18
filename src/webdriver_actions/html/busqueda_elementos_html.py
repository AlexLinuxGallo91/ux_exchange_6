import selenium.common.exceptions as SelExcept
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.utils.format_utils import FormatUtils
from src.utils.temporizador import Temporizador
from src.webdriver_actions import constantes_webdriver_actions
from src.webdriver_actions.html.validaciones_html import ValidacionesHTML
from src.utils import constantes_utils


class BusquedaElementosHtml:

    @staticmethod
    def buscar_elemento_por_id_timeout(web_driver: WebDriver, id_el_html: str, seg_timeout: int = 0):

        try:
            return WebDriverWait(web_driver, seg_timeout).until(EC.presence_of_element_located((By.ID, id_el_html)))
        except SelExcept.TimeoutException as e:
            e.msg = 'No fue posible localizar el elemento HTML con el id {} durante un lapso de {} ' \
                    'segundos'.format(id_el_html, seg_timeout)
            raise e

    @staticmethod
    def buscar_elemento_por_xpath_timeout(web_driver: WebDriver, xpath_html: str, seg_timeout: int = 0):

        try:
            return WebDriverWait(web_driver, seg_timeout).until(EC.presence_of_element_located((By.XPATH, xpath_html)))
        except SelExcept.TimeoutException as e:
            e.msg = 'No fue posible localizar el elemento HTML con el XPATH {} durante un lapso de {} ' \
                    'segundos'.format(xpath_html, seg_timeout)
            raise e

    # cuando se ingresa correctamen al OWA, se localizan las listas de folders que contiene el usuario en sesion
    @staticmethod
    def obtener_carpetas_en_sesion(driver: WebDriver):

        lista_de_carpetas_localizadas = []
        lista_nombres_de_carpetas_formateadas = []
        tiempo_de_inicio = Temporizador.obtener_tiempo_timer()
        tiempo_de_finalizacion = 0
        se_encontraron_carpetas = False

        while tiempo_de_finalizacion < 60:

            if ValidacionesHTML.verificar_elemento_encontrado_por_clase_js(
                    driver, constantes_webdriver_actions.OBTENER_CARPETAS_EN_SESION_CSS_CARPETA_OWA_2016):
                constantes_utils.owa_descubierto = 2016
                se_encontraron_carpetas = True

            elif ValidacionesHTML.verificar_elemento_encontrado_por_clase_js(
                    driver, constantes_webdriver_actions.OBTENER_CARPETAS_EN_SESION_CSS_CARPETA_OWA_2013):
                constantes_utils.owa_descubierto = 2013
                se_encontraron_carpetas = True

            elif ValidacionesHTML.verificar_elemento_encontrado_por_xpath(
                    driver, constantes_webdriver_actions.OBTENER_CARPETAS_EN_SESION_XPATH_CARPETA_OWA_2010):
                constantes_utils.owa_descubierto = 2010
                se_encontraron_carpetas = True

            tiempo_de_finalizacion = Temporizador.obtener_tiempo_timer() - tiempo_de_inicio

            if tiempo_de_finalizacion % 20 == 0:
                driver.refresh()

        if se_encontraron_carpetas:
            if constantes_utils.owa_descubierto == 2010:
                lista_de_carpetas_localizadas = driver.find_elements_by_xpath(
                    constantes_webdriver_actions.OBTENER_CARPETAS_EN_SESION_XPATH_CARPETA_OWA_2010)

            elif constantes_utils.owa_descubierto == 2013:
                lista_de_carpetas_localizadas = driver.execute_script(
                    constantes_webdriver_actions.OBTENER_CARPETAS_EN_SESION_JS_OBTENER_CARPETA_2013)

            elif constantes_utils.owa_descubierto == 2016:
                lista_de_carpetas_localizadas = driver.execute_script(
                    constantes_webdriver_actions.OBTENER_CARPETAS_EN_SESION_JS_OBTENER_CARPETA_2016)

        for carpeta in lista_de_carpetas_localizadas:

            if constantes_utils.owa_descubierto == 2010:
                nombre_de_carpeta = carpeta.text
            else:
                nombre_de_carpeta = FormatUtils.remover_backspaces(carpeta.get_attribute('innerHTML'))

            lista_nombres_de_carpetas_formateadas.append(nombre_de_carpeta)

        return lista_nombres_de_carpetas_formateadas

    @staticmethod
    def obtener_carpeta_con_timeout(driver: WebDriver, nombre_de_la_carpeta: str, timeout: int = 7):
        tiempo_limite = Temporizador.obtener_tiempo_timer() + timeout

        while Temporizador.obtener_tiempo_timer() < tiempo_limite:

            # verifica si encontro folder en caso de estar en plataforma OWA 2010
            if ValidacionesHTML.verificar_elemento_encontrado_por_xpath(
                    driver, constantes_webdriver_actions.NAVEGACION_CARPETAS_SEG_XPATH_CARPETA_OWA_2010.format(
                        nombre_de_la_carpeta)):

                return driver.find_element_by_xpath(
                    constantes_webdriver_actions.NAVEGACION_CARPETAS_SEG_XPATH_CARPETA_OWA_2010.format(
                        nombre_de_la_carpeta))

            elif ValidacionesHTML.verificar_elemento_encontrado_por_xpath(
                    driver, constantes_webdriver_actions.NAVEGACION_CARPETAS_SEG_XPATH_CARPETA_OWA_2013.format(
                        nombre_de_la_carpeta)):

                return driver.find_element_by_xpath(
                    constantes_webdriver_actions.NAVEGACION_CARPETAS_SEG_XPATH_CARPETA_OWA_2013.format(
                        nombre_de_la_carpeta))

            elif ValidacionesHTML.verificar_elemento_encontrado_por_xpath(
                    driver, constantes_webdriver_actions.NAVEGACION_CARPETAS_SEG_XPATH_CARPETA_OWA_2016.format(
                        nombre_de_la_carpeta)):

                return driver.find_element_by_xpath(
                    constantes_webdriver_actions.NAVEGACION_CARPETAS_SEG_XPATH_CARPETA_OWA_2016.format(
                        nombre_de_la_carpeta))

        raise SelExcept.TimeoutException(msg='No fue posible localizar la carpeta dentro de la plataforma')

    @staticmethod
    def localizar_boton_perfil_usuario(driver: WebDriver, timeout: int = 7):
        tiempo_limite = Temporizador.obtener_tiempo_timer() + timeout

        while Temporizador.obtener_tiempo_timer() < tiempo_limite:

            # verifica si encontro folder en caso de estar en plataforma OWA 2013
            if ValidacionesHTML.verificar_elemento_encontrado_por_xpath(
                    driver, constantes_webdriver_actions.CERRAR_SESION_BTN_PERFIL_USUARIO_OWA_2013):

                return driver.find_element_by_xpath(
                    constantes_webdriver_actions.CERRAR_SESION_BTN_PERFIL_USUARIO_OWA_2013)

            # verifica si encontro folder en caso de estar en plataforma OWA 2016
            elif ValidacionesHTML.verificar_elemento_encontrado_por_xpath(
                    driver, constantes_webdriver_actions.CERRAR_SESION_BTN_PERFIL_USUARIO_OWA_2016):

                return driver.find_element_by_xpath(
                    constantes_webdriver_actions.CERRAR_SESION_BTN_PERFIL_USUARIO_OWA_2016)

        raise SelExcept.TimeoutException(msg='No fue posible localizar el boton de perfil del usuario dentro de la '
                                             'plataforma')

    @staticmethod
    def localizar_boton_cierre_sesion_owa_2013_2016(driver: WebDriver, timeout: int = 7):
        tiempo_limite = Temporizador.obtener_tiempo_timer() + timeout

        while Temporizador.obtener_tiempo_timer() < tiempo_limite:

            # verifica si encontro folder en caso de estar en plataforma OWA 2016
            if ValidacionesHTML.verificar_elemento_encontrado_por_xpath(
                    driver, constantes_webdriver_actions.CERRAR_SESION_BTN_XPATH_CIERRE_SESION_OWA_2016_ENGLISH):

                return driver.find_element_by_xpath(
                    constantes_webdriver_actions.CERRAR_SESION_BTN_XPATH_CIERRE_SESION_OWA_2016_ENGLISH)

            elif ValidacionesHTML.verificar_elemento_encontrado_por_xpath(
                    driver, constantes_webdriver_actions.CERRAR_SESION_BTN_XPATH_CIERRE_SESION_OWA_2016_SPANISH):

                return driver.find_element_by_xpath(
                    constantes_webdriver_actions.CERRAR_SESION_BTN_XPATH_CIERRE_SESION_OWA_2016_SPANISH)

            # verifica si encontro folder en caso de estar en plataforma OWA 2013
            elif ValidacionesHTML.verificar_elemento_encontrado_por_xpath(
                    driver, constantes_webdriver_actions.CERRAR_SESION_BTN_XPATH_CIERRE_SESION_OWA_2013):

                return driver.find_element_by_xpath(
                    constantes_webdriver_actions.CERRAR_SESION_BTN_XPATH_CIERRE_SESION_OWA_2013)

        raise SelExcept.TimeoutException(msg='No fue posible localizar el boton de cierre de sesion dentro de la '
                                             'plataforma')

    @staticmethod
    def localizar_enlace_cierre_sesion_owa_2010(driver: WebDriver, timeout: int = 7):
        tiempo_limite = Temporizador.obtener_tiempo_timer() + timeout

        while Temporizador.obtener_tiempo_timer() < tiempo_limite:

            # verifica si encontro folder en caso de estar en plataforma OWA 2013
            if ValidacionesHTML.verificar_elemento_encontrado_por_id(
                    driver, constantes_webdriver_actions.CERRAR_SESION_CIERRE_SESION_ID_BTN_CIERRE_SESION_OWA_2010):
                return driver.find_element_by_id(
                    constantes_webdriver_actions.CERRAR_SESION_CIERRE_SESION_ID_BTN_CIERRE_SESION_OWA_2010)

        raise SelExcept.TimeoutException(msg='No fue posible localizar el boton de cierre de sesion dentro de la '
                                             'plataforma')
