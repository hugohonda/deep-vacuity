# -*- coding: utf-8 -*-

import re
import json
import time
import pathlib
import subprocess
import requests
import tempfile
from datetime import datetime
from helpers.helpers import headers, get_response
# import pika

exchange_name = 'urls_exchange'
queue_name = 'urls_queue'
routing_key   = 'urls'
rabbitmq_user = 'admin'
rabbitmq_pass = 'admin'

def parse_doc_url (url):
    '''
    Parse document URL into object containing journal, date, first_page, last_page, filename.
    Args:
        param1 (str): The complete url.
    Returns:
        dict: returns object containing parsed details from URL.
    '''
    matched = re.search(r'jornal=(\d+?)&pagina=(\d+?)&data=([\d\/]{10})&totalArquivos=(\d+)', url)
    date = datetime.strptime(matched[3], '%d/%m/%Y')
    return {
        'journal': int(matched[1]),
        'date': str(date),
        'first_page': int(matched[2]),
        'last_page': int(matched[4]) + 1,
        'filename': date.strftime('%Y%m%d')
    }

def get_pdf_online_content (url):
    '''
    Convert online pdf to text using a complete URL, pdftotext module and tempfile.
    Args:
        param1 (str): The complete url.
    Returns:
        str: returns text converted from the pdf in the URL.
    '''
    try:
        result = get_response(url)
        temp_file = tempfile.TemporaryFile()
        temp_file.write(result.content)
        temp_file.seek(0)
        output, error  = subprocess.Popen(['pdftotext', '-raw', '-enc', 'UTF-8', '-', '-'], stdin=temp_file, stdout=subprocess.PIPE).communicate()
        pdf_text = str(output, 'utf-8')
        temp_file.close()
        if error:
            raise subprocess.CalledProcessError
    except subprocess.CalledProcessError as e:
        print('[Called Process Error] Could not convert using pdftotext. Technical Details given below.')
        print(str(e))
    return pdf_text

def get_pages_content (url):
    '''
    Get data from pages content from a document.
    Args:
        param1 (dict): The document dict.
    Returns:
        list: returns a list from pages content from the reference document.
    '''
    data = []
    parsed = parse_doc_url(url)
    for page_number in range(parsed['first_page'], parsed['last_page']):
        body = ''
        try:
            page_url = re.sub('&pagina=(\d+?)&', f'&pagina={str(page_number)}&', url)
            body = get_pdf_online_content(page_url)
            page = {
                'journal': parsed['journal'],
                'date': parsed['date'],
                'pageNumber': page_number,
                'body': body,
                'url': page_url,
                'status': True
            }
            data.append(page)
        except Exception as error:
            raise error
    return data

def generate_json_file (urls):
    '''
    Generates JSON file from extracted URLs.
    '''
    dirpath = pathlib.Path('./data/documents/')
    dirpath.mkdir(parents=True, exist_ok=True)
    data = []
    for url in urls:
        parsed = parse_doc_url(url)
        filename = f"{parsed['filename']}.json"
        filepath = dirpath / filename
        if not filepath.exists():
            print(url)
            content = get_pages_content(url)
            data.extend(content)
            with filepath.open(mode='w', encoding='utf-8') as outfile:
                json.dump(data, outfile)
        else:
            print(f'{str(filepath)} already exists')

def load_urls():
    '''
    Load URLs from JSON file array.
    '''
    dirpath = pathlib.Path('./data/')
    dirpath.mkdir(parents=True, exist_ok=True)
    filename = 'urls.json'
    filepath = dirpath / filename
    with filepath.open('r', encoding ='utf-8') as outfile:
        return json.load(outfile)

# def receive_urls():
#     credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
#     connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', '5672', '/', credentials))
#     channel = connection.channel()

#     channel.exchange_declare(exchange=exchange_name,
#                             exchange_type='fanout')

#     result = channel.queue_declare(exclusive=True)
#     queue_name = result.method.queue

#     channel.queue_bind(exchange=exchange_name,
#                         queue=queue_name)

#     def callback(ch, method, properties, body):
#         urls = json.loads(body)
#         generate_json_file(urls)

#     channel.basic_consume(callback,
#                             queue=queue_name,
#                             no_ack=True)

#     channel.start_consuming()
