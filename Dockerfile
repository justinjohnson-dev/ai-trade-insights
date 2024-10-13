FROM python:3.11

WORKDIR /src

COPY . /src

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN tox

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]