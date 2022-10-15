# Metagame Project - Backend

API developed using Django and PostgreSQL.

## Docker instructions

1. You must have Docker installed (if you don't follow this [link](https://docs.docker.com/get-docker/)).

2. Define environment variables in a file named `.env.local`:
```
SECRET_KEY=
DEBUG=

SQL_ENGINE=
SQL_DATABASE=
SQL_USER=
SQL_PASSWORD=
SQL_HOST=
SQL_PORT=

DATABASE=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
```

3. Build the image and run the container:
```
docker-compose build && docker-compose up -d
```

5. Navigate to http://localhost:8000/api to check the documentation. 

6. If you'd like to down and remove the containers, run:
```
docker-compose down --volumes
```