import itertools as it
import pathlib
import json
import re

def clean_page(text):
    text = re.sub(r'[^\S\n]', ' ', text)
    text = re.sub(r'(?<=[A-Z]\-)\n(?=[A-Z])', '', text)
    text = re.sub(r'^N[\s\S]+?ICP-Brasil.\s\d\n?', '', text)
    return text

def extract_publications(text):
    '''
    Extract publications from page raw text.
    Args:
        param1 (str): Page's raw text.
    Returns:
        list: returns extracted publications formatted as a list of dicts containing publication's title and body.
    '''
    text = clean_page(text)
    sentences = re.finditer(r'(?:\n)([A-Z]{2,}[A-ZÃÂÁÀẼÊÉÈÍÌÕÔÓÒÚÙÇ\s\d\.,oºª\-\/]{3,})(?:\n)(?![a-z])', text)
    sentences, sentences_next = it.tee(sentences)
    publications = []
    try:
        next(sentences_next)
        for sentence, sentence_next in zip(sentences, sentences_next):
            title = re.sub(r'^\n+|\n+$', '', sentence.group())
            body = re.sub(r'^\n+|\n+$', '', text[sentence.end():sentence_next.start()])
            body = re.sub(r'(?:(?<=E|\-|\,|\:)|(?<=D(?:E|A|O)|N(?:A|O))|(?<=D(?:E|A|O)S|N(?:A|O)S))\n', ' ', body)
            body = re.sub(r'\n(?=(?:E|D(?:E|A|O)S?|N(?:A|O)S?|\-)\s+)', ' ', body)
            body = re.sub(r'[a-z]\-\s|[A-Z]\-[A-Z]', '', body)
            publication = {
                'title': title,
                'body': body
            }
            publications.append(publication)
    except Exception as e:
        print(f'Error: {str(e)}')
        pass
    return publications

def generate_publications():
    '''
    Load documents.
    '''
    output_path = pathlib.Path('./data/publications')
    output_path.mkdir(parents=True, exist_ok=True)
    input_path = pathlib.Path('./data/documents').glob('*.json')
    files = [x for x in input_path if x.is_file()]
    for file in files:
        file_data = None
        output_filename = file.name
        print(output_filename)
        output_filepath = output_path / output_filename
        if output_filepath.exists():
            print(f'{str(output_filepath)} already exists')
        else:
            with file.open('r', encoding ='utf-8') as input_file:
                file_data = json.load(input_file)
            if file_data:
                full_text = ''
                for page in file_data:
                    full_text = f"{full_text}\n{page['body']}"
                if len(full_text):
                        publications = extract_publications(full_text)
                        with output_filepath.open(mode='w', encoding='utf-8') as output_file:
                            json.dump(publications, output_file)
