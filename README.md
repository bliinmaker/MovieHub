# MovieHub
### Uses .env variables:
PG_HOST
PG_PORT
PG_USER
PG_PASSWORD
PG_DBNAME

# creating docker container with postgres
docker run -d --name MovieHub -p 5555:5432 -e POSTGRES_DBNAME=movieHub \
    -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test postgres

# connecting to postgres with psql
psql -h 127.0.0.1 -p 5555 -U test movieHub # password test

# creating table
CREATE TABLE movie (name TEXT NOT NULL, rating FLOAT NOT NULL, actors TEXT NOT NULL);

# inserting values
INSERT INTO movie (name, rating, actors) VALUES ('movie', 1.0, 'Peter Parker');

# unique city constraint
ALTER TABLE movie ADD CONSTRAINT unique_movie UNIQUE(name, rating, actors);
