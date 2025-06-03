import pandas as pd

def leTabela(arquivo):
    extensao = arquivo.lower().split('.')[-1]
    df = ''
    if extensao in ['xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt']:
        df = pd.read_excel(f'UPLOAD_FOLDER/{arquivo}')
    elif extensao == 'csv':
        df = pd.read_csv(f'UPLOAD_FOLDER/{arquivo}')
    return df