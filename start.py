import os
import docker

client = docker.from_env()

print('Hello, ' + os.getlogin() + '! Please wait while all containers are starting.\n')

zabbix_env = client.containers.run("zabbix/zabbix-appliance:latest",
    name="zabbix-monitoring",
    ports={'10051/tcp': 10051, '80/tcp': 81},
    detach=True)


def get_ip(container, network_name="bridge"):
    nw = client.networks.get(network_name)
    ip = [_.attrs['NetworkSettings']['Networks']['bridge']['IPAddress'] for _ in nw.containers if _.id == container.id][0]
    return ip

zabbix_env_ip = get_ip(zabbix_env)

print("IP of Zabbix Server in Docker network is : " + zabbix_env_ip + "\n")

print("Containers started, have a nice day!\n")