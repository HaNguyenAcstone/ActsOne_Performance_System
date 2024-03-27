docker run --name ActsOne -d -p 6379:6379 redis

```bash
root@serverlocal:~# docker ps
CONTAINER ID   IMAGE                               COMMAND                  CREATED              STATUS              PORTS                                       NAMES
1fcd6b7e85b3   redis                               "docker-entrypoint.s…"   About a minute ago   Up About a minute   0.0.0.0:6379->6379/tcp, :::6379->6379/tcp   ActsOne
```