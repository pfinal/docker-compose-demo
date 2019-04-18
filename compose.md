

Docker Compose是一个用于 定义 和 运行 多容器Docker应用程序的工具。
使用YAML文件来配置，然后使用单个命令，您可以从配置中创建并启动所有服务


使用Compose基本上是一个三步过程：

1. 定义您的应用程序环境，Dockerfile以便可以在任何地方进行复制
2. 定义构成应用程序的服务，docker-compose.yml 以便它们可以在隔离的环境中一起运行
4. 运行 docker-compose up 启动并运行整个应用程序


文档
https://docs.docker.com/compose/

安装compose-compose

```
# https://github.com/docker/compose/releases

curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-compose
```


compose-file版本与docker版本对应关系
https://docs.docker.com/compose/compose-file/

Compose file format    Docker Engine版本
3.7                    18.06.0+
3.4                    17.09.0+
3.2                    17.04.0+

yaml格式是一种配置文件，有人认为 json 的写法不爽，所以弄了这个

1. 大小写敏感            json 里也是大小写敏感的
2. 使用缩进表示层级关系    json 中使用 {} 的嵌套表示层级
   缩进时不允许使用Tab键，只允许使用空格
   缩进的空格数目不重要，只要相同层级的元素左侧对齐即可
3. # 表示注释            json文件中不允许写注释
   从这个字符一直到行尾，都会被解析器忽略

数据结构:
1. 对象 

```
# conf.yml
AppName: demo
hash: { name: Steve, foo: bar }    # 允许另一种写法，将所有键值对写成一个行内对象
```
转换为 json 为：

```
{
    { "AppName": "demo" },
    { "hash": { "name": "Steve", "foo": "bar" } }
}
```

2. 数组

```
# conf.yml
Animal:
 - Cat
 - Dog
 - Goldfish
```

转换为 json 为： { "Animal": [ "Cat", "Dog", "Goldfish" ] }

数组也可以采用行内表示法  animal: [Cat, Dog]


3. 字符串

单引号和双引号都可以使用，双引号不会对特殊字符转义。
单引号之中如果还有单引号，必须连续使用两个单引号转义 str: 'labor''s day' 

```
# conf.yml
# 正常情况下字符串不用写引号
str: 这是一行字符串
# 字符串内有空格或者特殊字符时需要加引号
str: '内容： 字符串'
```

4. null

```
# conf.yml
parent: ~
```

.yml 中 ~ 表示 null，转换为 json 为：

```
{ "parent": null }
```

布尔值用true和false表示

YAML 允许使用两个感叹号，强制转换数据类型

```
e: !!str 123
f: !!str true
```
转为 JavaScript 如下
{ e: '123', f: 'true' }

=============


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
-e MYSQL_ROOT_PASSWORD=123456 \
mysql:5.5 --default-time-zone=+8:00


docker run -d --name api -p 8000:5000 --link redis --link mysql \
-e MYSQL_HOST=mysql \
-e MYSQL_USER=root \
-e MYSQL_PASSWORD=123456 \
-e MYSQL_PORT=3306 \
-e MYSQL_DATABASE=testdb \
-e REDIS_HOST=redis \
-e REDIS_PORT=6379 \
api


docker run -d --name web -p 8080:80 web
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



