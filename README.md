# MovieHub
### creating .env:
```bash
cp .env.template .env
```

# creating docker container with postgres
```bash
docker run -d --name MovieHub -p 5525:5432 -e PG_DBNAME=movieHub \
    -e PG_USER=test -e PG_PASSWORD=test postgres
```

# creating table
```bash
python3 main.py
```

# inserting values
commit Base.metadata.create_all(bind=engine)
uncommit Session
```bash
python3 main.py
```

# inserting server
```bash
python3 server.py
```