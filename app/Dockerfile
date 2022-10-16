FROM python:3.9.6-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV IS_DOCKER_RUNNING Yes

COPY ./requirements.txt .

# install psycopg2 dependencies
RUN apk update
RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apk --purge del .build-deps

# copy entrypoint
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]