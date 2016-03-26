"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

import socket


def ovpn_status(host, port, passwd=None):
    """Get open vpn status and clients connected

    :param host: string
    :param port: int
    :return: dict
    """
    host = host
    port = port
    data = ''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except socket.error:
        return False
    socket_data = sock.recv(256)
    if passwd and socket_data == b'ENTER PASSWORD:':
        sock.send('{}\n'.format(passwd).encode())
        socket_data = sock.recv(256)
        if socket_data == b'ENTER PASSWORD:':
            return False
    sock.send('status\n'.encode())
    while True:
        socket_data = sock.recv(1024)
        socket_data = socket_data.decode()
        data += socket_data
        if data.endswith("\nEND\r\n"):
            break
    sock.send('quit\n'.encode())
    sock.close()
    return list(filter(None, data.split('\r\n')))


def clean_ovpn_data(ovpn_data):
    """Clean data retrieved from OpenVpn

    :param ovpn_data: list
    :return: tuple
    """
    to_remove = [
        'OpenVPN CLIENT LIST',
        'Common Name,Real Address,Bytes Received,Bytes Sent,Connected Since',
        'Virtual Address,Common Name,Real Address,Last Ref',
        'GLOBAL STATS',
        'END'
    ]
    for item in to_remove:
        if item in ovpn_data:
            ovpn_data.remove(item)
    if 'Max bcast/mcast queue length' in ovpn_data[-1]:
        ovpn_data.pop(-1)

    update_time = ovpn_data.pop(0).replace('Updated,', '')
    # TODO Check that entry Undef is not present and if is block IP
    divider = ovpn_data.index('ROUTING TABLE')
    clients = ovpn_data[0:divider]
    divider += 1
    routes = ovpn_data[divider:]
    merged_data = {}

    for row in clients:
        line = row.split(',')
        merged_data[line[0]] = {
            'public_ip': line[1].split(':')[0],
            'byte_received': line[2],
            'byte_sent': line[3],
            'connected_since': line[4]
        }

    for row in routes:
        line = row.split(',')
        public_ip_route = line[2].split(':')[0]
        if line[1] in merged_data.keys() and type(merged_data[line[1]]) is dict:
            public_ip_client = merged_data[line[1]]['public_ip']
            if public_ip_client != public_ip_route:
                merged_data[line[1]]['public_ip'] = (
                    "ERR: Public IP missmatch " +
                    "[public_ip_route: {}, public_ip_client: {}]".format(
                        public_ip_route,
                        public_ip_client
                    ))
            merged_data[line[1]]['ovpn_ip'] = line[0]
            merged_data[line[1]]['route_update'] = line[3]
        else:
            merged_data[line[1]] = {
                'public_ip': public_ip_route,
                'ovpn_ip': line[0],
                'last_ref': line[3],
            }

    return update_time, merged_data


def get(host, port):
    """ Get data from ovpn

    :param host: string
    :param port: int
    :return: mixed(dict/bool)
    """
    data = ovpn_status(host, port)
    if not data:
        return False
    return clean_ovpn_data(data)
