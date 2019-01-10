from urlscraper import get_document_urls, emit_urls
import time

def main():
    urls = get_document_urls(begin_month=12, year=2014)
    emit_urls(urls)

if __name__ == '__main__':
    main()
    try:
        while True:
            time.sleep(1)
    except Exception as e:
        print('Error:', str(e))