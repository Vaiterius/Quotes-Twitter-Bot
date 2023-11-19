FROM arm64v8/python:3.12-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./api_wrapper /code/api_wrapper

COPY ./app /code/app

CMD ["python3", "-m", "app.bot", "--host", "0.0.0.0", "--port", "8080"]