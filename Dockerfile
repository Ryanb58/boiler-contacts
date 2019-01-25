FROM python:3.7

ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt

EXPOSE 22222
CMD ["python", "-u", "app.py"]