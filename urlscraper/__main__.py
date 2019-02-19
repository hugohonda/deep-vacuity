from urlscraper import get_document_urls, dump_urls
import time

def main():
    urls = get_document_urls(begin_month=12, year=2014)
    dump_urls(urls)

if __name__ == '__main__':
    main()