from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests import Session, ConnectionError, Timeout

rabbitmq_info = {
    'exchange_name': 'urls_exchange',
    'queue_name': 'urls_queue',
    'routing_key': 'urls',
    'rabbitmq_user': 'admin',
    'rabbitmq_pass': 'admin'
}

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
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