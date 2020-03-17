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

When everything is up & running you are able to open Zabbix at `0.0.0.0:80` in your web browser while using the default Zabbix credentials (Admin/zabbix) and at port 3000 you can find Grafana.
At port 9090 there's a Prometheus instance running.

To stop all containers you could use the `python3 stop_all.py` script but be aware, running this script wil stop and remove ALL of your running containers. Even the ones that weren't started by this project. The stop script is also a `work in progress` 

## Access Zabbix from Grafana

1. Visit `0.0.0.0:3000` in your browser and sign in with default Grafana credentials (admin/admin)
2. Currently there are 2 dashboards available. These dashboards are being provisioned while putting `.json` files into the `\grafana_config\provisioning\dashboards\` folder
3. If you need more dashboards, create them or just download a json file from the Grafana website (https://grafana.com/grafana/dashboards) and put that into the above mentioned folder. Please note, using and ID to get access to a dashboard does not save the dashboard. So you could use an ID to test if things are working, alter the dashboard, when needed, and than export the JSON file and put that in to the above mentioned folder. The next time you will start this script the dashboards will be added automatically.

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
- [x] Automatically add discovery rules
- [ ] Automatically add auto-registration rules
- [x] Add Grafana dashboards by file, not how it's currently done by Prombix.
- [x] Add Prometheus datasource via API
- [ ] Find a way to reload config in running container (https://www.consul.io)
- [ ] Add options to restart containers when needed

