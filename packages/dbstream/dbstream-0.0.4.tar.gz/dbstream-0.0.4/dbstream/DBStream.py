import os
from dbstream.tunnel import create_ssh_tunnel


class DBStream:

    def __init__(self, instance_name):
        self.instance_name = instance_name
        self.instance_type_prefix = ""
        self.ssh_init_port = ""
        self.ssh_tunnel = None

    def credentials(self):
        prefix = self.instance_type_prefix + "_" + self.instance_name
        if self.ssh_tunnel:
            host = self.ssh_tunnel.local_bind_host
            port = self.ssh_tunnel.local_bind_port
        else:
            host = os.environ[prefix + "_HOST"]
            port = os.environ[prefix + "_PORT"]
        return {
            'database': os.environ[prefix + "_DATABASE"],
            'user': os.environ[prefix + "_USERNAME"],
            'host': host,
            'port': port,
            'password': os.environ[prefix + "_PASSWORD"],
        }

    def create_tunnel(self):
        self.ssh_tunnel = create_ssh_tunnel(self.instance_name, self.ssh_init_port)
        return self.ssh_tunnel

    def execute_query(self, query):
        pass

    def send_data(self, data, replace=True):
        pass

    def _send(self, data, replace, batch_size=1000):
        pass
