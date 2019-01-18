from pdfextractor import load_urls, generate_json_file

def main():
    urls = load_urls()
    generate_json_file(urls)

if __name__ == '__main__':
    main()