FROM python:3.7.0-stretch
LABEL mantainer="Vincenzo Palazzo v.palazzo1@studenti.unipi.it"
ADD . /code
WORKDIR code

RUN pip install -r requirements.txt
RUN python setup.py develop
EXPOSE 5000
CMD ["python", "monolith/app.py"]