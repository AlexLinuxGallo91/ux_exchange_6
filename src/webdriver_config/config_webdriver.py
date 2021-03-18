from selenium import webdriver
from src.evaluacion_json import constantes_json
import src.webdriver_config.constantes_configuracion_web_driver as constantes_config_webdriver
import warnings
import sys
from src.utils.format_utils import FormatUtils
from src.utils.main_utils import UtilsMain


class ConfiguracionWebDriver:

    def __init__(self, ruta_web_driver, driver_por_configurar):
        self.ruta_web_driver = ruta_web_driver
        self.driver_por_configurar = driver_por_configurar

    def inicializar_webdriver_phantom_js(self):

        arg_webdriver_service_args = ['--ignore-ssl-errors=true', '--ssl-protocol=any']

        # suprime el mensaje warning del uso de phantomjs ya que es una libreria obsoleta
        warnings.filterwarnings('ignore')

        try:
            webdriver_phantomjs = webdriver.PhantomJS(service_args=arg_webdriver_service_args,
                                                      executable_path=self.ruta_web_driver,
                                                      service_log_path=constantes_json.DEV_NULL)

            webdriver_phantomjs.set_window_size(1120, 550)

        except FileNotFoundError as e:
            print('Sucedio un error al intentar configurar el webdriver: {}'.format(e))
            sys.exit()

        except Exception as e:
            print('Sucedio una excepcion al intentar configurar el webdriver {}'.format(e))
            sys.exit()

        return webdriver_phantomjs

    # inicializa un nuevo driver (firefox) para la experiencia de usuario con el uso del navegador Mozilla Firefox
    def inicializar_webdriver_firefox(self):

        archivo_config_ini = FormatUtils.obtener_archivo_de_configuracion()
        modo_headless = archivo_config_ini.getboolean('Driver', 'headless')
        mandar_log_a_dev_null = archivo_config_ini.getboolean('Driver', 'log_path_dev_null')

        mime_types = 'application/zip,application/octet-stream,image/jpeg,application/vnd.ms-outlook,' \
                     'text/html,application/pdf'

        # ruta para deshabilitar log inecesario del geckodriver
        opciones_firefox = webdriver.FirefoxOptions()
        perfil_firefox = webdriver.FirefoxProfile()

        firefox_capabilities = webdriver.DesiredCapabilities().FIREFOX.copy()
        firefox_capabilities.update({'acceptInsecureCerts': True, 'acceptSslCerts': True})
        firefox_capabilities['acceptSslCerts'] = True

        # ignora las certificaciones de seguridad, esto solamente se realiza para la experiencia de usuario
        opciones_firefox.add_argument('--ignore-certificate-errors')
        opciones_firefox.accept_insecure_certs = True
        perfil_firefox.accept_untrusted_certs = True
        perfil_firefox.assume_untrusted_cert_issuer = False
        perfil_firefox.set_preference("browser.download.folderList", 2)
        perfil_firefox.set_preference("browser.download.manager.showWhenStarting", False)
        perfil_firefox.set_preference("browser.helperApps.alwaysAsk.force", False)
        perfil_firefox.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)

        opciones_firefox.headless = modo_headless

        if mandar_log_a_dev_null:
            param_log_path = constantes_json.DEV_NULL
        else:
            param_log_path = None

        try:
            webdriver_firefox = webdriver.Firefox(executable_path=self.ruta_web_driver,
                                                  firefox_options=opciones_firefox,
                                                  firefox_profile=perfil_firefox,
                                                  capabilities=firefox_capabilities,
                                                  log_path=param_log_path)

        except FileNotFoundError as e:
            print('Sucedio un error al intentar configurar el webdriver: {}'.format(e))
            sys.exit()

        except Exception as e:
            print('Sucedio una excepcion al intentar configurar el webdriver {}'.format(e))
            sys.exit()

        return webdriver_firefox

    # inicializa un nuevo driver (chrome driver) para la experiencia de usuario con el uso del navefador google chrome
    def inicializar_webdriver_chrome(self):

        archivo_config_ini = FormatUtils.obtener_archivo_de_configuracion()
        modo_headless = archivo_config_ini.getboolean('Driver', 'headless')
        mandar_log_a_dev_null = archivo_config_ini.getboolean('Driver', 'log_path_dev_null')

        opciones_chrome = webdriver.ChromeOptions()

        # ignora las certificaciones de seguridad, esto solamente se realiza para la experiencia de usuario
        opciones_chrome.add_argument('--ignore-certificate-errors')
        opciones_chrome.add_argument('--allow-running-insecure-content')
        opciones_chrome.add_argument("--enable-javascript")
        opciones_chrome.add_argument('window-size=1920x1080')
        opciones_chrome.add_argument('--no-sandbox')

        # establece el modo headless, esto dependiendo de la opcion que se tenga en el archivo config.ini
        if modo_headless:
            opciones_chrome.add_argument("--headless")

        opciones_chrome.add_experimental_option('excludeSwitches', ['enable-logging'])

        chrome_capabilities = webdriver.DesiredCapabilities().CHROME.copy()
        chrome_capabilities['acceptSslCerts'] = True
        chrome_capabilities['acceptInsecureCerts'] = True

        # establece el directorio al cual se redireccionara el log generado por el chromedriver
        if mandar_log_a_dev_null:
            param_service_log_path = constantes_json.DEV_NULL
        else:
            param_service_log_path = None

        try:
            webdriver_chrome = webdriver.Chrome(self.ruta_web_driver,
                                                chrome_options=opciones_chrome,
                                                desired_capabilities=chrome_capabilities,
                                                service_log_path=param_service_log_path)

        except FileNotFoundError as e:
            print('Sucedio un error al intentar configurar el webdriver: {}'.format(e))
            sys.exit()

        except Exception as e:
            print('Sucedio una excepcion al intentar configurar el webdriver {}'.format(e))
            sys.exit()

        return webdriver_chrome

    def configurar_obtencion_web_driver(self):

        # verifica que el parametro del directorio del webdriver se encuentre establecido y sea un directorio valido
        if len(self.ruta_web_driver.strip()) == 0 or not UtilsMain.verificar_si_path_archivo_existe(
                self.ruta_web_driver.strip()):
            print(constantes_config_webdriver.MSG_ERROR_PROP_INI_WEBDRIVER_SIN_CONFIGURAR)
            sys.exit()

        if len(self.ruta_web_driver.strip()) == 0:
            print(constantes_config_webdriver.MSG_ERROR_PROP_INI_WEBDRIVER_SIN_CONFIGURAR)
            sys.exit()

        elif self.driver_por_configurar == constantes_config_webdriver.CHROME:
            driver_configurado = self.inicializar_webdriver_chrome()

        elif self.driver_por_configurar == constantes_config_webdriver.FIREFOX:
            driver_configurado = self.inicializar_webdriver_firefox()

        elif self.driver_por_configurar == constantes_config_webdriver.PHANTOMJS:
            driver_configurado = self.inicializar_webdriver_phantom_js()

        else:
            print(constantes_config_webdriver.MSG_ERROR_CONFIGURACION_DRIVER)
            sys.exit()

        return driver_configurado
