FROM python:3.7.2-alpine3.8

RUN mkdir /src
WORKDIR /src
ADD . /src/
RUN pip install -r requirements.txt
RUN python -m nltk.downloader -d /usr/share/nltk_data stopwords

CMD ["python", "/src/main.py"]