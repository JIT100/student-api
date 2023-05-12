FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY ./requirements.txt  /code/requirements.txt
RUN pip install -r requirements.txt

COPY . /code

EXPOSE 5000

CMD ["python", "-u","app/main.py"]


