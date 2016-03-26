"""
// JOM

:copyright: (c) 2016 by Jacopo Scrinzi.
:license: MIT, see LICENSE for more details.

"""

import os
import shutil
from config import BASE_DIR


def mkdirs(full_path_directory):
    """Checks if the directory exists and if it doesn't it creates it

    :param full_path_directory: string
    :return: void
    """
    if not os.path.exists(full_path_directory):
        os.makedirs(full_path_directory)


class OpenVPN:
    def __init__(self, server_name, profile, easyrsa):
        """

        :param server_name: string
        :param profile: app.servers.models.ServersProfiles
        :param easyrsa: app.servers.models.EasyRsa
        :return:
        """
        self.server_name = server_name
        self.profile = profile
        self.easyrsa = easyrsa
        self.server_dir = '{}/servers/{}'.format(BASE_DIR, self.server_name)
        self.easyrsa_dir = '{}/easyrsa'.format(self.server_dir)
        self.error = None
    '''
*create_server:
    - prepare folder environment [$HOME/servers, $HOME/servers/<server-name>]
    - cp easy-rsa of profile to $HOME/servers/<server-name>/easyrsa
    - create var file
    - create ca / dh / server-cert
    - create server conf
    - create server folders $HOME/servers/<server-name>/[ccd, logs, keys]

*create_client
    - create client-cert
    - create ccd if needed
    - create config
    - create tar.bz2 in keys folder

    '''

    def prepare_server_env(self):
        """ Prepare new OpenVPN server

        :return: void
        """
        mkdirs('{}/easyrsa'.format(self.server_dir))
        mkdirs('{}/ccd'.format(self.server_dir))
        mkdirs('{}/logs'.format(self.server_dir))
        shutil.copytree(self.easyrsa.easy_rsa, self.easyrsa_dir)
        vars_data = '''if [ -z "$EASYRSA_CALLER" ]; then
	echo "You appear to be sourcing an Easy-RSA 'vars' file." >&2
	echo "This is no longer necessary and is disallowed. See the section called" >&2
	echo "'How to use this file' near the top comments for more details." >&2
	return 1
fi
set_var EASYRSA_DN              "org"
set_var EASYRSA_REQ_COUNTRY	    "{country}"
set_var EASYRSA_REQ_PROVINCE	"{province}"
set_var EASYRSA_REQ_CITY	    "{city}"
set_var EASYRSA_REQ_ORG	        "{organization}"
set_var EASYRSA_REQ_EMAIL	    "{email}"
set_var EASYRSA_REQ_OU		    "{organization_unit}"
set_var EASYRSA_KEY_SIZE	    {key_size}
set_var EASYRSA_CA_EXPIRE	    {ca_expire}
set_var EASYRSA_CERT_EXPIRE	    {key_expire}
set_var EASYRSA_BATCH		    "EasyRSA"'''.format(
            country=self.easyrsa.country,
            province=self.easyrsa.province,
            city=self.easyrsa.city,
            organization=self.easyrsa.organization,
            email=self.easyrsa.email,
            organization_unit=self.easyrsa.organization_unit,
            key_size=self.easyrsa.key_size,
            ca_expire=self.easyrsa.ca_expire,
            key_expire=self.easyrsa.key_expire
        )
        with open('{}/vars'.format(self.easyrsa_dir), 'w') as vars:
            vars.write(vars_data)

    def create_server_config(self):
        """ Create config new OpenVPN server

        :return: void
        """
        config = '{}/servers/{}/{}.conf'.format(
            BASE_DIR,
            self.server_name,
            self.server_name
        )
        if os.path.isfile(config):
            raise ValueError("{} already exists.".format(config))
        server_config = '''proto {proto}
port {port}
dev {dev}
server {network}
topology subnet
persist-key
persist-tun
keepalive 10 60
verb 3

dh {dh}
ca {ca}
cert {cert}
key {key}

max-clients {max_client}

log-append {server_dir}/logs/openvpn.log
client-config-dir {server_dir}/ccd
management {mgt_host} {mgt_port}
{extra_options}'''.format(
            proto=self.profile.proto,
            port=self.profile.port,
            dev=self.profile.dev,
            network=self.profile.network,
            dh='{}/dh.pem'.format(self.server_name),
            ca='{}/ca.crt'.format(self.server_name),
            cert='{}/cert.crt'.format(self.server_name),
            key='{}/key.crt'.format(self.server_name),
            max_client=self.profile.max_client,
            server_dir=self.server_dir,
            mgt_host=self.profile.mgt_host,
            mgt_port=self.profile.mgt_port
        )
        with open('{}/{}.conf'.format(self.server_dir, self.server_name), 'w') as conf:
            conf.write(server_config)

    def create_key(self, key, cn='', param='nopass'):
        """Create OpenVpn keys

        :return:
        """
        if key is "ca":
            # create ca
            os.system('{}/easyrsa init-pki'.format(self.easyrsa_dir))
            os.system('{}/easyrsa build-ca {}'.format(self.easyrsa_dir, param))

        elif key is "dh":
            # create dh
            os.system('{}/easyrsa gen-dh'.format(self.easyrsa_dir))
        elif key is "server":
            # create server
            os.system('{}/easyrsa init-pki'.format(self.easyrsa_dir))
            os.system('{}/easyrsa build-server-full {}'.format(self.easyrsa_dir, param))
        elif key is "client":
            # create client
            os.system('{}/easyrsa init-pki'.format(self.easyrsa_dir))
            os.system('{}/easyrsa build-client-full {}'.format(self.easyrsa_dir, param))
        else:
            raise ValueError("{} is not valid key.".format(key))


    def create_server(self):
        pass