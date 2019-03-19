
安装compose-compose

```
# https://github.com/docker/compose/releases

curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-compose
```

docker build -t myapi api
docker build -t myweb web

docker run --rm -d --name redis -v $PWD/redis:/data redis:4.0-alpine

docker run --rm -d --name api -p 8000:5000 --link redis myapi
docker run --rm -d --name web -p 8080:80 myweb

docker stop api web redis

docker rm api  # 如果run时没有--rm参数还需要手动删除容器

=====================


docker-compose build
docker-compose up
docker-compose up -d
docker-compose down


