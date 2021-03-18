class Correo:

    def __init__(self, correo, password, url):
        self.correo = correo
        self.password = password
        self.url = url

    def obtener_cuenta_correo_sin_dominio(self):
        if self.correo is None:
            return ''
        else:
            return self.correo.split('@')[0]

    def __str__(self):
        return 'url; {}, correo: {}, password: {}'.format(self.url, self.correo, self.password)

    def __repr__(self):
        return self.__str__()
