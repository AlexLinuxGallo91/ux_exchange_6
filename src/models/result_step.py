from src.utils.temporizador import Temporizador


class ResultStep:

    def __init__(self):
        self.validacion_correcta = False
        self.mensaje_error = ''
        self.tiempo_inicio_de_ejecucion = 0
        self.tiempo_fin_de_ejecucion = 0
        self.tiempo_total_de_la_ejecucion = 0
        self.datetime_inicial = ''
        self.datetime_final = ''
        self.numero_intentos_fallidos_reingreso_portal = 0

        # bandera en caso de tener error por credenciales
        self.error_inicio_de_sesion_credenciales_erroneas = False

        # mensaje obteniedo en caso de tener error de credenciales
        self.msg_error_de_credenciales = ''

        # banderas en caso de haber realizado n intentos para ingresar a la bandeja de entrada
        self.error_plataforma_inicio_de_sesion = False
        self.error_plataforma_navegacion_entre_carpetas = False
        self.error_plataforma_cierre_de_sesion = False


    def establecer_tiempo_de_ejecucion(self):
        tiempo_inicial = self.tiempo_inicio_de_ejecucion
        tiempo_final = self.tiempo_fin_de_ejecucion
        self.tiempo_total_de_la_ejecucion = tiempo_final - tiempo_inicial

    def inicializar_tiempo_de_ejecucion(self):
        self.datetime_inicial = Temporizador.obtener_fecha_tiempo_actual()
        self.tiempo_inicio_de_ejecucion = Temporizador.obtener_tiempo_timer()

    def finalizar_tiempo_de_ejecucion(self):
        self.datetime_final = Temporizador.obtener_fecha_tiempo_actual()
        self.tiempo_fin_de_ejecucion = Temporizador.obtener_tiempo_timer()
        self.establecer_tiempo_de_ejecucion()

    def __str__(self):
        cadena = ''
        cadena += 'validacion_correcta : {self.validacion_correcta}\n'.format(self=self)
        cadena += 'mensaje_error : {self.mensaje_error}\n'.format(self=self)
        cadena += 'tiempo_inicio_de_ejecucion : {self.tiempo_inicio_de_ejecucion}\n'.format(self=self)
        cadena += 'tiempo_fin_de_ejecucion : {self.tiempo_fin_de_ejecucion}\n'.format(self=self)
        cadena += 'tiempo_total_de_la_ejecucion : {self.tiempo_total_de_la_ejecucion}\n'.format(self=self)
        cadena += 'datetime_inicial : {self.datetime_inicial}\n'.format(self=self)
        cadena += 'datetime_final : {self.datetime_final}\n'.format(self=self)
        cadena += 'numero_intentos_fallidos_reingreso_portal : {self.numero_intentos_fallidos_reingreso_portal}\n'.\
            format(self=self)

        return cadena
