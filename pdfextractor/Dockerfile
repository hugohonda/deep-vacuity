FROM python:3.7.2-alpine3.8

RUN mkdir /src
RUN mkdir /helpers
WORKDIR /src
ADD . /src/
ADD . /helpers/
RUN pip install -r requirements.txt

RUN apk add --no-cache poppler-utils
ENTRYPOINT ["/usr/bin/pdftotext"]
CMD ["-", "-"] 

CMD ["python", "/src/pdfextractor.py"]