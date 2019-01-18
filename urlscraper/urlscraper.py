# -*- coding: utf-8 -*-

import re
import os
import pika
import json
import pathlib
from datetime import datetime
from bs4 import BeautifulSoup
from helpers.helpers import rabbitmq_info, headers, get_response

def parse_url(url):
    """Parse a DOU URL extracted via scraper into a document dict.
    Args:
        param1 (str): The url to be parsed in format `jornal=(\d+?)&pagina=(\d+?)&data=([\d\/]{10})&totalArquivos=(\d+)`.
    Returns:
        dict: returns the parsed data from url in dict format.
    """
    matched = re.match(r'jornal=(\d+?)&pagina=(\d+?)&data=([\d\/]{10})&totalArquivos=(\d+)', url)
    return 'http://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer?' + \
            f'jornal={matched[1]}&' + \
            f'pagina={matched[2]}&' + \
            f'data={matched[3]}&' + \
            f'totalArquivos={int(matched[4])}&' + 'captchafield=firstAccess'


def get_document_urls(year=datetime.now().year-1, begin_day=1, begin_month=1, end_day=31, end_month=12, document_type=r'Di..?rio Oficial da Uni..?o'):
    """Get a bulk of document urls from certain time interval.
    Args:
        param1 (int): Scraping year.
        param2 (int): Scraping begin day.
        param3 (int): Scraping begin month.
        param4 (int): Scraping end day.
        param5 (int): Scraping end month.
        param6 (str): Document description.
    Returns:
        list: returns a list of scraped documents.
    """
    urls = []
    base_url = 'http://pesquisa.in.gov.br/imprensa/core/jornalList.action?' +\
                f'edicao.dtInicio={str(begin_day).zfill(2)}' +\
                f'%2F{str(begin_month).zfill(2)}' +\
                f'&edicao.jornal=3%2C3000%2C3020%2C1040%2C526%2C530%2C608%2C609%2C610%2C611' +\
                f'&edicao.dtFim={str(end_day).zfill(2)}' +\
                f'%2F{str(end_month).zfill(2)}' +\
                f'&edicao.ano={str(year)}' +\
                f'&edicao.jornal_hidden='
    response = get_response(base_url, stream=True)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf8')
    max_pages = 1
    if begin_day != end_day:
        last_page = soup.find('a', text=re.compile('.ltimo'))['href']
        max_pages = int(re.search(r'-p=(\d+)&', last_page)[1])
    for page in range(1, max_pages+1):
        page_url = f'{base_url}&d-7825134-p={page}'
        response = get_response(page_url, stream=True)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser', from_encoding='utf8')
        table = soup.find('table', {'id': 'ResultadoConsulta'})
        for tr in table.findAll('tr'):
            a = tr.find('a', href=True)
            if a and re.search(document_type, a.text):
                parcial_url = re.search(r"redirecionaSelect\('\.\.\/jsp\/visualiza\/index\.jsp\?(.*)'\);", a['onclick'])[1]
                parsed = parse_url(parcial_url)
                urls.append(parsed)
    urls.sort(key=lambda x: datetime.strptime(re.search(r'(?<=data=)\d{2}\/\d{2}\/\d{4}', x).group(0), '%d/%m/%Y'))
    return urls

def dump_urls(urls):
    dirpath = pathlib.Path('./data/')
    dirpath.mkdir(parents=True, exist_ok=True)
    filename = 'urls.json'
    filepath = dirpath / filename
    with filepath.open('w', encoding ='utf-8') as outfile:
        json.dump(urls, outfile)

def emit_urls(urls):
    credentials = pika.PlainCredentials(rabbitmq_info['rabbitmq_user'], rabbitmq_info['rabbitmq_pass'])
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', '5672', '/', credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange=rabbitmq_info['exchange_name'],
                         exchange_type='fanout')

    channel.basic_publish(exchange=rabbitmq_info['exchange_name'],
                        routing_key='',
                        body=json.dumps(urls))

    print(f' [x] Emitted {len(urls)} urls to queue')
    connection.close()
