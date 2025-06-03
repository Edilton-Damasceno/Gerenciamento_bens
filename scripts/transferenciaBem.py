from time import sleep
from datetime import datetime

data = datetime.now().strftime('%d%m%Y')

def caminhoTransferencia(page):
    try:
        # Chegando na tranferência
        page.get_by_text("Bens Móveis").click()
        page.locator('[id="frmPortal:BM_BEM_MOV:hdr"]').get_by_text("Bem móvel").click()
        page.locator('[id="frmPortal:BM_TRANS"]').get_by_text("Transferência").click()
        return True
    except:
        return False

def transfereBem(page, patrimonio, siape_setor, tipo_setor_siape, conservacao):
    try:
        # Preenchendo
        page.fill('[name="frmPortal:j_idt133"]', patrimonio)
        page.keyboard.press("Tab")
        sleep(4)
        page.click('input[name="frmPortal:j_idt140InputDate"]')
        page.keyboard.type(data)

        if tipo_setor_siape.lower() == 'siape':
            page.locator('[id="frmPortal:subscriptions"]').get_by_text(" Siape").click()  # Siape
            sleep(2)
            page.fill('[name="frmPortal:j_idt149Input"]', siape_setor)
            page.keyboard.press("Tab")
            sleep(3)

        else:
            page.locator('[id="frmPortal:subscriptions"]').get_by_text(" Setor").click()  # Setor
            page.fill('[name="frmPortal:j_idt158Input"]', siape_setor)
            page.keyboard.press("Tab")
            sleep(3)

        page.click('select[name="frmPortal:conservacao"]')  # Conservação

        if conservacao == 'Bom':
            page.locator('[id="frmPortal:conservacao"]').select_option("Bom")
        elif conservacao == 'Péssimo':
            page.locator('[id="frmPortal:conservacao"]').select_option("Péssimo")
        else:
            page.locator('[id="frmPortal:conservacao"]').select_option("Regular")

        page.keyboard.press("Escape")

        # Botão de clique para salvar
        page.keyboard.press("Tab")
        page.keyboard.press("Enter")
        sleep(3)

        return True
    except:
        return False