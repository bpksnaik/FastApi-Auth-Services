FROM python:latest

WORKDIR /app

COPY ./requirement.txt /app

RUN pip install --no-cache-dir --upgrade -r requirement.txt

COPY ./ app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]