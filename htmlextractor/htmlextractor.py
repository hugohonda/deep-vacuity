# -*- coding: utf-8 -*-

import re
import csv
import pathlib
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from datetime import date, timedelta
import json

from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests import Session, ConnectionError, Timeout

base_path = pathlib.Path('./data')
base_url =' http://www.imprensanacional.gov.br/'
base_section = '3'
base_year = '2018'
(base_path / base_year).mkdir(parents=True, exist_ok=True)

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Debian; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'accept-Language': 'pt-BR,pt;q=0.5',
    'accept-Encoding': 'gzip, deflate',
    'connection': 'keep-alive',
    'upgrade-insecure-requests': '1',
    'referrer': 'https://google.com.br',
}

def requests_retry_session(retries=10, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    session = session or Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def get_response (url, stream=False):
    try:
        response = requests_retry_session().get(url, headers=headers, stream=stream)
    except ConnectionError as e:
        print(f'Connection Error. Technical details:\n{str(e)}')
    except Timeout as e:
        print(f'Timeout Error:\n{str(e)}')
    except Exception as e:
        print(f'General Error :\n{e.__class__.__name__}')
    finally:
        return response
def extract_html_publications(date):
    url = f'{base_url}leiturajornal?data={date}&secao=dou{base_section}'
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
    output_path = pathlib.Path('./data/html_publications')
    output_path.mkdir(parents=True, exist_ok=True)
    output_filename = ''.join(date.split('-')[::-1]) + '.json'
    output_filepath = output_path / output_filename
    if output_filepath.exists():
        print(f'{str(output_filepath)} already exists')
    else:
        publications = extract_html_publications(date)
        print('extracted: ', date)
        with output_filepath.open(mode='w', encoding='utf-8') as output_file:
            json.dump(publications, output_file)
