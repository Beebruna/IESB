import utils
import parser_def
from tqdm import tqdm
from banco.config import banco_padrao
from psycopg2.errors import UniqueViolation


def scraper(nome: str, table):

    banco = banco_padrao()

    colunas = tuple(utils.format_column_name(nome, list(table.columns)))
    print(colunas)

    for _, row in tqdm(table.iterrows()):
        registro = row.to_dict()
        valores = list(registro.values())

        hash = utils.get_hash(valores[:-1])
        valores[0] = hash
        print(valores)
        
        try:
            banco.insert(nome, colunas, tuple(valores))
        except UniqueViolation:
            print('\033[1;31mEsse dado já existe!\033[0m')
            continue


if __name__ == "__main__":

    url = 'http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sih/cnv/spabr.def'

    linha, coluna, conteudo, periodo = parser_def.parser(url)

    LINHA = ['Município']
    COLUNA = ['Grupo procedimento', 'Subgrupo proced.']
    CONTEUDO = ['Quantidade aprovada', 'Valor aprovado']
    PERIODO = [data for data in periodo if (data[0] not in ('2008'))]

    for row in LINHA:
        for column in COLUNA:
            for content in CONTEUDO:
                nome = column.replace(' ', '_').lower().replace('.', '') + '_' + content.replace(' ', '_').lower()
                print('\033[1;36m', nome.upper(), '\033[0m')
                for period in PERIODO:
                    table = parser_def.get_table(url, row, column, content, period)
                    scraper(nome, table)