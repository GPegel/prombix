import os
import sys
import docker
import time
import json
import requests
from requests.auth import HTTPBasicAuth

client = docker.from_env()

def lets_start():
    print('Hello, ' + os.getlogin() + '! Please wait while all containers are starting.\n')

lets_start()

zabbix = client.containers.run("zabbix/zabbix-appliance:latest",
    name="zabbix-monitoring",
    ports={'80/tcp': 80},
    network="bridge",
    detach=True)

zabbix_agent = client.containers.run("zabbix/zabbix-agent:latest",
    name="zabbix-agent",
    links={'zabbix-monitoring': 'zabbix-server'},
    volumes={'/Users/gerhardpegel/Git/prombix/config/zabbix_config/': {'bind': '/etc/zabbix/', 'mode': 'ro'},
             '/Users/gerhardpegel/Git/prombix/config/zabbix_agentd.d/': {'bind': '/etc/zabbix/zabbix_agentd.d/', 'mode': 'ro'}},
    network="bridge",
    detach=True)

grafana = client.containers.run("grafana/grafana:latest",
    name="grafana",
    ports={'3000/tcp': 3000},
    environment=["GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource,alexanderzobnin-zabbix-app"],
    volumes={'/Users/gerhardpegel/Git/prombix/config/grafana_config/': {'bind': '/etc/grafana/', 'mode': 'rw'}},
    links={'zabbix-monitoring': 'zabbix-server'},
    network="bridge",
    detach=True)

prometheus = client.containers.run("prom/prometheus:latest",
    name="prometheus",
    ports={'9090/tcp': 9090},
    volumes={'/Users/gerhardpegel/Git/prombix/config/prometheus_config/': {'bind': '/etc/prometheus/', 'mode': 'ro'}},
    network="bridge",
    detach=True)

node_exporter = client.containers.run("quay.io/prometheus/node-exporter",
    name="node-exporter",
    network="bridge",
    detach=True)

def get_ip(container, network_name="bridge"):
    nw = client.networks.get(network_name)
    ip = [_.attrs['NetworkSettings']['Networks']['bridge']['IPAddress'] for _ in nw.containers if _.id == container.id][0]
    return ip

zabbix_ip = get_ip(zabbix)
zabbix_agent_ip = get_ip(zabbix_agent)
grafana_ip = get_ip(grafana)
prometheus_ip = get_ip(prometheus)
node_exporter_ip = get_ip(node_exporter)

print("IP of Zabbix Server in Docker network is : " + zabbix_ip + "\n")
print("IP of Zabbix Agent in Docker network is : " + zabbix_agent_ip + "\n")
print("IP of Grafana in Docker network is : " + grafana_ip + "\n")
print("IP of Prometheus in Docker network is : " + prometheus_ip + "\n")
print("IP of Prometheus Node-Exporter in Docker network is : " + node_exporter_ip + "\n")

def wait():
    print("Waiting 45 seconds for all containers to settle.\n")
    time.sleep(45)
wait()

headers = {'content-type': 'application/json'}
zabbix_username = "Admin"
zabbix_password = "zabbix"
url_zabbix_api = "http://0.0.0.0/api_jsonrpc.php"
hostname = "prometheus"
host_dns = "prometheus.intern.whatever.com"
host_group_id = "2"
template_id = "10285"

def get_aut_key_zabbix():
    payload= {'jsonrpc': '2.0','method':'user.login','params':{'user':zabbix_username,'password':zabbix_password},'id':'1'}
    r = requests.post(url_zabbix_api, data=json.dumps(payload), headers=headers, verify=True, auth=HTTPBasicAuth(zabbix_username,zabbix_password))
    if  r.status_code != 200:
        print('problem -key')
        print(r.status_code)
        print(r.text)
        sys.exit()
    else:
        result=r.json()
        auth_key_zabbix=result['result']
        return auth_key_zabbix

def create_host(auth_key_zabbix):
    payload={
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": {
            "host": hostname,
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": prometheus_ip,
                    "dns": host_dns,
                    "port": "10050"
                }
            ],
            "groups": [
                {
                    "groupid": host_group_id
                }
            ],
            "templates": [
                {
                    "templateid": template_id
                }
            ],
        },
        "auth": auth_key_zabbix,
        "id": 1
    }

    r = requests.post(url_zabbix_api, data=json.dumps(payload), headers=headers, verify=True, auth=HTTPBasicAuth(zabbix_username,zabbix_password))
    if  r.status_code != 200:
        print('problem -request')
        sys.exit()
    else:
        try:
            result=r.json()['result']
            host_id=result['hostids'][0]
            return host_id
        except:
            result=r.json()['error']
            print('error - creating host')
            print(result)
            sys.exit()

auth_key_zabbix=get_aut_key_zabbix()
host_id=create_host(auth_key_zabbix)

def enable_zabbix_plugin():
    url = "http://admin:admin@localhost:3000/api/plugins/alexanderzobnin-zabbix-app/settings/"
    payload = "{\n  \"name\": \"Zabbix\",\n  \"type\": \"app\",\n  \"id\": \"alexanderzobnin-zabbix-app\",\n  \"enabled\": true,\n  \"basicAuth\": true,\n  \"basicAuthUser\": \"admin\",\n  \"secureJsonData\": {\n    \"basicAuthPassword\": \"admin\"\n  }\n}"
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data = payload)

def add_zabbix_datasource():
    url = "http://admin:admin@localhost:3000/api/datasources"
    payload = "{\n    \"name\": \"Zabbix\",\n    \"type\": \"alexanderzobnin-zabbix-datasource\",\n    \"url\": \"http://0.0.0.0/api_jsonrpc.php\",\n    \"access\": \"direct\",\n    \"basicAuth\": false,\n    \"isDefault\": true,\n    \"jsonData\": {\n        \"addThresholds\": false,\n        \"alerting\": false,\n        \"alertingMinSeverity\": 3,\n        \"dbConnectionDatasourceId\": null,\n        \"dbConnectionEnable\": false,\n        \"disableReadOnlyUsersAck\": false,\n        \"password\": \"zabbix\",\n        \"trends\": false,\n        \"username\": \"Admin\",\n        \"zabbixVersion\": 4\n    }\n}"
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data = payload)

enable_zabbix_plugin()
add_zabbix_datasource()

def the_end():
    print("Containers started, have a nice day!\n")

the_end()