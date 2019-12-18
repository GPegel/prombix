import os
import docker

client = docker.from_env()

print('Hello, ' + os.getlogin() + '! Please wait while all containers are starting.\n')
mysql = client.containers.run("mysql:5.7",
    name="mysql-server",
    environment=["MYSQL_DATABASE=zabbix", "MYSQL_USER=zabbix", "MYSQL_PASSWORD=zabbix", "MYSQL_ROOT_PASSWORD=root_pwd"],
    detach=True)
print(mysql.id)

zabbix_server_mysql = client.containers.run("zabbix/zabbix-server-mysql:centos-4.4-latest",
    name="zabbix-server-mysql",
    environment=["DB_SERVER_HOST=mysql-server", "MYSQL_DATABASE=zabbix", "MYSQL_USER=zabbix", "MYSQL_PASSWORD=zabbix", "MYSQL_ROOT_PASSWORD=root_pwd"],
    links={'mysql-server': 'mysql'},
    ports={'10051/tcp': 10051},
    detach=True)
print(zabbix_server_mysql.id)

zabbix_web_nginx_mysql = client.containers.run("zabbix/zabbix-web-nginx-mysql:centos-4.4-latest",
    name="zabbix-web-nginx-mysql",
    environment=["DB_SERVER_HOST=mysql-server", "MYSQL_DATABASE=zabbix", "MYSQL_USER=zabbix", "MYSQL_PASSWORD=zabbix", "MYSQL_ROOT_PASSWORD=root_pwd"],
    links=[{'mysql-server':'mysql', 'zabbix-server-mysql':'zabbix-server'}],
    ports={'80/tcp': 81},
    detach=True)
print(zabbix_web_nginx_mysql.id)

zabbix_agent = client.containers.run("zabbix/zabbix-agent:centos-4.4-latest",
    name="zabbix-agent",
    environment=["ZBX_HOSTNAME=Zabbix server", "ZBX_SERVER_HOST=zabbix-server-mysql", "ZBX_METADATA=docker"],
    links=[{'mysql-server':'mysql', 'zabbix-server-mysql':'zabbix-server'}],
    ports={'10050/tcp': 10050},
    detach=True)
print(zabbix_agent.id)

print('Containers started, have a nice day!')
