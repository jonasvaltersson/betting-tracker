FROM python:3.6-alpine3.7 as builder

RUN apk add --no-cache build-base libffi-dev gettext postgresql-dev \
	libxml2-dev \
	libxslt-dev

ARG PYPI_USERNAME
ARG PYPI_PASSWORD

COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 wheel -w /wheelhouse/ -r /tmp/requirements.txt


FROM python:3.6-alpine3.7

COPY --from=builder /wheelhouse /wheelhouse

RUN apk add --no-cache \
	libffi-dev \
	libxml2 \
	libxml2-dev \
	libxslt \
	libxslt-dev \
	postgresql-dev \
	py-gevent \
    ca-certificates  # for proper SSL-management

COPY . /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install --no-index --find-links=/wheelhouse -r /tmp/requirements.txt
RUN pip3 install .

CMD ["run-deploy"]
