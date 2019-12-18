# PromBix
Let Zabbix monitor Prometheus end-points

## This project is still a 'Work in Progress'
Feel free to fork, clone and/or contribute to this repo.

## What you need:
1. docker installed
2. python3 installed and working
3. if you miss some modules, please run `pip3 install -r requirements.txt` to install all necesarry modules.

## How to set this up:
In the file called `start.py` you will see a bunch of Docker containers being started like zabbix-server, mysql and also zabbix-agent.

So to start MySQL, Zabbix Server, Zabbix Server Front-End, Zabbix Agent, ~~Prometheus~~ and ~~Grafana~~ just type in your CLI : `python3 start.py`

To stop all containers you could use the `python3 stop_all.py` script but be aware, running this script wil STOP all of your running containers. Even the ones that weren't started by this project.