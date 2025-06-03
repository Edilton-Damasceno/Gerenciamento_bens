class Usuario:
    def __init__(self):
        self._usuario = None
        self._senha = None
        self._permitido = None
        self._lista_bens = []

    def get_usuario(self):
        return self._usuario

    def set_usuario(self, usuario):
        self._usuario = usuario

    def get_senha(self):
        return self._senha

    def set_senha(self, senha):
        self._senha = senha

    def get_permitido(self):
        return self._permitido

    def set_permitido(self, bool):
        self._permitido = bool

