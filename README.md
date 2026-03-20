# Sistema de Gerenciamento de Bens Móveis

Solução em Flask para registrar informações adicionais de bens móveis, automatizar o processo de transferência em um sistema externo (SDA) e manter um histórico local.

## Visão Geral

Este sistema permite que os usuários gerenciem bens móveis, cadastrando detalhes como número de patrimônio, modelo, número de série, IMEIs, responsável/setor, estado do bem, localização, defeitos e observações. Uma funcionalidade chave é a capacidade de registrar essas informações e, em seguida, automatizar a transferência desses bens no sistema SDA (Sistema de Distribuição de Ativos) utilizando a biblioteca Playwright para interação web. O sistema também mantém um banco de dados local (SQLite) para persistência dos dados e logs de transferência.

## Funcionalidades Principais

* **Autenticação de Usuários:** Sistema de login para acesso restrito.
* **Cadastro de Bens:**
    * **Individual:** Formulário para adicionar informações detalhadas de um bem.
    * **Em Lote:** Upload de arquivo (presumivelmente Excel/CSV, processado por `pandas`) para cadastro de múltiplos bens.
    * **Cadastro de Modelos:** Permite adicionar novos modelos de bens que podem ser associados aos patrimônios.
* **Integração com SDA:**
    * Automatiza o login no sistema SDA.
    * Navega até a seção de transferência de bens no SDA.
    * Registra a transferência dos bens cadastrados no sistema SDA.
* **Consultas e Relatórios:**
    * Visualização dos bens cadastrados no banco de dados local.
    * Log de todas as transferências realizadas e registradas no sistema.
    * Visualização da lista de bens atualmente na fila para transferência.
* **Gerenciamento de Usuários (Básico):**
    * Adição de novos usuários com permissão de acesso.
    * Alteração da própria senha pelo usuário logado.
* **Banco de Dados Local:** Utiliza SQLite para armazenar:
    * Informações dos patrimônios.
    * Modelos de bens.
    * Usuários e suas credenciais (de forma simplificada).
    * Logs de transferência.
    * Informações de funcionários/setores (para associação aos bens).

## Pré-requisitos

1.  **Python:** Versão 3.7 ou superior recomendada.
2.  **pip:** Gerenciador de pacotes do Python.
3.  **Navegador Web:** Um navegador moderno como Chrome/Chromium, Firefox ou WebKit para que o Playwright possa interagir com o sistema SDA. Os drivers correspondentes serão instalados pelo Playwright.
4.  **Acesso ao Sistema SDA:** Credenciais válidas para o sistema externo onde as transferências são realizadas.

## Instalação

1.  **Clone o Repositório (ou extraia os arquivos):**
    ```bash
    # Se estiver usando git
    git clone <url_do_repositorio>
    cd gerenciamento_bens
    ```
    Ou simplesmente navegue até a pasta onde os arquivos (`App.py`, `Banco.py`, etc.) estão localizados.

2.  **Crie e Ative um Ambiente Virtual (Recomendado):**
    ```bash
    python -m venv venv
    # No Windows
    venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```

3.  **Instale as Dependências:**
    Navegue até a pasta do projeto (que contém `requirements.txt`) e execute:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Instale os Navegadores para o Playwright:**
    Este comando fará o download dos navegadores necessários para o Playwright.
    ```bash
    playwright install
    ```
    (Pode ser necessário `python -m playwright install` ou `python3 -m playwright install` dependendo da sua configuração).

5.  **Configuração do Banco de Dados:**
    O sistema utiliza um banco de dados SQLite chamado `banco_gerenciamento_bem.db`. O arquivo `Banco.py` tentará se conectar a este banco.
    **Importante:** O script `Banco.py` *não* cria as tabelas se elas não existirem. Você precisará criar a estrutura inicial do banco de dados. Um schema básico, inferido do código, seria:

    ```sql
    CREATE TABLE IF NOT EXISTS modelos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS patrimonio (
        num_patrimonio TEXT PRIMARY KEY,
        id_modelo INTEGER, -- Ou TEXT, dependendo de como os modelos são referenciados
        num_serie TEXT,
        imei_um TEXT,
        imei_dois TEXT,
        num_siape_setor TEXT,
        estado_do_bem TEXT,
        localizacao TEXT,
        defeito TEXT,
        observacao TEXT,
        FOREIGN KEY (id_modelo) REFERENCES modelos(id) -- Ajuste se id_modelo for TEXT
    );

    CREATE TABLE IF NOT EXISTS log_transferencia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        registro TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS funcionarios_setores (
        id_funcionario_setor TEXT PRIMARY KEY, -- Ex: SIAPE ou código do setor
        nome TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE -- Armazena no formato "nomeusuario-senha"
    );
    ```
    Você pode usar uma ferramenta de gerenciamento SQLite (como DB Browser for SQLite) para criar o arquivo `banco_gerenciamento_bem.db` e executar esses comandos SQL para criar as tabelas.

6.  **Configurações da Aplicação:**
    * **Chave Secreta do Flask:** Em `App.py`, altere `app.secret_key = 'XXXXXXXXXXX'` para uma chave secreta forte e única.
    * **URL do SDA:** Em `App.py`, a URL `page.goto("https://www.com.br")` é um placeholder. Atualize-a para a URL correta do sistema SDA.

## Executando a Aplicação

1.  Certifique-se de que seu ambiente virtual está ativado.
2.  Navegue até o diretório raiz do projeto (onde `App.py` está localizado).
3.  Execute o comando:
    ```bash
    python App.py
    ```
4.  Abra seu navegador e acesse `http://127.0.0.1:9090/`.

## Estrutura do Projeto (Principais Arquivos)

* `App.py`: Arquivo principal da aplicação Flask, contém as rotas e a lógica de controle.
* `Banco.py`: Classe para interagir com o banco de dados SQLite.
* `InfoTranferencia.py`: Classe de dados para armazenar informações de um bem a ser transferido.
* `Transferencia.py`: Classe para gerenciar uma lista de bens para transferência.
* `Usuario.py`: Classe de dados para informações do usuário.
* `requirements.txt`: Lista de dependências Python do projeto. [cite: 1]
* `templates/`: Pasta contendo os templates HTML para as páginas web.
    * `login.html`: Página de login.
    * `cadastro.html`: Página para cadastro de bens.
    * `consulta.html`: Página para consulta de bens e logs.
    * `alterar_senha.html`: Página para alteração de senha.
    * `adicionar_usuario.html`: Página para adicionar novos usuários.
* `scripts/`: Pasta contendo scripts auxiliares.
    * `manipulaTabela.py`: (Conteúdo não fornecido) Provavelmente para ler e processar arquivos de lote.
    * `loginSda.py`: (Conteúdo não fornecido) Lógica para realizar login no sistema SDA.
    * `transferenciaBem.py`: (Conteúdo não fornecido) Lógica para realizar a transferência do bem no sistema SDA.
* `UPLOAD_FOLDER/`: Pasta criada dinamicamente para armazenar arquivos de lote enviados.

## Principais Tecnologias Utilizadas

* **Python:** Linguagem de programação principal.
* **Flask:** Microframework web para construir a aplicação.
* **Playwright:** Biblioteca para automação de navegador, usada para interagir com o sistema SDA.
* **SQLite:** Sistema de gerenciamento de banco de dados leve e baseado em arquivo.
* **Pandas:** (Inferido de `leTabela` e presente em `requirements.txt`) Para manipulação de dados, especialmente para o cadastro em lote. [cite: 1]
* **HTML/CSS/JavaScript:** (Implícito) Para a interface do usuário no navegador.
* **Werkzeug:** (Presente em `requirements.txt`) Utilitários WSGI, dependência do Flask. [cite: 1]

## Observações Importantes

* **Segurança de Credenciais:** A forma como os usuários são armazenados (`f'{usuario_rede}-{senha}'`) no banco não é segura. Considere usar hashing de senhas (ex: com Werkzeug security helpers ou passlib).
* **Criação Inicial de Usuário:** O primeiro usuário precisará ser adicionado manualmente ao banco de dados (tabela `usuarios`) ou através de um script separado, pois não há funcionalidade de "registrar-se" publicamente.
* **Configuração do SDA:** A URL do SDA e possivelmente seletores de elementos HTML para a automação com Playwright podem precisar de ajustes se o sistema SDA for atualizado.
* **Tratamento de Erros:** A robustez do tratamento de erros na interação com o SDA (Playwright) é crucial para a usabilidade.
