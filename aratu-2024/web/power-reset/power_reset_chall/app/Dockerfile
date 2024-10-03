FROM python:3.9-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apk add --no-cache nginx

EXPOSE 80

CMD ["sh", "-c", "nginx && python app.py"]

