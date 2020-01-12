import os
import docker

client = docker.from_env()

print('Hello, ' + os.getlogin() + '! Please wait while all containers are starting.\n')

zabbix = client.containers.run("zabbix/zabbix-appliance:latest",
    name="zabbix-monitoring",
    ports={'80/tcp': 81},
    detach=True)

zabbix_agent = client.containers.run("zabbix/zabbix-agent:latest",
    name="zabbix-agent",
    links={'zabbix-monitoring': 'zabbix-server'},
    volumes={'/Users/gpegel/Git/prombix/zabbix_config/': {'bind': '/etc/zabbix/', 'mode': 'rw'}},
    detach=True)

grafana = client.containers.run("grafana/grafana:latest",
    name="grafana",
    ports={'3000/tcp': 3000},
    environment=["GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource,alexanderzobnin-zabbix-app"],
    links={'zabbix-monitoring': 'zabbix-server'},
    detach=True)

def get_ip(container, network_name="bridge"):
    nw = client.networks.get(network_name)
    ip = [_.attrs['NetworkSettings']['Networks']['bridge']['IPAddress'] for _ in nw.containers if _.id == container.id][0]
    return ip

zabbix_ip = get_ip(zabbix)
zabbix_agent_ip = get_ip(zabbix_agent)
grafana_ip = get_ip(grafana)

print("IP of Zabbix Server in Docker network is : " + zabbix_ip + "\n")
print("IP of Zabbix Agent in Docker network is : " + zabbix_agent_ip + "\n")
print("IP of Grafana in Docker network is : " + grafana_ip + "\n")

print("Containers started, have a nice day!\n")