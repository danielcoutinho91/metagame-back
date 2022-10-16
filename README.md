# Metagame Project - Backend

API developed using Django and PostgreSQL.

## Local instructions

1. Run your Postgres database on port `5432`.

2. Create `metagame` database.

3. Define environment variables in `.env.local` next to and according to `.env.example`.

4. Run migrations with:
```bash
cd app && python manage.py makemigrations && python manage.py migrate
```

5. Run server with:
```bash
python manage.py runserver
```

## Docker instructions

1. You must have Docker installed (if you don't follow this [link](https://docs.docker.com/get-docker/)).

2. Define environment variables in `.env.local` next to and according to `.env.example`.

3. Build the image and run the container:
```bash
docker-compose build && docker-compose up -d
```

5. Navigate to http://localhost:8000/api to check the documentation. 

6. If you'd like to down and remove the containers, run:
```bash
docker-compose down --volumes
```
