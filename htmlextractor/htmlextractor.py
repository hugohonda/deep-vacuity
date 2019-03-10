# -*- coding: utf-8 -*-

import re
import csv
import pathlib
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from datetime import date, timedelta
from helpers.helpers import get_response
import json

output_path = pathlib.Path('./data/html_publications')
output_path.mkdir(parents=True, exist_ok=True)
base_url =' http://www.imprensanacional.gov.br/'

def extract_html_publications(date, base_section=3):
    url = f'{base_url}leiturajornal?data={date}&secao=dou{str(base_section)}'
    print(url)
    content = get_response(url, stream=True).content
    soup =  BeautifulSoup(content, 'html.parser', from_encoding='utf8')
    id_portlet_instance = re.search(r'(?<=idPortletInstance":")\w+?(?=",)', soup.text)
    id_portlet_instance = id_portlet_instance.group(0)
    entry_ids = re.findall(r'(?<=entryId":)\d+?(?=})', soup.text)
    publications = []
    for entry in entry_ids:
        url = f'http://www.in.gov.br/materia/-/asset_publisher/{id_portlet_instance}/content/id/{entry}'
        try:
            publication = get_publication(url)
            publications.append(publication)
        except Exception as e:
            print('Could not get publication from: ', url, 'with error')
            print(str(e))
    return publications

def get_publication(url):
    obj = {}
    try:
        content = get_response(url).content
        soup =  BeautifulSoup(content, 'html.parser', from_encoding='utf8')
        title = soup.find('h3', attrs={'class': 'titulo-dou'})
        if title:
            body = soup.find('span', attrs={'class': 'texto-dou'})
        else:
            title = soup.find('p', attrs={'class': 'identifica'})
            body = soup.find('p', attrs={'class': 'dou-paragraph'})
        agency = soup.find('span', attrs={'class': re.compile(r'orgao-dou-data')})
        signatories = soup.findAll('p', attrs={'class': re.compile(r'assina(-dou)?' )})
        functions = soup.findAll('p', attrs={'class': re.compile(r'cargo(-dou)?')})
        obj = {
            'url': url,
            'title': '',
            'body': '',
            'agency': ''
        }
        signatories_set = set()
        functions_set = set()
        if title:
            obj['title'] = title.text.strip()
        if body:
            obj['body'] = body.text.strip()
        if agency:
            obj['agency'] = agency.text.strip()
        if signatories:
            for sign in signatories:
                signatories_set.add(sign.text)
        if functions:
            for func in functions:
                functions_set.add(func.text)
        obj['signatories'] = list(signatories_set)
        obj['functions'] = list(functions_set)
    except Exception as e:
        raise e
    return obj

def generate_html_publications(date):
    output_filename = ''.join(date.split('-')[::-1]) + '.json'
    output_filepath = output_path / output_filename
    if output_filepath.exists():
        print(f'{str(output_filepath)} already exists')
    else:
        publications = extract_html_publications(date)
        print('extracted: ', date)
        with output_filepath.open(mode='w', encoding='utf-8') as output_file:
            json.dump(publications, output_file)
