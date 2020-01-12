import docker
import time
import sys

client = docker.from_env()
toolbar_width = 40

print('Please wait while nuking the containers...')
sys.stdout.write("[%s]" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width+1))

for i in range(toolbar_width):
    time.sleep(0.1)
    for container in client.containers.list():
      container.stop()
      container.remove()
    sys.stdout.write("-")
    sys.stdout.flush()
sys.stdout.write("]\n")
print('All containers are stopped and removed')