import utils
import requests
import pandas as pd
import urllib.parse as prs
from bs4 import BeautifulSoup


def request(tipo, url, linha=None, coluna=None, conteudo=None, periodo=None):
    
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded'
            }

    match tipo:
        case 'post':
            data = {
                    'Linha': f'{linha}'.replace(' ', '_'),
                    'Coluna': f'{coluna}'.replace(' ', '_'),
                    'Incremento': f'{conteudo}'.replace(' ', '_'),
                    'Arquivos': f'spabr{periodo[0][2:]}{periodo[1]}.dbf',
                    'zeradas': 'exibirlz',
                    'formato': 'table',
                    'mostre': 'Mostra'
                }
            response_content = requests.post(url, headers=headers, data=prs.urlencode(data, encoding='ISO-8859-1')).content
            return response_content
        case 'get':
            response_content = requests.get(url, headers=headers).content
            return response_content

    
def soup_object(response_content):
    return BeautifulSoup(response_content, 'html.parser')


def parser(url):

    soup = soup_object(request('get', url))

    linha = soup.find('div', class_='borda').find('div', 'linha').find_all('option')[0].get_text().split('\r\n    ')[:-1]
    
    coluna = soup.find('div', class_='borda').find('div', 'coluna').find_all('option')[0].get_text().split('\r\n    ')[:-1]
    
    conteudo = soup.find('div', class_='borda').find('div', 'conteudo').find_all('option')[0].get_text().split('\r\n    ')[:-1]
    
    periodo = soup.find('div', class_='periodo').find_all('option')[0].get_text().strip().split('\r\n    ')

    periodo = [utils.extract_date(data) for data in periodo]

    return linha, coluna, conteudo, periodo


def get_table(url: str, linha: str, coluna: str, conteudo: str, periodo: tuple) -> pd.DataFrame:
    response_content = request('post', url, linha, coluna, conteudo, periodo)
    df = pd.read_html(response_content)[0]
    
    # Remove um nível do título
    df = df.droplevel(0, axis=1)
    
    # Remove colunas de Unnamed e Total
    columns_to_drop = [col for col in df.columns if col.lower().startswith('unnamed') or col.lower().startswith('total')]
    df.drop(columns=columns_to_drop, inplace=True)

    # Remove a primeira linha
    df = df.drop(df.index[0])

    # Remove a última linha
    df = df.drop(df.index[-1])

    # Elimina os registros no qual a coluna municípios possui valores com substring iguais a ignorado
    mask = df['Município'].str.contains('ignorado', case=False)
    df.drop(df[mask].index, inplace=True)

    # Reinicia os indíces das linhas
    df.reset_index(drop=True, inplace=True)

    # Substitui qualquer ocorrência de '-' por None
    df.replace(to_replace=r'^-+$', value=None, regex=True, inplace=True)

    # Separa o código do IBGE do município da coluna Município
    df[['codigo_ibge', 'Município']] = df['Município'].str.split(' ', n=1, expand=True)

    # Elimina possíveis espaços extras iniciais e finais
    df['Município'] = df['Município'].str.strip()
    df['codigo_ibge'] = df['codigo_ibge'].str.strip()

    # Renomeia as colunas
    df.columns = [utils.get_character_numeric(column) for column in df.columns]
    df.rename(columns={'Município': 'municipio'}, inplace=True)

    # Coloca a coluna Codigo_IBGE na primeira posição
    ultima_coluna = df.pop(df.columns[-1]) # Extrai a última coluna
    df.insert(0, ultima_coluna.name, ultima_coluna) # Insere a última coluna na primeira posição

    # Cria as colunas Hash, Ano, Mes e current_datetime
    df.insert(0, 'hash', value=None)
    df.insert(2, 'ano', value=periodo[0])
    df.insert(3, 'mes', value=periodo[1])
    df['current_datetime'] = pd.Timestamp.now()

    # Formata os valores para onde o . separa os decimais
    for coluna in df.columns[5:-1]:
        df[coluna] = df[coluna].str.replace('.', '').str.replace(',', '.')

    return df