# PromBix

Let Zabbix monitor Prometheus end-points

## This project is still a 'Work in Progress'

Feel free to fork, clone and/or contribute to this repo.

## Presentation Slides

I've uploaded the presentation slides that I've used at the Zabbix Benelux Conference 2020.
See the 'slides' folder.

## What you need:

1. docker installed
2. python3 installed and working. Current version I'm using is **3.6.1** 
3. if you miss some modules, please run `pip3 install -r requirements.txt` to install all necesarry modules.

## How to set this up:

In the file called `start.py` you will see a bunch of Docker containers being started like zabbix-server, mysql and also zabbix-agent.

So to start MySQL, Zabbix Server, Zabbix Server Front-End, Zabbix Agent, ~~Prometheus~~ and Grafana just type in your CLI : `python3 start.py`

To stop all containers you could use the `python3 stop_all.py` script but be aware, running this script wil stop and remove ALL of your running containers. Even the ones that weren't started by this project.

## Access Zabbix from Grafana

1. check if Zabbix plugin is enabled
2. add http://localhost/api_jsonrpc.php as HTTP URL in Grafana datasource
3. Have fun creating dashboards

### To-do list (subject to change)

- [x] For some reason the Zabbix server does not start so 'Go Fix'.
- [x] Add Prometheus server + end-point running node-exporter https://github.com/prometheus/node_exporter
- [x] Add Grafana server.
- [x] Add Grafana server incl. Zabbix datasources.
- [ ] Add Grafana server incl. dashboards.
- [ ] Add alert to pre-configured e-mail.
- [ ] Add CI/CD for automatic deployment of templates and configuration files.
- [x] Import Zabbix templates via API call
- [ ] Add Prometheus /metrics end-points to Zabbix via API for demo 
- [ ] Automatically add discovery rules
- [ ] Automatically add auto-registration rules
