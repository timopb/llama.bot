FROM python:3.10

WORKDIR /chatbot
RUN mkdir models
COPY ./requirements.txt /chatbot/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /chatbot/requirements.txt


COPY ./app /chatbot/app

WORKDIR /chatbot/app

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8123"]
