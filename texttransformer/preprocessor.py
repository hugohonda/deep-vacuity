# -*- coding: utf-8 -*-

import re
import nltk
import json
import pathlib
import unicodedata
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('portuguese'))

date_regex = r'\D((?:\d{1,2}\-\d{1,2}\-\d{2,4})|(?:\d{1,2}\/\d{1,2}\/\d{2,4}))\D'
hour_regex = r'[^\d\.](\d{1,2}(?:h|hs|\:)(?:\s*\d{2}(?:h|hs|m)?)?)'
phone_regex = r'\D(\(?(?:\d{2,3}|\d[\*x]{2}\d{2})\)?\s*9?\s?\d{4}[\-\s]?\d{4}(?:\s*\/\s*\d{4}[\-\s]?\d{4})*?(?:\/\d{4})?)\D'
phone_company_regex = r'\D(0800[\-\s]?\d{4,}?)\D'
email_regex = r'([\w\d_\-\.]+@(?:(?:[a-z_\-]+\.)+br|(?:[a-z_\-]+\.)+com|(?:[a-z_\-]+\.)+[a-z]{2,5}))\W'
website_regex = r'(?<![@\.\w@])((?:https?\:\/{2})?(?:(?:[a-z_\-\d]+\.)+br|(?:[a-z_\-\d]+\.)+com|(?:[a-z_\-\d]+\.){2,}[a-z]{2,5}))(?![@\w])'
cnpj_regex = r'\D(\d{2}\.?\d{3}\.?\d{3}[\/\-\.]?\d{4}[\/\-\.]?\d{2})\D'
cpf_regex = r'\D(\d{3}\.?\d{3}\.?\d{3}\-?\d{2})\D'
cep_regex = r'\D(\d{2}\.?\d{3}\-\d{3})\D'
monetary_regex = r'(?:(?:(?<!c)r\$\s*)(?:\d+)(?:[\. ]\d+)*(?:,\d+)?)(?:(?:\s+de)?\s+(?:rea(?:l|is)|centavos?))?|(?:(?:(?<!c)r\$\s*)?(?:\d+)(?:[\. ]\d+)*(?:,\d+)?)(?:(?:\s+de)?\s+(?:rea(?:l|is)|centavos?))'
contracted_regex = r'(?:[Cc]ontratad[ao](?:\([ao]\))?|CONTRATAD[AO|[Cc]oncedente|CONCEDENTE|[Oo]utorgante|OUTORGANTE]](?:\([AO]\))?)[sS]?\s*:?\s*([A-Z][\wÀ-ÿ]*(?:[\s\-&\']+[\wÀ-ÿ]+)*)\W'
contracting_regex = r'(?:[Cc]ontratante|CONTRATANTE|[Cc]onvenente|CONVENENTE|[Oo]utorgado|OUTORGADO)[sS]?\s*:?\s*([A-Z][\wÀ-ÿ]*(?:[\s\-&\']+[\wÀ-ÿ]+)*)\W'
object_regex = r'(?:[Oo]bjeto|OBJETO|[Ff]inalidade|FINALIDADE|[Oo]bjetivo|OBJETIVO|[Ee]sp.cie|ESP.CIE)[sS]?(?:\s+[Rr]esumid[ao])?\s*:?\s*"?([a-zA-Z][\wÀ-ÿ]*(?:[\s\-&]+[\(\)\wÀ-ÿ]+)*)"?\W'

def normalize (text):
    normalized = None
    try:
        text = unicodedata.normalize('NFKD', text)
        text = text.encode('ascii', 'ignore').decode('utf-8')
        text = re.sub('(\\d|\\W)+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        normalized = text
    except Exception as e:
        raise e
    return normalized

def tokenize (text):
    tokenized = None
    try:
        tokens = word_tokenize(text, language ='portuguese')
        tokenized = [w.lower() for w in tokens if w.lower() not in stop_words and len(w) > 2]
    except Exception as e:
        raise e
    return tokenized

def preprocess (text):
    try:
        normalized = normalize(text)
        tokenized = tokenize(normalized)
    except Exception as e:
        print('Error', str(e))
    return ' '.join(tokenized)

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
    
    parsed['date'] = match_unique(date_regex, text)
    parsed['hour'] = match_unique(hour_regex, text)
    parsed['phone'] = match_unique(phone_regex, text)
    parsed['phone'].extend(match_unique(phone_company_regex, text))
    parsed['email'] = match_unique(email_regex, text)
    parsed['website'] = match_unique(website_regex, text)
    parsed['cnpj'] = match_unique(cnpj_regex, text)
    parsed['cpf'] = match_unique(cpf_regex, text)
    parsed['cep'] = match_unique(cep_regex, text)
    parsed['monetary'] = match_unique(monetary_regex, text)
    parsed['contracted_party'] = match_unique(contracted_regex, text, flags=re.MULTILINE)
    parsed['contracting_party'] = match_unique(contracting_regex, text, flags=re.MULTILINE)
    parsed['object'] = match_unique(object_regex, text, flags=re.MULTILINE)
    
    if is_dict_empty(parsed):
        return None
    return parsed

def is_bidding(text):
    bidding_notice_regex = re.compile(r'(?!(?:extrato|aviso|processo)[\s\S]*?(?:dispen|inex)[\s\S]*?licita)^(?:extrato|aviso|processo)[\s\S]*?licita', re.IGNORECASE)
    if bidding_notice_regex.search(text):
        return True
    return False

def generate_preprocessed():
    '''
    Load documents.
    '''
    output_path = pathlib.Path('./data/preprocessed')
    output_path.mkdir(parents=True, exist_ok=True)
    input_path = pathlib.Path('./data/publications').glob('*.json')
    files = [x for x in input_path if x.is_file()]
    for filepath in files:
        file_data = None
        output_filename = filepath.name
        output_filepath = output_path / output_filename
        if output_filepath.exists():
            print(f'{str(output_filepath)} already exists')
        else:
            with filepath.open('r', encoding ='utf-8') as input_file:
                file_data = json.load(input_file)
            if file_data:
                print(filepath)
                preprocessed_data = []
                for publication in file_data:
                    preprocessed = {}
                    preprocessed['basics'] = extract_basics(publication['body'])
                    preprocessed['preprocessed'] = preprocess(publication['body'])
                    preprocessed_data.append(preprocessed)
                with output_filepath.open(mode='w', encoding='utf-8') as output_file:
                    json.dump(preprocessed_data, output_file)
