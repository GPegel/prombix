# PromBix

Let Zabbix monitor Prometheus end-points by automatically start Zabbix server, Zabbix Agent, Prometheus, Grafana and a Node exporter.


When you start Prombix, hopefully everything starts fine without any errors or warnings than you have not only  a running Zabbix server with a pre-configured agent.  But also some other nice things that are not completed yet. 

**Currently in progress** -> Grafana will be installed including the Zabbix datasource and Zabbix dashboard.

And last but certainly not least, a Prometheus server will be available and the node exporter is also up and running exposing all kinds of metrics of the node that's installed on. For example, it exposes all the metrics of my macbook when I run this locally.

Within Zabbix, a template will be added later automatically, I had a nice piece of code for it but I dropped it for now.

This goes also for the auto-registration rules and auto-discovery added via the Zabbix API. 

Longs story short, see next topic ;-)

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

In the file called `start.py` you will see a bunch of Docker containers being started like zabbix-appliance, zabbix-agent and also Grafana.

So to start the containers, just type in your CLI : `python3 start.py`

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
- [x] Add Grafana server incl. dashboards. 
- [ ] Add alert to pre-configured e-mail.
- [ ] Add CI/CD for automatic deployment of templates and configuration files.
- [x] Import Zabbix templates via API call (for now postponed)
- [x] Add Prometheus /metrics end-points to Zabbix via API for demo 
- [ ] Automatically add discovery rules
- [ ] Automatically add auto-registration rules
- [x] Add Grafana dashboards by file, not how it's currently done by Prombix.
- [x] Add Prometheus datasource via API
