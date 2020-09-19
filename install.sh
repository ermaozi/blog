#!/bin/bash
# Author: ErMaozi
# github: https://github.com/ermaozi/blog

read -p "本次安装中途会停用 80/443/3306 端口, 是否继续? [Y/n]" input
echo $input
[[ "Yy" =~ $input ]] || exit 1
read -p "本次安装将会在 /root 下创建 blog 目录, 并且会在 /var/log 下创建 blog 目录, 是否继续? [Y/n]" input
echo $input
[[ "Yy" =~ $input ]] || exit 1

project_root=~/blog

error_log(){
	echo "$1 执行失败, 请参考手动部署文档进行 $1"
	echo "文档地址: https://github.com/ermaozi/blog/blob/master/README.md"
	echo "如果文档方案不可行或描述不够详细, 可以加QQ群 373223696 进行咨询"
	echo "同时欢迎发送邮件至 admin@ermao.net 反馈问题"
	exit 1
}

install_tool(){
	echo "安装 $1 ..."
	$@ > /dev/null 2>&1 ||  yum install -y $1 > /dev/null 2>&1
	$@ || error_log "$1 安装失败"
	echo "$1 安装成功"
}

get_user_info(){
	read -p "请输入您解析到本机的域名: " input
	if [ ! $(echo "$input" | grep -E "[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?") ];then
		echo "域名不合法"
		exit 1
	fi
	host_ip=$(curl http://txt.go.sohu.com/ip/soip|grep -P "\d+.\d+.\d+.\d+" -o) > /dev/null 2>&1
	domain_ip=$(ping -c 2 $input | head -2 | tail -1 | awk '{print $5}' | sed 's/[(:)]//g') > /dev/null 2>&1
	if [ x"$host_ip" != x"$domain_ip" ];then
		echo "域名解析ip与本机ip不同!"
		exit 1
	fi
	domain=$input
	
	read -p "请输入您预设的数据库密码(自己设置, 自己记住): " input
	db_pwd=$input
}

init_sys(){
	echo "切换 yum 源"
	rpm -ivh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm  # 切换 yum 源主要目的是下载 nginx, 同时保证其他工具同源, 以免因差异导致的问题
	echo "更新系统"
	echo "如果系统长时间未更新, 该步骤执行时间会较长, 请耐心等待..."
	yum update -y > /dev/null 2>&1  # 更新系统, 这一步可能浪费时间比较多, 但是旧的系统总会有隐患
	echo "系统更新成功!"
	
	echo "安装依赖"
	yum groupinstall -y 'Development Tools' > /dev/null 2>&1  # 安装开发套件, 支撑软件运行环境
	yum install -y gcc openssl-devel bzip2-devel libffi-devel > /dev/null 2>&1  # 安装编译套件, 部分属于历史遗留问题, 后期会酌情删减
	yum install -y python36-devel > /dev/null 2>&1  # uwsgi 的依赖, 必须要装, 否则可能导致 uwsgi 无法安装
	yum install -y socat > /dev/null 2>&1  # acme.sh 的依赖, 必须要装, 否则可能导致证书无法申请
	echo "依赖安装成功!"
}

install_tools(){
	echo "安装工具"
	install_tool wget --version  # wget 是一个在网络上进行下载的工具, 本项目用于安装 acme.sh
	install_tool git --version  # git 是一个开源的分布式版本控制系统, 本项目用于...嗯, 我不相信这里有人不会 git
	install_tool python3.6 --version  # python 是一种解释型、面向对象、动态数据类型的高级程序设计语言, 本项目作为后端主语言
	install_tool nginx -v  # Nginx 是一款轻量级的Web服务器、反向代理服务器, 本项目用于转发 uwsgi 端口
	install_tool lsof -v   # lsof 是一个查看当前系统文件的工具, 本项目用于通过端口查询进程
	install_tool docker -v  # Docker 是一个开源的应用容器引擎, 本项目用于安装 mariadb 数据库
	systemctl start docker.service > /dev/null 2>&1  # docker 安装后需要启动服务
	python3.6 -m virtualenv --version || python3.6 -m pip install virtualenv > /dev/null 2>&1  # virtualenv 是一个创建隔绝的Python环境的工具, 在本项目中就是干这个用的
	python3.6 -m virtualenv --version || error_log "virtualenv 安装失败"
	
	echo "克隆项目代码"
	[ -f ~/blog/LICENSE ] || cd ~;git clone https://github.com/ermaozi/blog.git > /dev/null 2>&1  # 克隆项目代码
	[ -f ~/blog/LICENSE ] || error_log "克隆项目代码"
	echo "项目代码克隆成功!"
	
	echo "安装 acme.sh"
	[ -f ~/.acme.sh/acme.sh ] || wget -O - https://get.acme.sh | sh > /dev/null 2>&1  # acme.sh 是一个自动化证书管理环境脚本, 本项目用于自动化申请证书
	[ -f ~/.acme.sh/acme.sh ] || error_log "acme.sh 安装"
	echo "acme.sh 安装成功!"
}


get_blog_project(){
	cd $project_root
	echo "创建虚拟环境"
	python3.6 -m virtualenv venv > /dev/null 2>&1  # 创建虚拟环境 venv
	source venv/bin/activate > /dev/null 2>&1  # 使用 deactivate 可退出虚拟环境
	echo "安装 python 第三方库"
	pip install -r requirements.txt > /dev/null 2>&1  # 安装项目所需的第三方库
}

install_mariadb(){
	echo "安装数据库"
	cd $project_root
	
	# 检查是否存在 mariadb 容器
	if [[ $(docker ps --format "{{.Names}}"|grep mariadb) ]];then
	    echo "mariadb 数据库已存在, 请自行创建 blog 数据库与 test_blog 数据库"
		return
	fi

	echo "数据库密码将自动更新至 $project_root/conf/flask/private/private.py 配置文件中"
	echo "该配置文件内容均为敏感内容, 需要严格保密, 切勿将此文件上传至公开库或在公开环境暴露"
	echo "否则将有可能使您的网站与设备处于极度危险的状态"
	echo ""
	
	echo "修改项目中的配置文件"
	cp -f $project_root/conf/flask/private/private_template.py $project_root/conf/flask/private/private.py  > /dev/null 2>&1
	sed -i "s/ PASSWORD = .*  #/ PASSWORD = \'$db_pwd\'  #/" $project_root/conf/flask/private/private.py  > /dev/null 2>&1
	
	echo "拉取 mariadb 镜像"
	echo "过程受网速影响, 可能较慢, 请耐心等待"
	docker pull mariadb  # 拉取超时可多试几次, 镜像拉取成功后可以通过 docker images 命令进行查看
	echo "镜像拉取成功! 安装完成后可通过 docker images 命令进行查看"
	mkdir -p /data/mariadb/data  # 创建数据存储目录
	
	echo "创建容器"
	kill -9 $(lsof -i:3306 -t)  # 杀死 3306 端口
	docker run --name mariadb -p 3306:3306 -e MYSQL_ROOT_PASSWORD=$db_pwd -v /data/mariadb/data:/var/lib/mysql -d mariadb > /dev/null 2>&1
	echo "设置容器自启动"
	docker container update --restart=always mariadb > /dev/null 2>&1  # 设置容器自启动
	docker restart mariadb -t 20 > /dev/null 2>&1  # 部分场景 mariadb 容器不会自启动, 这里重启一下
	sleep 10s
	
	echo "创建生产环境数据库与测试环境数据库"
	docker exec mariadb mysql -uroot -p$db_pwd -e "create database blog;" > /dev/null 2>&1
	docker exec mariadb mysql -uroot -p$db_pwd -e "create database test_blog;" > /dev/null 2>&1
}


conf_nginx(){
	cd $project_root
	echo "修改 nginx 配置, 并创建配置目录软连接"
	nginx_conf=$(pwd)/conf/nginx
	domain_conf=$domain
	[[ $(echo "$domain" | grep -o '\.'|wc -l) == 1 ]] && domain_conf="$domain www.$domain"  # 只输入二级域名时自动添加 www 三级域名
	sed -i "s/server_name .*;/server_name $domain_conf;/" $nginx_conf/nginx.conf > /dev/null 2>&1  # 写入 nginx 配置文件
	
	# 创 nginx 配置文件建软连接至系统配置路径
	ln -sf $nginx_conf/nginx.conf /etc/nginx/
	ln -snf $nginx_conf/ssl /etc/nginx/

	echo "关闭 80 端口与 443 端口"
	kill -9 $(lsof -i:80 -t)
	kill -9 $(lsof -i:443 -t)

	echo "申请证书"
	~/.acme.sh/acme.sh --issue -d $domain --debug --standalone > /dev/null 2>&1
	~/.acme.sh/acme.sh  --installcert  --domain $domain --key-file $nginx_conf/ssl/privkey.pem --fullchain-file $nginx_conf/ssl/fullchain.pem > /dev/null 2>&1

	if [ ! -f $nginx_conf/ssl/privkey.pem ] || [ ! -f $nginx_conf/ssl/fullchain.pem ]; then
	    error_log "申请证书"
	fi
	echo "证书申请成功"

	echo "配置定时任务"
	crontab $project_root/conf/crontab/crontab.cron > /dev/null 2>&1
}

start_project(){
	cd $project_root
	echo "初始化日志目录"
	mkdir -p /var/log/blog/uwsgi/
	mkdir -p /var/log/blog/nginx/
	mkdir -p /var/log/blog/flask/

	echo "启动 Uwsgi"
	uwsgi --ini ./conf/uwsgi/uwsgi.ini > /dev/null 2>&1
	[[ $(lsof -i:8000 -t) ]] || error_log "启动 Uwsgi"
	echo "Uwsgi 启动成功"

	echo "启动 Nginx"
	systemctl start nginx.service || [[ nforcing =~ $(getenforce) ]] && setenforce 0; systemctl start nginx.service > /dev/null 2>&1
	sleep 5s
	[[ $(lsof -i:80 -t) ]] || error_log "启动 Nginx"
	[[ $(lsof -i:443 -t) ]] || error_log "启动 Nginx"
	echo "启动成功!"
}

get_user_info || exit 1
init_sys || exit 1
install_tools || exit 1
get_blog_project || exit 1
install_mariadb || exit 1
conf_nginx || exit 1
start_project || exit 1

echo -e "\n-----------------------------------------------------------------\n"
echo "已经完成部署"
echo "可以通过 https://$domain 来访问您的博客"
echo "在 $project_root/conf/ 中可以看到本项目的各种配置"
echo "运行过程中若发现问题, 可以在 /var/log/blog/ 目录中查看日志"
echo "同时欢迎加群交流, QQ群号: 373223696"
echo "有问题或建议也非常欢迎您发送邮件反馈, 邮箱地址: admin@ermao.net" 
