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