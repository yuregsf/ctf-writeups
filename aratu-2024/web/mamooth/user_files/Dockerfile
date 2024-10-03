FROM webdevops/php-nginx:8.0


# install gcc
RUN apt-get update && apt-get install -y gcc make autoconf libc-dev pkg-config

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY . .

# compile
RUN gcc -o /readflag /app/readflag.c

RUN chown root:root /readflag
RUN chmod 400 /readflag
RUN chmod u+s /readflag
COPY flag.txt /flag.txt
RUN rm -f /app/flag.txt

RUN chown root:root /flag.txt; chmod 400 /flag.txt

RUN chown -R www-data:www-data /app
RUN chmod -R 755 /app

# Expose the port the app runs on
EXPOSE 80

RUN head -c 16 /dev/urandom | xxd -ps | head -n 1 | tr -d '\n' > /secret

ENTRYPOINT ["/entrypoint"]
CMD ["supervisord"]
