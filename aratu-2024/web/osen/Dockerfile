FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    python3-pip \
    nodejs \
    npm \
    wget \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash flask_user && useradd -ms /bin/bash express_user

WORKDIR /app

COPY ./app_py/requirements.txt ./app_py/
RUN pip install --no-cache-dir -r ./app_py/requirements.txt

COPY ./app_js/package*.json ./app_js/
RUN cd ./app_js && npm install

COPY ./app_py /app/app_py
COPY ./app_js /app/app_js


COPY flag.txt /flag.txt
RUN chmod o+r /flag.txt; mv /flag.txt /flag-$(head /dev/urandom | tr -dc 'A-Za-z0-9' | head -c 12).txt

RUN chown -R flask_user:flask_user /app/app_py && \
    chown -R express_user:express_user /app/app_js

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 5000

CMD ["/usr/bin/supervisord"]