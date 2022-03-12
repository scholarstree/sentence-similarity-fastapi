FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
COPY ./app /app