import time

import selenium.common.exceptions as SelExcept
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.models.correo import Correo
from src.models.result_step import ResultStep


class ValidacionesHTML:

    @staticmethod
    def verificar_elemento_encontrado_por_id(webdriver: WebDriver, id_elem_html: str):
        """
        verifica si se encontro el elemento deseado mediante el id
        retorna True si se encontro el elemento
        en caso contrario retorna False

        :param webdriver:
        :param id_elem_html:
        :return:
        """
        elemento_html = None

        try:
            webdriver.find_element_by_id(id_elem_html)
            return True
        except SelExcept.NoSuchElementException:
            return False

    @staticmethod
    def verificar_elemento_encontrado_por_xpath(webdriver: WebDriver, xpath: str):
        """
        verifica si se encontro el elemento deseado mediante el xpath
        retorna True si se encontro el elemento
        en caso contrario retorna False

        :param webdriver:
        :param xpath:
        :return:
        """
        elemento_html = None

        try:
            webdriver.find_element_by_xpath(xpath)
            return True
        except SelExcept.NoSuchElementException as e:
            return False

    @staticmethod
    def verificar_elemento_encontrado_por_clase_js(webdriver, clase: str):
        """
        :param webdriver:
        :param clase:
        :return:
        """
        elementos_html = webdriver.execute_script(
            "return document.getElementsByClassName('{}');".format(clase))

        if elementos_html is not None and len(elementos_html) >= 1:
            return True
        else:
            return False

    @staticmethod
    def verificar_error_plataforma(driver: WebDriver):
        """
        verifica si en la plataforma existe algun error presente, las cuales se enlistan a continuacion y
        que se han descubierto hasta este momento:

        1) elemento title HTML con leyenda "Error"
        2) En el body de la plataforma se se presente la leyenda 'NegotiateSecurityContext failed with for host'

        :param driver:
        :return:
        """
        existe_error = False
        leyenda_title = driver.title
        mensaje_error_localizado = ''

        if leyenda_title is None:
            leyenda_title = ''

        if 'Error' in leyenda_title:
            existe_error = True

            if ValidacionesHTML.verificar_elemento_encontrado_por_id(driver, 'errMsg'):
                elemento_mensaje_error = driver.find_element_by_id('errMsg')
                mensaje_error_localizado = elemento_mensaje_error.get_attribute('innerHTML')
                existe_error = True

        elif ValidacionesHTML.verificar_elemento_encontrado_por_xpath(driver, '//body'):

            elemento_body = driver.find_element_by_xpath('//body')
            mensaje_error_localizado = elemento_body.get_attribute('innerHTML')

            if mensaje_error_localizado is None:
                mensaje_error_localizado = ''

            if 'NegotiateSecurityContext' in mensaje_error_localizado or \
                    'LogonDenied' in mensaje_error_localizado:
                existe_error = True

        if existe_error:
            ValidacionesHTML.txt_mensaje_error_encontrado_owa = mensaje_error_localizado
            ValidacionesHTML.mensaje_error_encontrado_owa = existe_error

        return existe_error

    @staticmethod
    def obtener_mensaje_error_plataforma(driver: WebDriver):

        existe_error = False
        leyenda_title = driver.title
        mensaje_error_localizado = ''

        if leyenda_title is None:
            leyenda_title = ''

        if 'Error' in leyenda_title:
            existe_error = True

            if ValidacionesHTML.verificar_elemento_encontrado_por_id(driver, 'errMsg'):
                elemento_mensaje_error = driver.find_element_by_id('errMsg')
                mensaje_error_localizado = elemento_mensaje_error.get_attribute('innerHTML')
                existe_error = True

        elif ValidacionesHTML.verificar_elemento_encontrado_por_xpath(driver, '//body'):

            elemento_body = driver.find_element_by_xpath('//body')
            mensaje_error_localizado = elemento_body.get_attribute('innerHTML')

            if mensaje_error_localizado is None:
                mensaje_error_localizado = ''

            if 'NegotiateSecurityContext' in mensaje_error_localizado or \
                    'LogonDenied' in mensaje_error_localizado:
                existe_error = True

        return mensaje_error_localizado


    # verifica que no aparezca el dialogo de interrupcion (dialogo informativo que en algunas ocasiones
    # aparece cuando se ingresa a una carpeta con correos nuevos)
    @staticmethod
    def verificar_dialogo_de_interrupcion(driver, result):
        if len(driver.find_elements_by_id('divPont')) > 0:

            try:
                time.sleep(4)
                boton_remover_dialogo = driver.find_element_by_id('imgX')
                boton_remover_dialogo.click()
            except SelExcept.ElementClickInterceptedException:
                ValidacionesHTML.verificar_dialogo_de_interrupcion(driver, result)


    @staticmethod
    def intento_ingreso_nuevamente_al_portal(result: ResultStep, correo: Correo, driver: WebDriver,
                                             numero_de_intentos_por_ingresar: int = 3, step_evaluacion: str = ''):

        for intento in range(numero_de_intentos_por_ingresar):
            try:
                boton_inicio_sesion = None
                driver.delete_all_cookies()
                driver.refresh()

                driver.get(correo.url)

                WebDriverWait(driver, 18).until(EC.visibility_of_element_located((By.ID, 'username')))

                input_usuario = driver.find_element_by_id('username')
                input_password = driver.find_element_by_id('password')

                input_usuario.clear()
                input_password.clear()

                if ValidacionesHTML.verificar_elemento_encontrado_por_id(driver, 'chkBsc'):
                    check_casilla_owa_2010_version_ligera = driver.find_element_by_id('chkBsc')
                    check_casilla_owa_2010_version_ligera.click()

                if ValidacionesHTML.verificar_elemento_encontrado_por_xpath(driver, "//input[@type='submit'][@class='btn']"):
                    boton_inicio_sesion = driver.find_element_by_xpath("//input[@type='submit'][@class='btn']")

                elif ValidacionesHTML.verificar_elemento_encontrado_por_xpath(driver, "//div[@class='signinbutton']"):
                    boton_inicio_sesion = driver.find_element_by_xpath("//div[@class='signinbutton']")

                # num_random = randint(1,1000)
                # driver.save_screenshot('./Logs/{}_0.png'.format(num_random))
                time.sleep(1)
                input_usuario.send_keys(correo.correo)
                # driver.save_screenshot('./Logs/{}_1.png'.format(num_random))
                time.sleep(1)
                input_password.send_keys(correo.password)
                # driver.save_screenshot('./Logs/{}_2.png'.format(num_random))
                time.sleep(1)
                boton_inicio_sesion.click()
                # driver.save_screenshot('./Logs/{}_5.png'.format(num_random))

                time.sleep(10)
                # driver.save_screenshot('./Logs/{}_6.png'.format(num_random))

                # se verifica si encuentra al menos las carpetas en la bandeja
                if ValidacionesHTML.verificar_elemento_encontrado_por_clase_js(driver, "_n_C4") or \
                        ValidacionesHTML.verificar_elemento_encontrado_por_clase_js(driver, "_n_Z6") or \
                        ValidacionesHTML.verificar_elemento_encontrado_por_xpath(driver, "//a[@name='lnkFldr']"):

                    result.validacion_correcta = True
                    result.mensaje_error = 'Se ingresa nuevamente de manera correcta al buzon de entrada de la ' \
                                           'cuenta {}'.format(correo.correo)

                    break

                elif ValidacionesHTML.verificar_error_plataforma(driver):
                    msg_error = ValidacionesHTML.obtener_mensaje_error_plataforma(driver)
                    result.validacion_correcta = False
                    result.mensaje_error = 'Ingreso al buzon de entrada no exitosa, se presenta el siguiente error ' \
                        'dentro de la plataforma Exchange OWA: {}'.format(msg_error)

                else:
                    result.validacion_correcta = False
                    result.mensaje_error = 'Ingreso al buzon de entrada no exitosa. Se intento ingresar a la ' \
                        'bandeja de entrada de la plataforma Exchange OWA, se presenta problemas de carga de pagina'


            except SelExcept.NoSuchElementException as e:
                result.validacion_correcta = False
                result.mensaje_error = 'No fue posible ingresar nuevamente a la bandeja de entrada. No se ' \
                                       'localizaron correctamente los inputs para el ingreso de usuario y password'

            except SelExcept.TimeoutException as e:
                result.validacion_correcta = False
                result.mensaje_error = 'No fue posible ingresar nuevamente a la bandeja de entrada. Se tiene un ' \
                                       'problema de tiempo de carga en la pagina'


        return result

    @staticmethod
    def verificar_ingreso_exitoso_pagina_principal(web_driver: WebDriver, id_html: str, seg_de_espera: int = 20):

        try:
            WebDriverWait(web_driver, seg_de_espera).until(
                EC.presence_of_element_located((By.ID, id_html)))

        except SelExcept.TimeoutException as e:
            e.msg = 'No fue posible localizar el elemento HTML con el ID {}'.format(id_html)

            raise e




