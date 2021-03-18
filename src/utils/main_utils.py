import configparser
from os.path import exists


class UtilsMain:

    @staticmethod
    def verificacion_correcta_archivo_config(archivo_config: configparser.ConfigParser):
        """
        Funcion el cual permite verificar que el archivo config.ini contenga todos los parametros necesarios. En caso
        de que contenga las secciones y keys establecidos, la funcion devolvera True, en caso contrario regresara False

        :return:
        """
        validacion_total = True

        bool_ruta = archivo_config.has_option('Driver', 'ruta')
        bool_web_driver = archivo_config.has_option('Driver', 'driverPorUtilizar')
        bool_headless = archivo_config.has_option('Driver', 'headless')
        bool_log_path_dev_null = archivo_config.has_option('Driver', 'log_path_dev_null')

        if not bool_ruta:
            print('Favor de establecer el path del webdriver a utilizar dentro del archivo config.ini')
            validacion_total = False
        elif not bool_web_driver:
            print('Favor de establecer el tipo/nombre del webdriver a utilizar dentro del archivo config.ini')
            validacion_total = False
        elif not bool_headless:
            print('Favor de establecer la opcion/configuracion headless dentro del archivo config.ini')
            validacion_total = False
        elif not bool_log_path_dev_null:
            print('Favor de establecer la opcion/configuracion log_path_dev_null dentro del archivo config.ini')
            validacion_total = False

        return validacion_total

    @staticmethod
    def verificar_si_path_archivo_existe(path_por_analizar):
        return exists(path_por_analizar)
