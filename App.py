from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from playwright.sync_api import sync_playwright
from werkzeug.utils import secure_filename
from scripts.manipulaTabela import leTabela
from scripts.loginSda import loginSda
from scripts.transferenciaBem import transfereBem, caminhoTransferencia
from Usuario import Usuario
from Transferencia import Transferencia
import os
from Banco import Banco
from datetime import datetime
from time import sleep

app = Flask(__name__)
app.secret_key = 'XXXXXXXXXXX'  # IMPORTANTE

usuario = Usuario()
transferencia = Transferencia()
banco = Banco()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        req = request.form
        usuario_rede = req['usuario_rede']
        senha = request.form['senha']

        if usuario_rede is not None:
            usuario.set_usuario(usuario_rede)
            usuario.set_senha(senha)

        # if o usuario estiver em uma lista de usuarios permitidos deixe passar
        permissao = banco.verifica_permissao(f'{usuario_rede}-{senha}')

        if permissao:
            usuario.set_permitido(permissao)
            flash('Você está logado!', 'notice')
            return redirect(url_for('cadastro'))
        else:
            flash('Usuário não autorizado!', 'error')

    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():

    if (usuario.get_permitido() != True):
        return redirect(url_for('login'))

    if request.method == 'POST' and (request.form.get('form_name') == 'form_cadastro_modelo'):
        req = request.form
        modelo = req['cadastro_modelo']

        banco.inserir_modelo(modelo)


    if request.method == 'POST' and (request.form.get('form_name') == 'form_cadastro'):
        req = request.form

        # CADASTRO NO BANCO
        patrimonio = req['patrimonio']
        modelo = req.get('modelo')
        numero_serie = req['numeroSerie']
        imei_um = req['imei1']
        imei_dois = req['imei2']
        setor_siape_nome = req.get('campo-busca')

        if not ' - ' in setor_siape_nome: #setor_siape_nome not in:
            flash('Siape / Setor inválido!', 'warning')
            return render_template('cadastro.html')
        elif not modelo in f'{banco.obter_modelo()}':
            flash('Modelo não cadastrado!', 'warning')
            return render_template('cadastro.html')

        id_nome = setor_siape_nome.split(' - ')
        setor_siape = id_nome[0]
        nome = id_nome[1]

        estado = req['estado']
        localizacao = req['localizacao']
        defeito = req['defeito']
        observacao = req['observacoes']

        #Lista de treansferencia para o SDA
        transferencia.adicionar_bem(patrimonio, modelo, numero_serie, imei_um, imei_dois, nome, setor_siape, estado, localizacao, defeito, observacao)
        flash('Bem adicionado a Lista', 'info')

    if request.method == 'POST' and (request.form.get('form_name') == 'form_cadastro_lote'):

        if 'file' not in request.files:
            return 'Arquivo não foi fornecido', 400

        file = request.files['file']

        if file.filename == '':
            return 'Você não selecionou nenhum arquivo', 400

        if file:
            # CADASTRO EM LOTE NO BANCO
            filename = secure_filename(file.filename)
            UPLOAD_FOLDER = os.path.abspath('UPLOAD_FOLDER')

            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            data_frame = leTabela(filename)
            num_linhas = len(data_frame.index)

            for n in range(num_linhas):
                linha = data_frame.loc[n]

                patrimonio = str(linha['patrimonio'])
                modelo = str(linha['modelo'])
                numero_serie = str(linha['num_serie'])
                imei_um = str(linha['imei_um'])
                imei_dois = str(linha['imei_dois'])
                nome = str(linha['nome'])
                setor_siape = str(linha['setor_siape'])
                estado = str(linha['estado'])
                localizacao = str(linha['localizacao'])
                defeito = str(linha['defeito'])
                observacao = str(linha['observacao'])

                print(patrimonio)

                transferencia.adicionar_bem(patrimonio, modelo, numero_serie, imei_um, imei_dois, nome, setor_siape, estado, localizacao, defeito, observacao)


    if request.method == 'POST' and (request.form.get('form_name') == 'form_cadastro_finalizar'):
        # CADASTRO NO SDA
        lista_bens = transferencia.get_listaBens()
        print(lista_bens)
        if len(lista_bens) > 0:
            flash('Adicionando itens no SDA...', 'info')
        else:
            flash('Não há itens para serem reistrados!', 'warning')
        erro_bens = []

        if len(lista_bens) > 0:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                try:
                    page.goto("https://www.com.br")
                except:
                    sleep(5)
                    try:
                        page.goto("https://www.com.br")
                    except:
                        pass

                usuario_rede = usuario.get_usuario()
                senha = usuario.get_senha()

                sucessoLoginSda = loginSda(page, usuario_rede, senha)

                if sucessoLoginSda:
                    sucessoCaminhoTranferencia = caminhoTransferencia(page)
                    if sucessoCaminhoTranferencia:
                        for bem in lista_bens:
                            print(bem.get_patrimonio())
                            patrimonio = bem.get_patrimonio()
                            setor_siape = bem.get_setor_siape()
                            estado = bem.get_estado()

                            if len(setor_siape) >= 6:
                                tipo_setor_siape = 'siape'  # Temporario até ter a lista da galera
                            else:
                                tipo_setor_siape = 'setor'

                            sucessoRegistraSda = transfereBem(page, patrimonio, setor_siape, tipo_setor_siape, estado)
                            if sucessoRegistraSda:

                                patrimonio, modelo, numero_serie, imei_um, imei_dois, nome, setor_siape, estado, localizacao, defeito, observacao = \
                                    bem.get_patrimonio(), bem.get_modelo(), bem.get_numero_serie(), bem.get_imei_um(), bem.get_imei_dois(), bem.get_nome(), bem.get_setor_siape(), \
                                    bem.get_estado(), bem.get_localizacao(), bem.get_defeito(), bem.get_observacao()
                                data = datetime.now().strftime('%d/%m/%Y')

                                banco.inserir_patrimonio(patrimonio, modelo, numero_serie, imei_um, imei_dois, setor_siape, estado, localizacao, defeito, observacao)
                                banco.registrar_transferencia(f'{patrimonio} - {modelo} - {numero_serie} - {imei_um} - {imei_dois} - {setor_siape} - {nome} - {estado} - {localizacao} - {defeito} - {observacao} - {data}')
                                flash('Bem registrado com sucesso!', 'notice')

                            else:
                                flash(f'Erro ao fazer transferência no SDA!<br>Patrimônio: {bem.get_patrimonio()}<br>'
                                      f'Modelo: {bem.get_modelo()}<br>Nome: {bem.get_nome()}', 'error')
                                erro_bens.append(bem)


                        transferencia.set_listaBens([])
                else:
                    flash('Erro ao fazer login no SDA!', 'error')

                browser.close()

    return render_template('cadastro.html')

@app.route('/consulta', methods=['GET', 'POST'])
def consulta():
    if (usuario.get_permitido() != True):
        return redirect(url_for('login'))
    return render_template('consulta.html')

@app.route('/alterar_senha', methods=['GET', 'POST'])
def alterar_senha():
    if (usuario.get_permitido() != True):
        return redirect(url_for('login'))

    if request.method == 'POST':
        req = request.form
        usuario_rede = req['usuario_rede']
        senha_atual = request.form['senha_atual']
        nova_senha = request.form['nova_senha']

        if senha_atual == usuario.get_senha():
            banco.atualiza_senha(usuario_rede, nova_senha)

    return render_template('alterar_senha.html')

@app.route('/adicionar_usuario', methods=['GET', 'POST'])
def adicionar_usuario():
    if (usuario.get_permitido() != True):
        return redirect(url_for('login'))

    if request.method == 'POST':
        req = request.form
        novo_usuario = req['usuario']
        senha = request.form['senha']
        banco.adiciona_usuario(f'{novo_usuario}-{senha}')


    return render_template('adicionar_usuario.html')

@app.route('/api/carrega_opcoes')
def get_carrega_opcoes():
    opcoes = banco.obter_modelo()
    return jsonify(opcoes)

@app.route('/api/opcoes')
def get_opcoes():
    opcoes = banco.obter_funcionario_setor()
    return jsonify(opcoes)

@app.route('/api/patrimonio')
def get_patrimonio():
    opcoes = banco.obter_dados_patrimonio()
    return jsonify(opcoes)

@app.route('/api/log_transferencia')
def get_log_transferencia():
    opcoes = banco.obter_log_transferencia()
    return jsonify(opcoes)

@app.route('/api/lista_transferencia')
def get_lista_transferencia():
    lista_bens = transferencia.get_listaBens()
    lista = []
    for bem in lista_bens:
        linha = {'patrimonio': f'{bem.get_patrimonio()}', 'modelo': f'{bem.get_modelo()}', 'nome': f'{bem.get_nome()}'}
        lista.append(linha)
    return jsonify(lista)

if __name__ == '__main__':
    app.run(port=9090)
