"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

import os
from app.servers.models import Servers, ServersSupervisor
from app.servers.supervisor.pumper import get
from config import config


class Monitor:
    """Monitor OVPN"""
    @staticmethod
    def retrieve():
        """Retrieve data from Servers and update DB

        :return:
        """
        for server in Servers.select():
            result = get(server.host, int(server.port))
            if result:
                ServersSupervisor.add_clients(result[1], server, result[0])
                Servers.status_update(server, 1, len(result[1]))
            else:
                Servers.status_update(server)
        ServersSupervisor.put_offline()
        return True

    @staticmethod
    def start_vpn(server_name):
        """ run bash script with start param

        :param server_name: string
        :return:
        """
        script_path = config['MAIN']['script']
        start = os.system("sudo sh {} start {} > /dev/null".format(script_path, server_name))
        if start == 0:
            return True
        return False

    @staticmethod
    def stop_vpn(server_name):
        """ run bash script with stop param

        :param server_name: string
        :return: bool
        """
        script_path = config['MAIN']['script']
        start = os.system("sudo sh {} stop {} > /dev/null".format(script_path, server_name))
        if start == 0:
            return True
        return False
