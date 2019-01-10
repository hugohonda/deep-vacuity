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
    
    monetary_regex = r'(?:(?:(?<!c)r\$\s*)(?:\d+)(?:[\. ]\d+)*(?:,\d+)?)(?:(?:\s+de)?\s+(?:rea(?:l|is)|centavos?))?|(?:(?:(?<!c)r\$\s*)?(?:\d+)(?:[\. ]\d+)*(?:,\d+)?)(?:(?:\s+de)?\s+(?:rea(?:l|is)|centavos?))'
    parsed['monetary'] = match_unique(monetary_regex, text)
    
    contracted_regex = r'(?:[Cc]ontratad[ao](?:\([ao]\))?|CONTRATAD[AO](?:\([AO]\))?)[sS]?\s*:?\s*([A-Z][\wÀ-ÿ]*(?:[\s\-&\']+[\wÀ-ÿ]+)*)\W'
    parsed['contracted_party'] = match_unique(contracted_regex, text, flags=re.MULTILINE)
    
    contracting_regex = r'(?:[Cc]ontratante|CONTRATANTE)[sS]?\s*:?\s*([A-Z][\wÀ-ÿ]*(?:[\s\-&\']+[\wÀ-ÿ]+)*)\W'
    parsed['contracting_party'] = match_unique(contracting_regex, text, flags=re.MULTILINE)
    
    object_regex = r'(?:[Oo]bjeto|OBJETO|[Ff]inalidade|FINALIDADE|[Oo]bjetivo|OBJETIVO|[Ee]sp.cie|ESP.CIE)[sS]?(?:\s+[Rr]esumid[ao])?\s*:?\s*"?([a-zA-Z][\wÀ-ÿ]*(?:[\s\-&]+[\wÀ-ÿ]+)*)"?\W'
    parsed['object'] = match_unique(object_regex, text, flags=re.MULTILINE)
    
    if is_dict_empty(parsed):
        return None
    return parsed

def is_bidding(text):
    bidding_notice_regex = re.compile(r'(?!(?:extrato|aviso|processo)[\s\S]*?(?:dispen|inex)[\s\S]*?licita)^(?:extrato|aviso|processo)[\s\S]*?licita', re.IGNORECASE)
    if bidding_notice_regex.search(text):
        return True
    return False
