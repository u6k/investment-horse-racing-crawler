FROM python:3.8
LABEL maintainer="u6k.apps@gmail.com"

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install tor privoxy && \
    apt-get clean && \
    pip install pipenv

RUN echo 'forward-socks5 / localhost:9050 .' >/etc/privoxy/config

WORKDIR /var/myapp
VOLUME /var/myapp

COPY Pipfile Pipfile.lock ./
RUN pipenv install

CMD ["pipenv", "run", "help"]
