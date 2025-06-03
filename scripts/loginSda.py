def loginSda(page, usuario, senha):
    try:
        # Preencha o campo de usuário
        page.fill('[name="frmPortal-conteudo:j_idt131"]', usuario)

        # Preencha o campo de senha
        page.fill('[name="frmPortal-conteudo:cmpSenha"]', senha)

        # Clique no botão de login
        page.click('button[name="frmPortal-conteudo:j_idt140"]')

        try:
            page.click('button[name="frmPortal-conteudo:btnLogar"]')
        except:
            pass
        page.get_by_text("Bens Móveis")
        return True
    except:
        return False


