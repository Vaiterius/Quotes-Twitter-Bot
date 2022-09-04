FROM python:3.10.6-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./api_wrapper /code/api_wrapper

COPY ./app /code/app

CMD ["python3", "-m", "app.gooby_bot", "--host", "0.0.0.0", "--port", "8080"]