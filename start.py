import os
import sys
import docker
import time
import glob
from pyzabbix import ZabbixAPI, ZabbixAPIException


client = docker.from_env()

path = '/Users/gerhardpegel/Git/prombix/config/zabbix_templates'
zabbix_hosts_path = '/Users/gerhardpegel/Git/prombix/config/zabbix_hosts'

print('Hello, ' + os.getlogin() + '! Please wait while all containers are starting.\n')

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

print("Waiting 45 seconds for all containers to settle.\n")
time.sleep(45)

zabbix_server = 'http://0.0.0.0:80'
csvfile = open(zabbix_hosts_path+'/list.csv', 'r')

zapi = ZabbixAPI(zabbix_server)

# Login to the Zabbix API
#zapi.session.verify = False
zapi.login("Admin", "zabbix")

print("Connected to Zabbix API Version %s" % zapi.api_version())

def get_hostgroup_id(hostgroup):
    data = zapi.hostgroup.get(filter={'name': hostgroup})
    if data != []:
        hostgroupid = data[0]['groupid']
    else:
        raise Exception('Could not find hostgroupID for: ' + hostgroup)
    return str(hostgroupid)

def add_host(ip, hostname, hostgroups):
    interface_list = [{
        "type": 1,
        "main": 1,
        "useip": 1,
        "ip": str(ip),
        "dns": '',
        "port": "10050"
    }]

    groups = list()

    for g in hostgroups:
        groups.append({"groupid": str(get_hostgroup_id(g))})


    query = {
        'host': str(hostname),
        'groups': groups,
        'proxy_hostid': '0',
        'status': '0',
        'interfaces': interface_list,
        'inventory_mode': 1,
        'inventory': {
            'name': str(hostname)
        }
    }

    result = zapi.host.create(**query)

for l in csvfile.readlines():
    if l.strip().startswith('#') or not ',' in l:
        continue

    myargs = l.strip().split(',')
    try:
        add_host(myargs[0], myargs[1], myargs[2].split(':'))
        print("Added %s" %myargs[0])
    except:
        print("Failed to add %s" %myargs[0])
        pass

rules = {
    'applications': {
        'createMissing': True,
    },
    'discoveryRules': {
        'createMissing': True,
        'updateExisting': True
    },
    'graphs': {
        'createMissing': True,
        'updateExisting': True
    },
    'groups': {
        'createMissing': True
    },
    'hosts': {
        'createMissing': True,
        'updateExisting': True
    },
    'images': {
        'createMissing': True,
        'updateExisting': True
    },
    'items': {
        'createMissing': True,
        'updateExisting': True
    },
    'maps': {
        'createMissing': True,
        'updateExisting': True
    },
    'screens': {
        'createMissing': True,
        'updateExisting': True
    },
    'templateLinkage': {
        'createMissing': True,
    },
    'templates': {
        'createMissing': True,
        'updateExisting': True
    },
    'templateScreens': {
        'createMissing': True,
        'updateExisting': True
    },
    'triggers': {
        'createMissing': True,
        'updateExisting': True
    },
    'valueMaps': {
        'createMissing': True,
        'updateExisting': True
    },
}

if os.path.isdir(path):
    files = glob.glob(path+'/*.xml')
    for file in files:
        print('Pushing this template to Zabbix:' + file)
        with open(file, 'r') as f:
            template = f.read()
            try:
                zapi.confimport('xml', template, rules)
            except ZabbixAPIException as e:
                print(e)
        print('Template pushed successfully\n')
elif os.path.isfile(path):
    files = glob.glob(path)
    for file in files:
        with open(file, 'r') as f:
            template = f.read()
            try:
                zapi.confimport('xml', template, rules)
            except ZabbixAPIException as e:
                print(e)
else:
    print('I need a xml file')




print("Containers started, have a nice day!\n")