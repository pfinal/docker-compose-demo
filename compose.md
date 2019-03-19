
安装compose-compose

```
# https://github.com/docker/compose/releases

curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-compose
```


构建镜像

```
docker build -t api api/
docker build -t web web/
```

启动容器

```
docker run -d --name redis -v $PWD/redis-data:/data redis:4.0-alpine


docker run -d --name mysql -v $PWD/mysql-data:/var/lib/mysql \
-e MYSQL_DATABASE=testdb \
-e MYSQL_ROOT_PASSWORD=123456 
mysql:5.5 --default-time-zone=+8:00


docker run -d --name api -p 8000:5000 --link redis --link mysql \
-e MYSQL_HOST=db \
-e MYSQL_USER=root \
-e MYSQL_PASSWORD=123456 \
-e MYSQL_PORT=3306 \
-e MYSQL_DATABASE=testdb \
-e REDIS_HOST=redis \
-e REDIS_PORT=6379 \
api


docker run -d --name web -p 8080:80
```

查看日志
docker logs -f api

停止
docker stop redis mysql api web

删除
docker rm redis mysql api web

docker ps -a

=====================


docker-compose build
docker-compose up
docker-compose up -d
docker-compose down


docker ps | grep db
docker exec counter_db_1 bash
mysql -uroot -p123456

删除镜像 (留下 nginx redis mysql)
docker rmi web api counter_web counter_api



