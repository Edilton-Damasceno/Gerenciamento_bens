import sqlite3

class Banco:
    def __init__(self):
        self._lista_bens = []

    def open_db(self):
        conn = sqlite3.connect('banco_gerenciamento_bem.db')
        cursor = conn.cursor()
        return conn, cursor

    def close(self, conn, cursor):
        # Confirmar as mudanças
        conn.commit()
        # Fechar o cursor
        cursor.close()
        # Fechar a conexão
        conn.close()

    def inserir_modelo(self, modelo):
        conn, cursor = self.open_db()

        cursor.execute(f'''
        INSERT INTO modelos (nome) VALUES ('{modelo}')
        ''')
        self.close(conn, cursor)

    def registrar_transferencia(self, transferencia):
        conn, cursor = self.open_db()

        cursor.execute(f'''
           INSERT INTO log_transferencia (registro) VALUES ('{transferencia}')
           ''')
        self.close(conn, cursor)


    def inserir_patrimonio(self, patrimonio, modelo, numero_serie, imei_um, imei_dois, setor_siape, estado, localizacao, defeito, observacao):
        conn, cursor = self.open_db()

        cursor.execute('''
            UPDATE patrimonio
            SET id_modelo = ?, num_serie = ?, imei_um = ?, imei_dois = ?, num_siape_setor = ?, estado_do_bem = ?, localizacao = ?, defeito = ?, observacao = ?
            WHERE num_patrimonio = ?
            ''', (modelo, numero_serie, imei_um, imei_dois, setor_siape, estado, localizacao, defeito, observacao, patrimonio))

        if cursor.rowcount == 0:
            # Se não foi, então o ID não existe, então insira um novo registro
            cursor.execute('''
                INSERT INTO patrimonio (num_patrimonio, id_modelo, num_serie, imei_um, imei_dois, num_siape_setor, estado_do_bem, localizacao, defeito, observacao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (patrimonio, modelo, numero_serie, imei_um, imei_dois, setor_siape, estado, localizacao, defeito, observacao))

        self.close(conn, cursor)

    def obter_modelo(self):
        conn, cursor = self.open_db()
        lista_modelo = []

        cursor.execute('''
        SELECT * FROM modelos
        ''')

        resultados = cursor.fetchall()

        for linha in resultados:
            modelo = {'value': f'{linha[0]}', 'text': f'{linha[1]}'}
            lista_modelo.append(modelo)

        self.close(conn, cursor)
        return lista_modelo

    def obter_funcionario_setor(self):
        conn, cursor = self.open_db()
        lista_funcionario_setor = []

        cursor.execute("SELECT * FROM funcionarios_setores")
        opcoes = cursor.fetchall()

        for linha in opcoes:
            modelo = {'value': f'{linha[0]}', 'text': f'{linha[0]} - {linha[1]}'}
            lista_funcionario_setor.append(modelo)

        self.close(conn, cursor)
        return lista_funcionario_setor

    def obter_dados_patrimonio(self):
        conn, cursor = self.open_db()
        cursor.execute("SELECT * FROM patrimonio")
        rows = cursor.fetchall()
        self.close(conn, cursor)
        return [dict(patrimonio=row[0], modelo=row[1], numero_serie=row[2], imei_um=row[3], imei_dois=row[4],
                     setor_siape=row[5], estado=row[6], localizacao=row[7], defeito=row[8], observacao=row[9]) for row in rows]

    def obter_log_transferencia(self):
        conn, cursor = self.open_db()
        cursor.execute("SELECT * FROM log_transferencia")
        rows = cursor.fetchall()
        self.close(conn, cursor)
        lista = []
        for row in rows:
            row = row[1].split(' - ')
            lista.append(dict(patrimonio=row[0], modelo=row[1], numero_serie=row[2], imei_um=row[3], imei_dois=row[4],
                setor_siape=row[5], nome=row[6], estado=row[7], localizacao=row[8], defeito=row[9], observacao=row[10], data=row[11]))
        return lista

    def obter_nome_funcionario_setor(self):
        conn, cursor = self.open_db()
        lista_nome = []

        cursor.execute('''
                SELECT nome FROM funcionarios_setores
                ''')

        resultados = cursor.fetchall()

        for linha in resultados:
            nome = {'value': '1', 'text': f'{linha[0]}'}
            lista_nome.append(nome)

        self.close(conn, cursor)
        return lista_nome

    def atualiza_senha(self, usuario, senha):
        conn, cursor = self.open_db()
        print(usuario)
        cursor.execute(f'''
            UPDATE usuarios
            SET usuario = ?
            WHERE usuario LIKE "{usuario}%"
            ''', (f'{usuario}-{senha}',))

        self.close(conn, cursor)

    def adiciona_usuario(self, usuario):
        conn, cursor = self.open_db()
        cursor.execute(f'''
                INSERT INTO usuarios (usuario) VALUES ('{usuario}')
                ''')
        self.close(conn, cursor)

    def verifica_permissao(self, usuario):
        conn, cursor = self.open_db()

        cursor.execute('''
                SELECT * FROM usuarios
                ''')
        resultados = cursor.fetchall()
        for linha in resultados:

            if usuario == linha[1]:
                return True

        self.close(conn, cursor)
        return False



