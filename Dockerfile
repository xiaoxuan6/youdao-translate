FROM python:3.10.16-alpine3.21

WORKDIR /app

RUN apk add --no-cache \
    nodejs \
    npm

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8888

CMD ["sh", "-c", "python main.py"]
