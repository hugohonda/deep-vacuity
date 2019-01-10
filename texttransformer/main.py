from entityextractor import extract_basics
from preprocessor import preprocess
from pprint import pprint

def main():
    text = 'Processo Licitatório/FMS n° 010/2018 OBJETO: Aquisição de 03 (três) veículos zero km, 01 (um) veículo PICK-UP CABINE DUPLA 4X4 A DIESEL, 01 (uma) AMBULÂNCIA TIPO A - SIMPLES REMOÇÃO TIPO FURGÃO A DIESEL e 01 (uma) AMBULÂNCIA SIMPLES REMOÇÃO TIPO ADAPTADA A GASOLINA E/OU ÁLCOOL; VALOR MÁXIMO ESTIMADO: R$ 382.993,33; TIPO DE JULGAMENTO: Menor preço unitário; ABERTURA: 04/06/2018 às 09h00min. O edital encontra-se disponível na sala de licitação, situada na Avenida José Veríssimo dos Santos, nº 365, Bairro Centro, Cidade de Triunfo, Estado de Pernambuco, CEP: 56.870-000, Fone: 87 3846 1365, E-mail: triunfocpl@outlook.com, no horário de 07h30min às 13h30min.'
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
    

if __name__ == '__main__':
    main()