from InfoTranferencia import InfoTranferencia
class Transferencia:
    def __init__(self):
        self._lista_bens = []

    def set_listaBens(self, lista):
        self._lista_bens = lista

    def get_listaBens(self):
        return self._lista_bens

    def adicionar_bem(self, patrimonio, modelo, numero_serie, imei_um, imei_dois, nome, setor_siape, estado, localizacao, defeito, observacao):
        bem = InfoTranferencia()

        bem.set_patrimonio(patrimonio)
        bem.set_modelo(modelo)
        bem.set_numero_serie(numero_serie)
        bem.set_imei_um(imei_um)
        bem.set_imei_dois(imei_dois)
        bem.set_nome(nome)
        bem.set_setor_siape(setor_siape)
        bem.set_estado(estado)
        bem.set_localizacao(localizacao)
        bem.set_defeito(defeito)
        bem.set_observacao(observacao)

        self._lista_bens.append(bem)

