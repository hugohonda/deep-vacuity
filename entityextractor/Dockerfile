FROM python:3.7.2-alpine3.8

RUN mkdir /src
WORKDIR /src
ADD . /src/
RUN pip install -r requirements.txt

CMD ["python", "/src/entityextractor.py"]