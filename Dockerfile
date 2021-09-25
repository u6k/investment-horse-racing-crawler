FROM python:3.8
LABEL maintainer="u6k.apps@gmail.com"

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get clean && \
    pip install pipenv

WORKDIR /var/myapp
VOLUME /var/myapp

COPY Pipfile Pipfile.lock ./
RUN pipenv install

CMD ["pipenv", "run", "help"]
