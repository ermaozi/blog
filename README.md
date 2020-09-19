> 由于条件有限, 目前仅在 CentOS 7.8 系统中进行过部署调试, 其他场景会尽可能的在后期进行补充. 同时欢迎大家提供其他场景的部署案例, 在此提前表示感谢.

*资料更新于 2020-09-17*

# 部署

默认部署环境为全新环境, 如果部分软件已完成安装, 可重新安装或跳过相关步骤

## 自动部署

CentOS 7 环境中执行以下命令:

``` shell
sh <(curl -sL https://git.io/blog-install)
```

自动部署目前仅支持全量部署(Nginx 启动), 需要选择性部署的同学可以参考手动部署方式


## 手动部署

### 安装 python 相关

安装依赖, 缺失依赖会导致编译失败

``` shell
yum update -y
yum groupinstall -y 'Development Tools'
yum install -y gcc openssl-devel bzip2-devel libffi-devel
yum install -y python36-devel
```

下载与编译 Python 3.6
``` shell
yum install -y python36
python3 -m pip install virtualenv
```

创建虚拟环境与项目依赖

``` shell
project_root=~/blog  # 项目在本机的路径

cd $project_root
python3 -m virtualenv venv
source venv/bin/activate  # 使用 deactivate 可退出虚拟环境
pip install -r requirements.txt
```

### 安装数据库

本项目使用 docker 下的 mariadb 数据库, 不喜欢 mariadb 的同学可以选择其他数据库. 同时, 数据库不一定要装在当前节点, 云服务器存储较小的情况可以考虑安装在其他节点

安装 docker

``` shell
yum install -y docker
docker pull mariadb  # 拉取超时可多试几次, 镜像拉取成功后可以通过 docker images 命令进行查看
docker run --name mariadb -p 3306:3306 -e MYSQL_ROOT_PASSWORD=输入数据库root用户的密码 -v /data/mariadb/data:/var/lib/mysql -d mariadb  # 参数详解见下方
docker container update --restart=always mariadb
docker exec mariadb mysql -uroot -pyueyue@0129 -e "create database blog;"
docker exec mariadb mysql -uroot -pyueyue@0129 -e "create database test_blog;"
```

docker 参数详解

　　--name 启动容器设置容器名称为 mariadb

　　-p 设置容器的 3306 端口映射到主机 3306 端口

　　-e MYSQL_ROOT_PASSWORD 设置环境变量数据库 root 用户密码为输入数据库 root 用户的密码 (必改)

　　-v 设置容器目录 /var/lib/mysql 映射到本地目录 /data/mariadb/data

　　-d 后台运行容器 mariadb 并返回容器 id

其他 docker 命令可自行搜索

### 修改配置文件

本项目配置文件位于根目录下的 conf 目录

其中 flask 目录下的配置文件需要个人参考注释手动修改, 同时将 private/private_template.py 文件改名为 private.py

需要注意的是 private.py 文件内容千万不要公开, 上传至公开库或是在生产环境使用 Debug 模式都会泄露其信息

本项目在 .gitignore 文件中已经配置了忽略 private.py 文件, 正常操作并不会上传该文件, 但是在每一次提交代码时依旧需要仔细检查

**信息泄露的后果十分严重, 轻则被人删库, 重则被人利用从事违法犯罪活动, 切记保护好个人隐私**

### 安装 nginx (选装)

本项目 nginx 的主要目的是为了转发 80 端口, 并使网站可以通过 https 访问, 没有该需求的同学可以跳过本步骤

安装 nginx

``` shell
yum install -y nginx

# 创建软连接, 也可以直接把该目录下的所有文件手动拷贝到 /etc/nginx/
project_root=~/blog  # 项目在本机的路径

cd $project_root
nginx_conf=$(pwd)/conf/nginx
ln -sf $nginx_conf/nginx.conf /etc/nginx/
ln -snf $nginx_conf/ssl /etc/nginx/
```

### 安装 acme.sh (选装)

本项目安装 acme.sh 的主要目的是为了自动获取证书, 使网站通过 https 访问时不会出现不安全的提示, 没有该需求的同学可以跳过本步骤

安装 acme.sh

``` shell
project_root=~/blog  # 项目在本机的路径
domain=ermao.net  # 修改成你的域名

nginx_conf=$(cd $project_root;pwd)/conf/nginx

wget -O - https://get.acme.sh | sh

~/.acme.sh/acme.sh --issue -d $domain --debug --standalone -k ec-256
~/.acme.sh/acme.sh  --installcert  --domain $domain --key-file /root/blog/conf/nginx/ssl/privkey.pem --fullchain-file /root/blog/conf/nginx/ssl/fullchain.pem --reloadcmd  "systemctl restart nginx.service"

```

### 定时任务 (选做)

本项目启动定时任务的主要目的是为了定时重启 nginx 以及通过 certbot-auto 续签证书, 没有该需求的同学可以跳过本步骤

``` shell
project_root=~/blog  # 项目在本机的路径

cd $project_root
crontab ./conf/crontab/crontab.cron
```

## 启动

启动时需要完成 **部署** 步骤中的对应操作

### 初始化日志目录

由于部分日志无法自动创建目录, 所以需要手动进行创建

``` shell
mkdir -p /var/log/blog/uwsgi/
mkdir -p /var/log/blog/nginx/
mkdir -p /var/log/blog/flask/
```

### 直接启动

直接启动可以作为测试用默认开启 Debug 模式

``` shell
project_root=~/blog  # 项目在本机的路径

cd $project_root
source ./venv/bin/activate
python manage.py >> /var/log/blog/flask/flask-$(date +%Y%m%d).log 2>&1
```

后台启动

``` shell
project_root=~/blog  # 项目在本机的路径

cd $project_root
source ./venv/bin/activate
nohup python manage.py >> /var/log/blog/flask/flask-$(date +%Y%m%d).log 2>&1 &
```

启动成功后可以访问 http://你的域名或ip 进行访问

日志位于 `/var/log/blog/flask/`

### Uwsgi 方式启动

修改 uwsgi.ini

``` shell
project_root=~/blog  # 项目在本机的路径

cd $project_root
vi ./conf/uwsgi/uwsgi.ini
```

将配置文件中的 `#http = 0.0.0.0:80` 行首的 `#` 删除
同时在 `socket = 127.0.0.1:8000` 行首添加 `#`
保存退出后执行以下命令

``` shell
project_root=~/blog  # 项目在本机的路径

cd $project_root
source ./venv/bin/activate
uwsgi --ini ./conf/uwsgi/uwsgi.ini
```

启动成功后可以访问 http://你的域名或ip 进行访问

日志位于 `/var/log/blog/uwsgi/uwsgi.log`

可以使用 `pkill -f -9 uwsgi` 停止服务

### Nginx 方式启动

修改 nginx.conf

``` shell
project_root=~/blog  # 项目在本机的路径

cd $project_root
vi ./conf/nginx/nginx.conf
```
将配置文件中的 server_name 参数改为自己的域名

启动 uwsgi 与 nginx

``` shell
project_root=~/blog  # 项目在本机的路径

cd $project_root
# 启动 uwsgi
cp ./conf/uwsgi/uwsgi.ini.default ./conf/uwsgi/uwsgi.ini
source ./venv/bin/activate
uwsgi --ini ./conf/uwsgi/uwsgi.ini

systemctl start nginx.service
```

启动成功后可以访问 https://你的域名或ip 进行访问, 同时访问 http://你的域名或ip 时会自动跳转至 https

日志位于 `/var/log/blog/nginx/access.log`

可以使用 `systemctl stop nginx.service` 停止服务


# 鸣谢

![avatar](web/static/img/readme/fandalong-01.jpg)

这是饭大龙，很显然它是一只猫。感谢饭大龙在我敲代码的时候踩我键盘、咬我网线。
如果本项目对您有所帮助，或许可以考虑请大龙吃个罐头。

