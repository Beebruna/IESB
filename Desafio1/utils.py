import re
import hashlib


meses = {
    'jan': '01',
    'fev': '02',
    'mar': '03',
    'abr': '04',
    'mai': '05',
    'jun': '06',
    'jul': '07',
    'ago': '08',
    'set': '09',
    'out': '10',
    'nov': '11',
    'dez': '12'
}

data_dictionary = {
    '01': 'Ações de promoção e prevenção em saúde',
    '02': 'Procedimentos com finalidade diagnóstica',
    '03': 'Procedimentos clínicos',
    '04': 'Procedimentos cirúrgicos',
    '05': 'Transplantes de orgãos, tecidos e células',
    '06': 'Medicamentos',
    '07': 'Órteses, próteses e materiais especiais',
    '08': 'Ações complementares da atenção à saúde',
    '0101': 'Ações coletivas/individuais em saúde',
    '0201': 'Coleta de material',
    '0202': 'Diagnóstico em laboratório clínico',
    '0203': 'Diagnóstico por anatomia patológica e citopatologia',
    '0204': 'Diagnóstico por radiologia',
    '0205': 'Diagnóstico por ultrasonografia',
    '0206': 'Diagnóstico por tomografia',
    '0207': 'Diagnóstico por ressonância magnética',
    '0208': 'Diagnóstico por medicina nuclear in vivo',
    '0209': 'Diagnóstico por endoscopia',
    '0210': 'Diagnóstico por radiologia intervencionista',
    '0211': 'Métodos diagnósticos em especialidades',
    '0212': 'Diagnóstico e procedimentos especiais em hemoterapia',
    '0214': 'Diagnóstico por teste rápido',
    '0301': 'Consultas / Atendimentos / Acompanhamentos',
    '0302': 'Fisioterapia',
    '0303': 'Tratamentos clínicos (outras especialidades)',
    '0304': 'Tratamento em oncologia',
    '0305': 'Tratamento em nefrologia',
    '0306': 'Hemoterapia',
    '0307': 'Tratamentos odontológicos',
    '0308': 'Tratamento de lesões, envenenamentos e outros, decorrentes de causas externas',
    '0309': 'Terapias especializadas',
    '0310': 'Parto e nascimento',
    '0401': 'Pequenas cirurgias e cirurgias de pele, tecido subcutâneo e mucosa',
    '0402': 'Cirurgia de glândulas endócrinas',
    '0403': 'Cirurgia do sistema nervoso central e periférico',
    '0404': 'Cirurgia das vias aéreas superiores, da face, da cabeça e do pescoço',
    '0405': 'Cirurgia do aparelho da visão',
    '0406': 'Cirurgia do aparelho circulatório',
    '0407': 'Cirurgia do aparelho digestivo, orgãos anexos e parede abdominal',
    '0408': 'Cirurgia do sistema osteomuscular',
    '0409': 'Cirurgia do aparelho geniturinário',
    '0410': 'Cirurgia de mama',
    '0411': 'Cirurgia obstétrica',
    '0412': 'Cirurgia torácica',
    '0413': 'Cirurgia reparadora',
    '0414': 'Bucomaxilofacial',
    '0415': 'Outras cirurgias',
    '0416': 'Cirurgia em oncologia',
    '0417': 'Anestesiologia',
    '0418': 'Cirurgia em nefrologia',
    '0501': 'Coleta e exames para fins de doação de orgãos, tecidos e células e de transplante',
    '0502': 'Avaliação de morte encefálica',
    '0503': 'Ações relacionadas à doação de orgãos e tecidos para transplante',
    '0504': 'Processamento de tecidos para transplante',
    '0505': 'Transplante de orgãos, tecidos e células',
    '0506': 'Acompanhamento e intercorrências no pré e pós-transplante',
    '0603': 'Medicamentos de âmbito hospitalar e urgência',
    '0702': 'Órteses, próteses e materiais especiais relacionados ao ato cirúrgico',
    '0801': 'Ações relacionadas ao estabelecimento',
    '0802': 'Ações relacionadas ao atendimento'
}


# Obtém apenas os caracteres numéricos de uma string/texto
def get_character_numeric(string: str) -> str:

    numero = re.findall(r'\d+', string)

    if numero:
        return numero[0]
    else:
        return string


# Extrai o ano e mês de uma data do tipo Jan/2023
def extract_date(data: str) -> tuple:
    
    ano = data.split('/')[1]
    mes = meses[data.split('/')[0].lower()]
    return (ano, mes)


# Obtém o hash dos valores a serem inseridos no banco de dados
def get_hash(valores: list) -> str:
    
    valores_concat = ''.join(str(valor) for valor in valores)
    hash = hashlib.sha256(valores_concat.encode('utf-8')).hexdigest()
    return hash


# Formata o nome das variáveis para se adaptar ao banco
def format_column_name(nome: str, columns: list) -> list:
    
    if 'quantidade' in nome:
        prefixo = 'qtd_'
    else:
        prefixo = 'val_'

    columns[5:-1] = [prefixo + coluna for coluna in columns[5:-1]]

    return columns