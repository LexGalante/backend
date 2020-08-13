run:
    uvicorn src.main:app --reload

database-test:
    docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v postgres_data:/data -d -t postgres
