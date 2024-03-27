#### Setup Redis

##### Make the docker-compose.yml file with this content 
```bash
version: '3'

services:
  redis:
    image: redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

# And then run this one, redis sẽ chạy trên pod 6379
docker-compose up -d

```bash
root@serverlocal:~# docker ps
CONTAINER ID   IMAGE                               COMMAND                  CREATED              STATUS              PORTS                                       NAMES
1fcd6b7e85b3   redis                               "docker-entrypoint.s…"   About a minute ago   Up About a minute   0.0.0.0:6379->6379/tcp, :::6379->6379/tcp   ActsOne
```