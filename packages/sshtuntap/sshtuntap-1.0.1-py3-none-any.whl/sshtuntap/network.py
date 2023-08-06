import os
import pwd
from os import path, chown
from ipaddress import ip_address, IPv4Network

import yaml

from . import linux
from .console import ok, warning, info


USER_CONFIGURATIONFILE = '.ssh/tuntap.yml'


def gethost(name):
    user = pwd.getpwnam(name)
    configurationfilename = path.join(user.pw_dir, USER_CONFIGURATIONFILE)
    if not path.exists(configurationfilename):
        raise KeyError(name)

    with open(configurationfilename) as f:
        return yaml.load(f), configurationfilename


def getallhosts():
    # Look for all linux users using pwd module
    # filter users which has home dirs
    for i in pwd.getpwall():
        if i.pw_uid >= 1000 and not i.pw_shell.endswith('nologin'):
            configurationfile = path.join(i.pw_dir, USER_CONFIGURATIONFILE)
            if not path.exists(configurationfile):
                continue

            with open(configurationfile) as f:
                conf = yaml.load(f)

            yield i.pw_name, conf


def getallassignedaddresses():
    for u, c in getallhosts():
        yield ip_address(c['addresses']['client'])
        yield ip_address(c['addresses']['server'])


def assign(network):
    addresses = set(getallassignedaddresses())
    result = []

    # find two free addresses
    for ip in network.hosts():
        if ip in addresses:
            continue

        if len(result) >= 2:
            break

        result.append(ip)

    client, server = result
    return client, server, int(client) - int(network.network_address)


def getnetwork():
    return IPv4Network(settings.cidr)


def createinterface(host):
    index = str(host['index'])
    ifname = f'tun{index}'
    clientaddr = host['addresses']['client']
    serveraddr = host['addresses']['server']
    netmask = host['netmask']
    owner = host['remoteuser']
    lines = [f'{i}\n' for i in [
        f'allow-hotplug {ifname}',
        f'auto {ifname}',
        f'iface {ifname} inet static',
        f'  address {serveraddr}',
        f'  endpoint {clientaddr}',
        f'  netmask {netmask}',
        f'  pre-up ip tuntap add mode tun dev {ifname} user {owner} group {owner}',
    ]]

    ifacefilename = path.join('/etc/network/interfaces.d', ifname)
    with open(ifacefilename, 'w') as f:
        f.writelines(lines)

    ok(f'File {ifacefilename} has been created successfully.')
    linux.shell(f'service networking restart')
    linux.shell(f'ifup {ifname}')


def addhost(network, user):
    configurationfile = path.join(user.pw_dir, USER_CONFIGURATIONFILE)
    if path.exists(configurationfile):
        warning(f'User is already exists: {user.pw_name}')
        warning(f'Overwriting the file: {configurationfile}')

    client, server, index = assign(network)
    info(f'Assigned addresses: {client} {server}')

    userconfiguration = dict(
        remoteuser=user.pw_name,
        uid=user.pw_uid,
        gid=user.pw_gid,
        shell=user.pw_shell,
        addresses=dict(client=str(client), server=str(server)),
        netmask=str(network.netmask),
        index=index
    )

    with open(configurationfile, 'w') as f:
        yaml.dump(userconfiguration, f, default_flow_style=False)

    chown(configurationfile, user.pw_uid, user.pw_gid)
    createinterface(userconfiguration)


def deletehost(username):
    host, configurationfilename = gethost(username)
    index = str(host['index'])
    ifname = f'tun{index}'
    linux.shell(f'ifdown {ifname}')

    # remove the interfaces.d file
    ifacefilename = path.join('/etc/network/interfaces.d', ifname)
    if path.exists(ifacefilename):
        os.remove(ifacefilename)

    linux.shell(f'ip tuntap delete {ifname} mode tun')

    # remove the .ssh/tuntap.yml file
    if path.exists(configurationfilename):
        os.remove(configurationfilename)

