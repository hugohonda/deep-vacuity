# -*- coding: utf-8 -*-

from entityextractor import extract_basics, is_bidding
from preprocessor import preprocess
from pprint import pprint

def main():
    text = 'PREGÃO SISPP Nº 2/2017. Contratante: INSTITUTO FEDERAL DE EDUCACAO, -CIENCIA E TECNOLOGIA DE. CNPJ Contratado: 00604122000197. Contratado : TRIVALE ADMINISTRACAO LTDA -.Objeto: Prorrogação do contrato nº 23/2017. Fundamento Legal: Lei 8666/93 . Vigência: 05/06/2018 a 04/06/2019. Valor Total: R$25.316,00. Fonte: 8100000000 - 2018NE800025. Data de Assinatura: 19/04/2018.'
    text = 'Processo: 21223.000098/2018-98. Contratante: Companhia Nacional de Abastecimento - CONAB. CNPJ: 26.461.699/0451-09. Contratado: Sul.Com Atacado e Varejo. CNPJ: 26.469.541/0001-57. Objeto: Aquisição de 3000 máscaras descartáveis PFF2, antipoeira/névoa, com válvula, com validade mínima de 01 (um) ano. Valor: R$ 3.000,00 (três mil reais). Empenho: 2018NE000025 - UG 135557. Fundamento Legal: Art. 29, Inciso II da Lei nº 13.303/2016. Declaração de Dispensa de Licitação em: 09/05/2018, autorizada por Leandro de Morais Maia - GEFAD e Autoridade Ratificadora: Maria Darcy de Almeida Xavier - Superintendente Regional.'
    text = 'Contrato: Ordem de Serviço PR/033/2018. Contratante: Centrais Elétricas de Rondônia S.A - CERON. Contratada: Expresso Maia Ltda. Proveniente da Dispensa de Licitação 006/2018. Objeto: Locação de um ônibus para atender ao Conselho de Consumidores durante o evento XX Encontro de Conselhos de Consumidores da Região Norte. Vigência: 30 (trinta) dias. Valor Total: R$5.500,00 (cinco mil e quinhentos reais). Assinaturas: 18/04/2018. Jonecildo Conceição Campos - Técnico de Nível Superior e Moisés Nonato de Souza - Assistente do Diretor, pela Contratante, Elivã de Jesus - Gerente de Vendas, pela Contratada.'
    text = 'RDC ELETRÔNICO Nº 3/2017. Contratante: UNIVERSIDADE FEDERAL DE ITAJUBA -.CNPJ Contratado: 14294202000106. Contratado : LBRAGA CONSTRUTORA E INCORPORADORAEIRELI - EPP. Objeto: Substituição de preposto. Passa a atuar como preposto da Contratada, o Sr. Arnaldo Laurito, CPF nº 286.870.196-53, em substituição ao Sr. Adriano da Silva, CPF nº 962.392.126-87. Fundamento Legal: Lei nº 8.666/93 e suas posteriores alterações. Data de Assinatura: 02/02/2018.'
    text = 'PREGÃO SRP Nº 344/2017. Contratante: UNIVERSIDADE FEDERAL DE SANTA -CATARINA. CNPJ Contratado: 02745352000100. Contratado : MARZO VITORINO - INDUSTRIA E -COMERCIO DE MOVEIS LTDA. Objeto: Aquisição de mobiliário corporativo para atender a todas as unidades da UFSC. Fundamento Legal: Lei 8666/93 . Vigência: 17/04/2018 a 17/04/2019. Valor Total: R$2.724,00. Fonte: 8250262460 - 2018NE800764. Data de Assinatura: 17/04/2018.'
    print('-'*50)
    print('original text:\n')
    print(text)
    print('-'*50)
    print('preprocessed text:\n')
    print(preprocess(text))
    print('-'*50)
    print('extracted entities:\n')
    basics = extract_basics(text)
    pprint(basics)
    print('-'*50)
    print(f'bidding: {is_bidding(text)}')

if __name__ == '__main__':
    main()
