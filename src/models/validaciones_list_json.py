from src.models.result_step import ResultStep


class ValidacionResultList:

    def __init__(self):
        self.result_tiempo_de_ejecucion = ResultStep()

        # establece el tiempo de inicio de ejecucion
        self.result_validacion_ingreso_url = ResultStep()
        self.result_validacion_acceso_portal_owa = ResultStep()
        self.result_validacion_navegacion_carpetas = ResultStep()
        self.result_validacion_cierre_sesion = ResultStep()

    def __str__(self):
        v_url = 'validacion url: {}'.format(self.result_validacion_ingreso_url.validacion_correcta)

        v_portal_owa = 'validacion ingreso portal owa {}'.format(
            self.result_validacion_acceso_portal_owa.validacion_correcta)

        v_n_carpetas = 'validacion navegacion carpetas: {}'.format(
            self.result_validacion_navegacion_carpetas.validacion_correcta)

        v_cierre_sesion = 'validacion cierre sesion: {}'.format(
            self.result_validacion_cierre_sesion.validacion_correcta)

        return '{}\n{}\n{}\n{}\n'.format(v_url, v_portal_owa, v_n_carpetas, v_cierre_sesion)
