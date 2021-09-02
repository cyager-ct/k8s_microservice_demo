FROM python:3.8-alpine
COPY /flask /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]