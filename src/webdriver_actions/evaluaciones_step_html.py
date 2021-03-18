import time

import selenium.common.exceptions as sel_excep
from selenium.webdriver.remote.webdriver import WebDriver

from src.evaluacion_json import constantes_json
from src.models.correo import Correo
from src.models.result_step import ResultStep
from src.models.validaciones_list_json import ValidacionResultList
from src.utils import constantes_utils
from src.utils.format_utils import FormatUtils
from src.utils.temporizador import Temporizador
from src.webdriver_actions import constantes_webdriver_actions
from src.webdriver_actions.html.busqueda_elementos_html import BusquedaElementosHtml
from src.webdriver_actions.html.validaciones_html import ValidacionesHTML

from src.utils.evaluaciones_utils import EvaluacionesUtils


class EvaluacionesHtml:
    # variable/bandera el cual indica que version del owa se esta analizando
    cuenta_sin_dominio = ''
    url_owa_exchange = ''
    constantes_utils.owa_descubierto = 0

    # bandera para revisar si se encontro error en la plataforma
    mensaje_error_encontrado_owa = False
    txt_mensaje_error_encontrado_owa = ''

    @staticmethod
    def navegar_a_portal_principal_owa(web_driver: WebDriver, url: str, result_list: ValidacionResultList):

        resultado = ResultStep()
        resultado.tiempo_inicio_de_ejecucion = 0
        resultado.inicializar_tiempo_de_ejecucion()
        segundos_por_esperar_elemento_html = 10

        try:
            web_driver.get(url)
            ValidacionesHTML.verificar_ingreso_exitoso_pagina_principal(
                web_driver, constantes_webdriver_actions.INICIAR_SESION_EN_OWA_ID_INPUT_PASSWORD,
                segundos_por_esperar_elemento_html)

            resultado.mensaje_error = constantes_webdriver_actions.NAVEGAR_SITIO_MSG_INGRESO_SITIO_CON_EXITO. \
                format(url)

            resultado.validacion_correcta = True

        except sel_excep.TimeoutException as e:
            resultado.mensaje_error = constantes_webdriver_actions.NAVEGAR_SITIO_MSG_TIMEOUT_EXCEP_MSG_ERROR.format(
                segundos_por_esperar_elemento_html, url, FormatUtils.formatear_excepcion(e))

            resultado.validacion_correcta = False

        except sel_excep.WebDriverException as e:
            resultado.mensaje_error = constantes_webdriver_actions.NAVEGAR_SITIO_MSG_WEBDRIVER_EXCEP_MSG_ERROR. \
                format(FormatUtils.formatear_excepcion(e))

            resultado.validacion_correcta = False

        resultado.finalizar_tiempo_de_ejecucion()
        resultado.establecer_tiempo_de_ejecucion()
        result_list.result_validacion_ingreso_url = resultado

        return result_list

    # Metodo el cual se encarga de establecer las credenciales en los inputs de la pagina principal del OWA
    @staticmethod
    def iniciar_sesion_en_owa(webdriver: WebDriver, correo: Correo, result_list: ValidacionResultList):

        inicio_de_sesion_correcto = False
        existe_error_de_credenciales = False
        mensaje_de_error_en_inicio_de_sesion_obtenido = ''

        EvaluacionesHtml.cuenta_sin_dominio = FormatUtils.formatear_correo(correo.correo)
        EvaluacionesHtml.url_owa_exchange = correo.url

        resultado = ResultStep()

        resultado.tiempo_inicio_de_ejecucion = Temporizador.obtener_tiempo_timer()
        resultado.datetime_inicial = Temporizador.obtener_fecha_tiempo_actual()

        # verifica que haya ingresado correctamente a la url
        if not result_list.result_validacion_ingreso_url.validacion_correcta:
            resultado.validacion_correcta = False
            resultado.mensaje_error = 'No fue posible el inicio de sesion dentro de la plataforma Exchange. ' \
                                      'No se ingreso correctamente a la pagina principal de la plataforma'

            resultado.finalizar_tiempo_de_ejecucion()
            resultado.establecer_tiempo_de_ejecucion()
            result_list.result_validacion_acceso_portal_owa = resultado

            return result_list

        try:
            input_usuario = BusquedaElementosHtml.buscar_elemento_por_id_timeout(
                webdriver, constantes_webdriver_actions.INICIAR_SESION_EN_OWA_ID_INPUT_USER, 7)

            input_usuario.send_keys(correo.correo)

            input_password = BusquedaElementosHtml.buscar_elemento_por_id_timeout(
                webdriver, constantes_webdriver_actions.INICIAR_SESION_EN_OWA_ID_INPUT_PASSWORD, 7)

            input_password.send_keys(correo.password)

            boton_ingreso_correo = None

            if ValidacionesHTML.verificar_elemento_encontrado_por_id(
                    webdriver,
                    constantes_webdriver_actions.INICIAR_SESION_EN_OWA_ID_CHECKBOX_PORTAL_LIGHTWEIGHT_OWA_2010):

                check_casilla_owa_2010_version_ligera = BusquedaElementosHtml.buscar_elemento_por_id_timeout(
                    webdriver,
                    constantes_webdriver_actions.INICIAR_SESION_EN_OWA_ID_CHECKBOX_PORTAL_LIGHTWEIGHT_OWA_2010, 7)

                check_casilla_owa_2010_version_ligera.click()
                constantes_utils.owa_descubierto = 2010

            if ValidacionesHTML.verificar_elemento_encontrado_por_xpath(
                    webdriver, constantes_webdriver_actions.INICIAR_SESION_EN_OWA_XPATH_BTN_OWA_2010):

                boton_ingreso_correo = BusquedaElementosHtml.buscar_elemento_por_xpath_timeout(
                    webdriver, constantes_webdriver_actions.INICIAR_SESION_EN_OWA_XPATH_BTN_OWA_2010, 7)

                constantes_utils.owa_descubierto = 2010

            elif ValidacionesHTML.verificar_elemento_encontrado_por_xpath(
                    webdriver, constantes_webdriver_actions.INICIAR_SESION_EN_OWA_XPATH_BTN_OWA_2013_2016):

                boton_ingreso_correo = BusquedaElementosHtml.buscar_elemento_por_xpath_timeout(
                    webdriver, constantes_webdriver_actions.INICIAR_SESION_EN_OWA_XPATH_BTN_OWA_2013_2016, 7)

                constantes_utils.owa_descubierto = 2016

            boton_ingreso_correo.click()

            resultado.mensaje_error = constantes_json.OUTPUT_EXITOSO_1_1
            resultado.validacion_correcta = True

            # verifica que haya ingresado correctamente que haya ingresado al portal de exchange
            inicio_de_sesion_correcto = EvaluacionesUtils.validar_ingreso_de_sesion(10, webdriver)

            # verifica si hay error de credenciales
            existe_error_de_credenciales, mensaje_de_error_en_inicio_de_sesion_obtenido = \
                EvaluacionesUtils.existencia_de_mensaje_de_error_credenciales_en_portal(webdriver)

            if not inicio_de_sesion_correcto and existe_error_de_credenciales:
                resultado.mensaje_error = constantes_webdriver_actions.INICIAR_SESION_MSG_ERROR_EN_PLATAFORMA.format(
                    mensaje_de_error_en_inicio_de_sesion_obtenido)

                resultado.validacion_correcta = False
                resultado.error_plataforma_inicio_de_sesion = True
                resultado.error_inicio_de_sesion_credenciales_erroneas = True
                resultado.msg_error_de_credenciales = mensaje_de_error_en_inicio_de_sesion_obtenido

            elif not inicio_de_sesion_correcto and ValidacionesHTML.verificar_error_plataforma(webdriver):
                resultado.mensaje_error = constantes_webdriver_actions.INICIAR_SESION_MSG_ERROR_EN_PLATAFORMA.format(
                    mensaje_de_error_en_inicio_de_sesion_obtenido)

                resultado.validacion_correcta = False
                resultado.error_plataforma_inicio_de_sesion = True

        except sel_excep.NoSuchElementException as e:
            resultado.mensaje_error = constantes_webdriver_actions.INICIAR_SESION_MSG_NOSUCHELEM_EXCEP_MSG_ERROR. \
                format(FormatUtils.formatear_excepcion(e))

            resultado.validacion_correcta = False

        except sel_excep.TimeoutException as e:
            resultado.mensaje_error = constantes_webdriver_actions.INICIAR_SESION_MSG_NOSUCHELEM_EXCEP_MSG_ERROR. \
                format(FormatUtils.formatear_excepcion(e))

            resultado.validacion_correcta = False

        except sel_excep.WebDriverException as e:

            resultado.mensaje_error = constantes_webdriver_actions.INICIAR_SESION_MSG_WEBDRIVER_EXCEP_MSG_ERROR. \
                format(FormatUtils.formatear_excepcion(e))

            resultado.validacion_correcta = False

        resultado.finalizar_tiempo_de_ejecucion()
        resultado.establecer_tiempo_de_ejecucion()
        result_list.result_validacion_acceso_portal_owa = resultado

        return result_list

    # ejecuta la navegacion de cada una de las carpetas que tiene la sesion de correo electronico se establece como
    # parametro el numero de segundos en que se estara ejecutando la navegacion entre carpetas (lo estipulado son
    # 2 min -> 120 s)
    @staticmethod
    def navegacion_de_carpetas_por_segundos(correo: Correo, driver: WebDriver, result_list: ValidacionResultList,
                                            numero_de_segundos: int = 120):

        result_navegacion_carpetas = ResultStep()
        result_navegacion_carpetas.inicializar_tiempo_de_ejecucion()
        tiempo_por_verificar = numero_de_segundos + Temporizador.obtener_tiempo_timer()
        lista_carpetas = BusquedaElementosHtml.obtener_carpetas_en_sesion(driver)

        total_contadores_errores = 0
        contador_errores_staleelementreferenceexception = 0
        contador_errores_elementclickinterceptedexception = 0
        contador_errores_nosuchelementexception = 0
        contador_errores_timeoutexception = 0
        contador_errores_webdriverexception = 0
        intento_de_clicks_en_carpeta = 0

        # verifica si se tiene error de credenciales, por lo cual si se tiene este error, se establece el mensaje
        # de error y envia el result como finalizado, esto debido a que no se podra navegar entre carpetas por no
        # estar loggeado y sin tener acceso al buzon de la plataforma
        if result_list.result_validacion_acceso_portal_owa.error_inicio_de_sesion_credenciales_erroneas:
            result_navegacion_carpetas.finalizar_tiempo_de_ejecucion()
            result_navegacion_carpetas.establecer_tiempo_de_ejecucion()
            result_navegacion_carpetas.validacion_correcta = False

            result_navegacion_carpetas.mensaje_error = constantes_webdriver_actions.\
                NAVEGACION_CARPETAS_SEG_MSG_ERROR_CREDENCIALES_OWA.format(
                    result_list.result_validacion_acceso_portal_owa.msg_error_de_credenciales)

            result_list.result_validacion_navegacion_carpetas = result_navegacion_carpetas

            return result_list

        # verifica si hay error en plataforma, en caso de ser asi, intenta realizar n intentos para volver a loggearse
        # y verificar si ingreso correctamente al buzon de entrada para navegar entre las carpetas
        if ValidacionesHTML.verificar_error_plataforma(driver):
            result_navegacion_carpetas = ValidacionesHTML.intento_ingreso_nuevamente_al_portal(
                result_navegacion_carpetas, correo, driver, step_evaluacion='Navegacion carpetas y buzon de entrada')

        # verifica si aun se sigue mostrando el mensaje de error en la plataforma, en caso contrario la prueba falla
        # y notificaria al cliente de presentar un error de plataforma

        if ValidacionesHTML.verificar_error_plataforma(driver):

            result_navegacion_carpetas.finalizar_tiempo_de_ejecucion()
            result_navegacion_carpetas.establecer_tiempo_de_ejecucion()
            result_navegacion_carpetas.validacion_correcta = False
            msg_error = ValidacionesHTML.obtener_mensaje_error_plataforma(driver)
            result_navegacion_carpetas.mensaje_error = constantes_webdriver_actions. \
                NAVEGACION_CARPETAS_SEG_MSG_ERROR_PLATAFORMA_OWA.format(msg_error)

            result_list.result_validacion_navegacion_carpetas = result_navegacion_carpetas

            return result_list

        elif len(lista_carpetas) == 0:

            result_navegacion_carpetas.finalizar_tiempo_de_ejecucion()
            result_navegacion_carpetas.establecer_tiempo_de_ejecucion()
            result_navegacion_carpetas.validacion_correcta = False
            result_navegacion_carpetas.mensaje_error = constantes_webdriver_actions. \
                NAVEGACION_CARPETAS_SEG_LOG_ERROR_LISTA_CARPETAS_VACIA

            result_list.result_validacion_navegacion_carpetas = result_navegacion_carpetas

            return result_list

        while Temporizador.obtener_tiempo_timer() < tiempo_por_verificar:
            for carpeta in lista_carpetas:
                try:
                    elemento_html_carpeta = BusquedaElementosHtml.obtener_carpeta_con_timeout(driver, carpeta, 7)
                    elemento_html_carpeta.click()

                except sel_excep.StaleElementReferenceException:
                    contador_errores_staleelementreferenceexception += 1

                except sel_excep.ElementClickInterceptedException:
                    contador_errores_elementclickinterceptedexception += 1

                except sel_excep.NoSuchElementException:
                    contador_errores_nosuchelementexception += 1

                except sel_excep.TimeoutException:
                    contador_errores_timeoutexception += 1

                except sel_excep.WebDriverException:
                    contador_errores_webdriverexception += 1

                time.sleep(8)
                intento_de_clicks_en_carpeta += 1

        result_navegacion_carpetas.finalizar_tiempo_de_ejecucion()
        result_navegacion_carpetas.establecer_tiempo_de_ejecucion()

        total_contadores_errores = contador_errores_staleelementreferenceexception + \
                                   contador_errores_elementclickinterceptedexception + \
                                   contador_errores_nosuchelementexception + \
                                   contador_errores_timeoutexception + \
                                   contador_errores_webdriverexception

        # verifica que no haya algun mensaje de error en la plataforma, en caso contrario se muestra el mensaje de
        # error que aparace en la plataforma dentro del result
        if ValidacionesHTML.verificar_error_plataforma(driver):
            msg_error = ValidacionesHTML.obtener_mensaje_error_plataforma(driver)
            result_navegacion_carpetas.validacion_correcta = False
            result_navegacion_carpetas.mensaje_error = constantes_webdriver_actions. \
                NAVEGACION_CARPETAS_SEG_MSG_ERROR_PLATAFORMA_OWA.format(msg_error)
        elif total_contadores_errores == intento_de_clicks_en_carpeta:
            result_navegacion_carpetas.validacion_correcta = False
            result_navegacion_carpetas.mensaje_error = constantes_webdriver_actions.\
                NAVEGACION_CARPETAS_SEG_MSG_ERROR_INTENTOS_CLICK.format(intento_de_clicks_en_carpeta)
        else:
            result_navegacion_carpetas.validacion_correcta = True
            result_navegacion_carpetas.mensaje_error = constantes_json.OUTPUT_EXITOSO_2_1

        result_list.result_validacion_navegacion_carpetas = result_navegacion_carpetas

        return result_list

    @staticmethod
    def cerrar_sesion(webdriver: WebDriver, result_list: ValidacionResultList, correo: Correo):

        resultado_cierre_sesion = ResultStep()
        resultado_cierre_sesion.inicializar_tiempo_de_ejecucion()
        cierre_sesion_exitosa = False

        # verifica si se tiene error de credenciales, por lo cual si se tiene este error, se establece el mensaje
        # de error y envia el result como finalizado, esto debido a que no puede localizar el boton de cierre de
        # sesion sin antes haberse loggeado dentro de la plataforma
        if result_list.result_validacion_acceso_portal_owa.error_inicio_de_sesion_credenciales_erroneas:
            resultado_cierre_sesion.finalizar_tiempo_de_ejecucion()
            resultado_cierre_sesion.establecer_tiempo_de_ejecucion()
            resultado_cierre_sesion.validacion_correcta = False

            resultado_cierre_sesion.mensaje_error = constantes_webdriver_actions. \
                CERRAR_SESION_MSG_ERROR_CREDENCIALES_OWA.format(result_list.result_validacion_acceso_portal_owa.
                                                                msg_error_de_credenciales)

            result_list.result_validacion_cierre_sesion = resultado_cierre_sesion

            return result_list

        # verifica si hay error en plataforma, en caso de ser asi, intenta realizar n intentos para volver a loggearse
        # y verificar si ingreso correctamente al buzon de entrada para navegar entre las carpetas
        if ValidacionesHTML.verificar_error_plataforma(webdriver):
            resultado_cierre_sesion = ValidacionesHTML.intento_ingreso_nuevamente_al_portal(
                resultado_cierre_sesion, correo, webdriver, step_evaluacion='cierre de sesion')

        try:
            if constantes_utils.owa_descubierto == 2013 or constantes_utils.owa_descubierto == 2016:
                btn_perfil_usuario = BusquedaElementosHtml.localizar_boton_perfil_usuario(webdriver)
                btn_perfil_usuario.click()

                btn_cierre_de_sesion = BusquedaElementosHtml.localizar_boton_cierre_sesion_owa_2013_2016(webdriver)
                btn_cierre_de_sesion.click()

            elif constantes_utils.owa_descubierto == 2010:
                enlace_cierre_sesion = BusquedaElementosHtml.localizar_enlace_cierre_sesion_owa_2010(webdriver)
                enlace_cierre_sesion.click()

            webdriver.get(correo.url)

            ValidacionesHTML.verificar_ingreso_exitoso_pagina_principal(
                webdriver, constantes_webdriver_actions.INICIAR_SESION_EN_OWA_ID_INPUT_PASSWORD, 10)

            cierre_sesion_exitosa = True

        except sel_excep.NoSuchElementException as e:
            resultado_cierre_sesion.mensaje_error = constantes_webdriver_actions. \
                CERRAR_SESION_LOG_ERROR_NO_SUCH_ELEM_EXCEP.format(FormatUtils.formatear_excepcion(e))

            resultado_cierre_sesion.validacion_correcta = False

        except sel_excep.ElementClickInterceptedException:
            webdriver.refresh()
            EvaluacionesHtml.cerrar_sesion(webdriver, result_list, correo)

        except sel_excep.TimeoutException as e:
            resultado_cierre_sesion.mensaje_error = constantes_webdriver_actions. \
                CERRAR_SESION_LOG_ERROR_TIMEOUT_EXCEP.format(FormatUtils.formatear_excepcion(e))

            resultado_cierre_sesion.validacion_correcta = False

        except sel_excep.WebDriverException as e:
            resultado_cierre_sesion.mensaje_error = constantes_webdriver_actions. \
                CERRAR_SESION_LOG_ERROR_WEBDRIVER_EXCEP.format(FormatUtils.formatear_excepcion(e))

            resultado_cierre_sesion.validacion_correcta = False

        except AttributeError:
            resultado_cierre_sesion.mensaje_error = constantes_webdriver_actions. \
                CERRAR_SESION_LOG_ERROR_ATRIBUTE_ERROR_EXCEP

            resultado_cierre_sesion.validacion_correcta = False

        finally:

            # verifica que no haya algun mensaje de error en la plataforma, en caso contrario se muestra el mensaje de
            # error que aparace en la plataforma dentro del result
            if ValidacionesHTML.verificar_error_plataforma(webdriver):
                resultado_cierre_sesion.validacion_correcta = False
                msg_error = ValidacionesHTML.obtener_mensaje_error_plataforma(webdriver)

                resultado_cierre_sesion.mensaje_error = constantes_webdriver_actions.CERRAR_SESION_ERROR_PLATAFORMA. \
                    format(msg_error)

                cierre_sesion_exitosa = False

        if cierre_sesion_exitosa:
            resultado_cierre_sesion.mensaje_error = constantes_json.OUTPUT_EXITOSO_3_1
            resultado_cierre_sesion.validacion_correcta = True

        resultado_cierre_sesion.finalizar_tiempo_de_ejecucion()
        resultado_cierre_sesion.establecer_tiempo_de_ejecucion()
        result_list.result_validacion_cierre_sesion = resultado_cierre_sesion

        return result_list
