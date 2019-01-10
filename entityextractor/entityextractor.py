# -*- coding: utf-8 -*-

import re

def match_unique(regex, input_text, flags=re.MULTILINE+re.IGNORECASE):
    match_pattern = re.compile(regex, flags=flags)
    matched = match_pattern.findall(input_text)
    match_set = set()
    if matched:
        for match in matched:
            match_set.add(match)
    return list(match_set)


def is_dict_empty(dictionary):
    return all(value == [] for value in dictionary.values())


def extract_basics(text):
    parsed = {}
    
    date_regex = r'\D((?:\d{1,2}\-\d{1,2}\-\d{2,4})|(?:\d{1,2}\/\d{1,2}\/\d{2,4}))\D'
    parsed['date'] = match_unique(date_regex, text)
    
    hour_regex = r'[^\d\.](\d{1,2}(?:h|hs|\:)(?:\s*\d{2}(?:h|hs|m)?)?)'
    parsed['hour'] = match_unique(hour_regex, text)

    phone_regex = r'\D(\(?(?:\d{2,3}|\d[\*x]{2}\d{2})\)?\s*9?\s?\d{4}[\-\s]?\d{4}(?:\s*\/\s*\d{4}[\-\s]?\d{4})*?(?:\/\d{4})?)\D'
    parsed['phone'] = match_unique(phone_regex, text)
    
    phone_company_regex = r'\D(0800[\-\s]?\d{4,}?)\D'
    parsed['phone'].extend(match_unique(phone_company_regex, text))

    email_regex = r'([\w\d_\-\.]+@[\w\d_\-\.]+\.\w{2,5})\W'
    parsed['email'] = match_unique(email_regex, text)

    website_regex = r'(?<![@\.\w\d])((?:http\:\/\/|https\:\/\/)?(?:[a-z][\w\d\-]{2,}\.)+[a-z][\w\d\-\/]*)(?![@\w])'
    parsed['website'] = match_unique(website_regex, text)

    cnpj_regex = r'\D(\d{2}\.?\d{3}\.?\d{3}[\/\-\.]?\d{4}[\/\-\.]?\d{2})\D'
    parsed['cnpj'] = match_unique(cnpj_regex, text)

    cpf_regex = r'\D(\d{3}\.?\d{3}\.?\d{3}\-?\d{2})\D'
    parsed['cpf'] = match_unique(cpf_regex, text)

    cep_regex = r'\D(\d{2}\.?\d{3}\-\d{3})\D'
    parsed['cep'] = match_unique(cep_regex, text)
    
    if is_dict_empty(parsed):
        return None
    return parsed

def main():
    text = 'Processo Licitatório/FMS n° 010/2018 OBJETO: Aquisição de 03 (três) veículos zero km, 01 (um) veículo PICK-UP CABINE DUPLA 4X4 A DIESEL, 01 (uma) AMBULÂNCIA TIPO A - SIMPLES REMOÇÃO TIPO FURGÃO A DIESEL e 01 (uma) AMBULÂNCIA SIMPLES REMOÇÃO TIPO ADAPTADA A GASOLINA E/OU ÁLCOOL; VALOR MÁXIMO ESTIMADO: R$ 382.993,33; TIPO DE JULGAMENTO: Menor preço unitário; ABERTURA: 04/06/2018 às 09h00min. O edital encontra-se disponível na sala de licitação, situada na Avenida José Veríssimo dos Santos, nº 365, Bairro Centro, Cidade de Triunfo, Estado de Pernambuco, CEP: 56.870-000, Fone: 87 3846 1365, E-mail: triunfocpl@outlook.com, no horário de 07h30min às 13h30min.'
    basics = extract_basics(text)
    print(basics)

if __name__ == '__main__':
    main()
