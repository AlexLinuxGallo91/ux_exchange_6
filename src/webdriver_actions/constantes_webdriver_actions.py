########################################################################################################################
##                                    Ejecuciones Scripts JS OWA 2013                                                 ##
########################################################################################################################

JS_LOCATE_DIV_CONTENT_BTN_CIERRE_SESION_OWA_2013 = '''
    var btn_cierre_sesion = document.querySelector('div._hl_d')
    return btn_cierre_sesion;
'''

JS_LOCATE_BTN_CIERRE_SESION_OWA_2013_ENGLISH = '''
    var btn_cierre_sesion = document.evaluate('//span[text()="Sign out"]', 
                                              document, null, 
                                              XPathResult.FIRST_ORDERED_NODE_TYPE, 
                                              null).singleNodeValue;
    return btn_cierre_sesion;
'''

JS_LOCATE_BTN_CIERRE_SESION_OWA_2013_SPANISH = '''
    var btn_cierre_sesion = document.evaluate('//span[text()="Cerrar sesi\u00f3n"]', 
                                              document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, 
                                              null).singleNodeValue;
    return btn_cierre_sesion;
'''
########################################################################################################################
##                                    Ejecuciones Scripts JS OWA 2016                                                 ##
########################################################################################################################


JS_LOCATE_DIV_CONTENT_BTN_CIERRE_SESION_OWA_2016 = '''
    var btn_cierre_sesion = document.querySelector('div.ms-Icon--person');
    return btn_cierre_sesion;
'''

JS_LOCATE_BTN_CIERRE_SESION_OWA_2016 = '''
    var btn_cierre_sesion = document.evaluate('//span[text()="Cerrar sesi\u00f3n"]', 
                                              document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, 
                                              null).singleNodeValue;
    return btn_cierre_sesion;
'''

########################################################################################################################
##                                   Constantes AccionesHTML navegar sitio                                            ##
########################################################################################################################

NAVEGAR_SITIO_MSG_INGRESO_SITIO = 'ingresando a la siguiente url: "{}"'

NAVEGAR_SITIO_MSG_INGRESO_SITIO_CON_EXITO = 'Accediendo a la pagina principal de la plataforma Exchange OWA con exito' \
                                            ', url actual: "{}"'

NAVEGAR_SITIO_MSG_TIMEOUT_EXCEP_MSG_ERROR = 'Han transcurrido mas de {} segundos sin poder acceder a la pagina ' \
                                            'principal de la plataforma "{}": {}'

NAVEGAR_SITIO_MSG_WEBDRIVER_EXCEP_MSG_ERROR = 'No fue posible ingresar a la plataforma de Exchange OWA, favor de ' \
                                              'verificar si se tiene conectividad por internet, error detallado : {}'

########################################################################################################################
##                               Constantes AccionesHTML iniciar_sesion_en_owa                                        ##
########################################################################################################################

INICIAR_SESION_EN_OWA_ID_INPUT_USER = 'username'

INICIAR_SESION_EN_OWA_ID_INPUT_PASSWORD = 'password'

INICIAR_SESION_EN_OWA_ID_ERROR_CREDENCIALES_OWA_2010 = 'trInvCrd'

INICIAR_SESION_EN_OWA_XPATH_ERROR_CREDENCIALES_OWA_2010 = "//tr[@id='trInvCrd']/td"

INICIAR_SESION_EN_OWA_XPATH_BTN_OWA_2010 = "//input[@type='submit'][@class='btn']"

INICIAR_SESION_EN_OWA_XPATH_BTN_OWA_2013_2016 = "//div[@class='signinbutton']"

INICIAR_SESION_EN_OWA_ID_CHECKBOX_PORTAL_LIGHTWEIGHT_OWA_2010 = 'chkBsc'

INICIAR_SESION_EN_OWA_MOSTRAR_TITLE_AND_URL = 'Titulo actual de la plataforma: {}\nURL actual de la plataforma: {}'

INICIAR_SESION_MSG_NOSUCHELEM_EXCEP_MSG_ERROR = 'No fue posible iniciar sesion dentro de la plataforma OWA, no se ' \
                                                'localizaron los inputs para ingresar las credenciales de la cuenta ' \
                                                'de correo electronico Exchange: {}'

INICIAR_SESION_MSG_WEBDRIVER_EXCEP_MSG_ERROR = 'No fue posible ingresar a la plataforma de Exchange OWA, favor de ' \
                                               'verificar si se tiene conectividad por internet, error detallado : {}'

INICIAR_SESION_LOG_MSG_ERROR_CREDENCIALES_OWA = 'Inicio de sesion no exitosa dentro de la plataforma Exchange OWA, ' \
                                                'se presenta el siguiente mensaje de error de credenciales: {}'

INICIAR_SESION_JS_LOCATE_ID_MSG_ERROR_CREDENCIALES_OWA_2016_2013 = '''
    var mensaje_error = document.querySelector("#signInErrorDiv").innerText;
    return mensaje_error;
'''

INICIAR_SESION_CREDENCIALES_INVALIDSESION_ID_EXCEP_MSG_ERROR = 'Inicio de sesion no exitosa dentro de la plataforma ' \
                                                               'Exchange OWA. Favor de verificar si se tiene ' \
                                                               'conectividad por internet, detalle del mensaje ' \
                                                               'de error : {}'

INICIAR_SESION_MSG_ERROR_EN_PLATAFORMA = 'Inicio de sesion no exitosa dentro de la plataforma Exchange OWA. Se ' \
                                         'presenta el siguiente mensaje de error en la plataforma: {}'

########################################################################################################################
##                               Constantes AccionesHTML obtener_carpetas_en_sesion                                   ##
########################################################################################################################

OBTENER_CARPETAS_EN_SESION_CSS_CARPETA_OWA_2016 = "_n_C4"

OBTENER_CARPETAS_EN_SESION_CSS_CARPETA_OWA_2013 = '_n_Z6'

OBTENER_CARPETAS_EN_SESION_XPATH_CARPETA_OWA_2010 = "//a[@name='lnkFldr']"

OBTENER_CARPETAS_EN_SESION_LOG_INFO_LOCALIZACION_EXITOSA_CARPETAS = 'Se localizan con exito las carpetas por navegar ' \
                                                                    'dentro de la plataforma Exchange OWA, en un ' \
                                                                    'lapso aproximado de {} seg'

OBTENER_CARPETAS_EN_SESION_LOG_ERROR_LOCALIZACION_SIN_EXITO_CARPETAS = 'Localizacion de carpetas sin exito dentro de ' \
                                                                       'la plataforma Exchange OWA. Se realizara ' \
                                                                       'nuevamente el intento de obtencion de carpetas'

OBTENER_CARPETAS_EN_SESION_MOSTRAR_TITLE_AND_URL = 'Titulo actual de la plataforma: {}\nURL actual de la plataforma: {}'

OBTENER_CARPETAS_EN_SESION_LOG_ERROR_LOCALIZACION_SIN_EXITO_CARPETAS_EXCESO_TIEMPO = 'Han transcurrido mas de {} seg ' \
                                                                                     'sin obtener de manera exitosa ' \
                                                                                     'las carpetas dentro de la ' \
                                                                                     'plataforma Exchange OWA'

OBTENER_CARPETAS_EN_SESION_OWA_LOCALIZADO = 'Plataforma OWA version {} identificada'

OBTENER_CARPETAS_EN_SESION_JS_OBTENER_CARPETA_2013 = '''
    var elementos = document.getElementsByClassName('_n_Z6');
    return elementos;
'''

OBTENER_CARPETAS_EN_SESION_JS_OBTENER_CARPETA_2016 = '''
    var elementos = document.getElementsByClassName('_n_C4');
    return elementos;
'''

OBTENER_CARPETAS_EN_SESION_OWA_CARPETA_OBTENIDA = 'Obteniendo la siguiente carpeta dentro de la sesion: {}'

########################################################################################################################
##                               Constantes AccionesHTML navegacion_de_carpetas_por_segundos                          ##
########################################################################################################################

NAVEGACION_CARPETAS_SEG_LOG_ERROR_LISTA_CARPETAS_VACIA = 'Localizacion de carpetas sin exito dentro de la plataforma ' \
                                                         'Exchange OWA.'

NAVEGACION_CARPETAS_SEG_MSG_ERROR_PLATAFORMA_OWA = 'Navegacion de carpetas no exitosa dentro de la plataforma ' \
                                                   'Exchange OWA. Se presenta el siguiente mensaje de error en la ' \
                                                   'plataforma: {}'

NAVEGACION_CARPETAS_SEG_LOG_INFO_NAVEGACION_CARPETAS_FINALIZADA = 'Ha transcurrido un lapso aproximado de 2 ' \
    'minutos, se procede a cerrar la sesion dentro de la plataforma OWA'

NAVEGACION_CARPETAS_SEG_LOG_INFO_INGRESO_CARPETA = 'Ingresando a la carpeta: {}'

NAVEGACION_CARPETAS_SEG_JS_LOCALIZAR_CARPETA_OWA_2016 = '''
    var carpeta = document.querySelector("span._n_C4[title='{}']");
    return carpeta;
'''

NAVEGACION_CARPETAS_SEG_JS_LOCALIZAR_CARPETA_OWA_2013 = '''
    var carpeta = document.querySelector("span._n_Z6[title='{}']");
    return carpeta;
'''

NAVEGACION_CARPETAS_SEG_XPATH_CARPETA_OWA_2010 = '//a[@name="lnkFldr"][@title="{}"]'

NAVEGACION_CARPETAS_SEG_XPATH_CARPETA_OWA_2013 = '//span[contains(@class,"_n_Z6")][@title="{}"]'

NAVEGACION_CARPETAS_SEG_XPATH_CARPETA_OWA_2016 = '//span[contains(@class,"_n_C4")][@title="{}"]'

NAVEGACION_CARPETAS_SEG_LOG_ERROR_STA_ELEM_REF_EXCEP = 'Una de las carpetas no se localiza dentro del DOM de la ' \
                                                   'plataforma OWA, se intentara ingresar nuevamente: {}'

NAVEGACION_CARPETAS_SEG_LOG_ERROR_ELEM_CLICK_INTERCEP_EXCEP = 'No fue posible navegar a la carpeta seleccionada, se ' \
                                                          'tiene un elemento HTML interfiriendo en la navegacion de ' \
                                                          'la carpeta, se intentara ingresar nuevamente: {}'

NAVEGACION_CARPETAS_SEG_LOG_ERROR_NO_SUCH_ELEM_EXCEP = 'No fue posible localizar la carpeta por navegar dentro de la ' \
                                                   'plataforma OWA, se intentara ingresar nuevamente'

NAVEGACION_CARPETAS_SEG_LOG_ERROR_TIMEOUT_EXCEP = 'Se presenta error de tiempo de carga en la plataforma OWA, se ' \
                                              'intentara actualizar la plataforma nuevamente: {}'

NAVEGACION_CARPETAS_SEG_LOG_ERROR_WEBDRIVER_EXCEP = 'Se presenta error del webdriver para la navegacion web dentro ' \
                                                'de la plataforma OWA: {}'

NAVEGACION_CARPETAS_SEG_MSG_ERROR_CREDENCIALES_OWA = 'Navegacion de carpetas e ingreso de bandeja no exitosa dentro ' \
    'de la plataforma Exchange OWA, se presenta el siguiente mensaje de error de credenciales: {}'

NAVEGACION_CARPETAS_SEG_MSG_ERROR_INTENTOS_CLICK = 'No fue posible la navegacion dentro de las carpetas en la ' \
    'plataforma, se tuvo un total de {} intentos fallidos para el ingreso a cada carpeta dentro del buzon.'

########################################################################################################################
##                               Constantes AccionesHTML cerrar_sesion                                                ##
########################################################################################################################

CERRAR_SESION_TITLE_CIERRE_SESION = 'Outlook'

CERRAR_SESION_CIERRE_SESION_ID_BTN_CIERRE_SESION_OWA_2010 = 'lo'

CERRAR_SESION_LOG_ERROR_BTN_CIERRE_SIGN_OUT = 'No se localiza el boton con el texto cierre de sesion, se intentara ' \
                                              'localizar el boton con la leyenda \'Sign out\''

CERRAR_SESION_LOG_INFO_CIERRE_SESION_TITLE_URL = 'Se cierra la sesion, obteniendo el titulo actual de la plataforma: ' \
                                                 '{}\nURL actual de la plataforma: {}'

CERRAR_SESION_LOG_ERROR_NO_SUCH_ELEM_EXCEP = 'Error al cerrar sesion dentro de la plataforma Exchange OWA. No fue ' \
                                             'posible localizar el boton de cierre de sesion dentro de la ' \
                                             'plataforma: {}'

CERRAR_SESION_LOG_ERROR_ELEM_INTERCEP_EXCEP = 'Error al cerrar sesion dentro de la plataforma Exchange OWA. No ' \
                                              'fue posible cerrar la sesion dentro de la plataforma, se tiene un ' \
                                              'elemento HTML interfiriendo el cierre de sesion: {}'

CERRAR_SESION_LOG_ERROR_TIMEOUT_EXCEP = 'Error al cerrar sesion dentro de la plataforma Exchange OWA. No fue posible ' \
                                        'cerrar la sesion dentro de la plataforma del OWA, se presenta un error de ' \
                                        'tiempo de carga dentro de la plataforma: {}'

CERRAR_SESION_LOG_ERROR_WEBDRIVER_EXCEP = 'Error al cerrar sesion dentro de la plataforma Exchange OWA. Se presenta ' \
                                          'un error de comunicacion con el webdriver de navegacion para la ' \
                                          'plataforma OWA: {}'

CERRAR_SESION_LOG_ERROR_ATRIBUTE_ERROR_EXCEP = 'Error al cerrar sesion dentro de la plataforma Exchange OWA. No fue ' \
                                               'posible localizar el boton de cierre de sesion dentro de la ' \
                                               'plataforma'

CERRAR_SESION_ERROR_PLATAFORMA = 'Error al cerrar sesion dentro de la plataforma Exchange OWA. Se presenta el ' \
                                 'siguiente error dentro de la plataforma: {}'

CERRAR_SESION_LOG_INFO_CIERRE_WEB_DRIVER = 'Prueba UX OWA finalizada, se procede a cerrar el webdriver'

CERRAR_SESION_LOG_INFO_CIERRE_SESION_EXITOSA = 'Se cierra con exito la sesion dentro de la plataforma Exchange OWA'

CERRAR_SESION_MSG_ERROR_CREDENCIALES_OWA = 'Cierre de sesion sin exito dentro de la plataforma Exchange OWA, se ' \
    'presenta el siguiente mensaje de error de credenciales: {}'

CERRAR_SESION_BTN_PERFIL_USUARIO_OWA_2013 = '//div[@class="_hl_d"]'

CERRAR_SESION_BTN_PERFIL_USUARIO_OWA_2016 = '//div[contains(@class,"ms-Icon--person")]'

CERRAR_SESION_BTN_XPATH_CIERRE_SESION_OWA_2016_SPANISH = '//span[text()="Cerrar sesi\u00f3n"]'

CERRAR_SESION_BTN_XPATH_CIERRE_SESION_OWA_2016_ENGLISH = '//span[text()="Sign out"]'

CERRAR_SESION_BTN_XPATH_CIERRE_SESION_OWA_2013 = '//span[text()="Cerrar sesi\u00f3n"]'


