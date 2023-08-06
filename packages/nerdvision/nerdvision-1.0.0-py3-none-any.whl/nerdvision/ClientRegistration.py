import locale
import logging
import os
import platform
import re
import socket

import nerdvision
import netifaces
import psutil
import requests
import time
from nerdvision import settings, Utils
from requests.auth import HTTPBasicAuth

our_logger = logging.getLogger("nerdvision")


class ClientRegistration(object):
    def __init__(self):
        self.start = int(round(time.time() * 1000))
        self.api_key = settings.get_setting("api_key")
        self.name = settings.get_setting("name")
        self.tags = settings.get_setting("tags")

        self.uid = Utils.generate_uid()
        self.env_str_max = settings.get_setting("env_max_str_length")
        self.env_regex = re.compile(settings.get_setting("env_regex"))
        self.license_url = settings.get_license_url()
        self.network_exclude_regex = re.compile(settings.get_setting("network_interface_regex"))

    def run_and_get_session_id(self):
        reg_doc = {
            'uid': self.uid,
            'api_key': self.api_key,
            'product': self.product_extra(),
            'instance': self.instance_extra(),
            'os': self.os_extra(),
            'language': self.language_extra(),
            'env': self.env_extra(),
            'network': self.network_extra(),
            'tags': self.tags
        }
        our_logger.debug("Sending activation to %s => %s", self.license_url, reg_doc)
        response = requests.post(self.license_url, json=reg_doc, auth=HTTPBasicAuth(self.uid, self.api_key))

        our_logger.debug("Response from activation attempt: %s => %s", response.status_code, response.text)
        if response.status_code == 200:
            json = response.json()
            response.close()
            return json['session']
        response.close()
        return None


    def network_extra(self):
        get_hostname = socket.gethostname()
        return {
            'hostname': get_hostname,
            'address': socket.gethostbyname(get_hostname),
            'interfaces': self.load_interfaces()
        }

    def load_interfaces(self):
        ifaces = []
        filtered = list(filter(lambda x: self.network_exclude_regex.match(x) is None, netifaces.interfaces()))

        for _next in filtered:
            try:
                ifaddresses = netifaces.ifaddresses(_next)
                addresses = []
                if netifaces.AF_INET in ifaddresses:
                    inet_v4 = ifaddresses[netifaces.AF_INET]
                    addresses += [{
                        'hostname': socket.gethostbyaddr(net['addr'])[0],
                        'address': net['addr']
                    } for net in inet_v4]
                if netifaces.AF_INET6 in ifaddresses:
                    inet_v6 = ifaddresses[netifaces.AF_INET6]
                    addresses += [{
                        'hostname': socket.gethostbyaddr(net['addr'])[0],
                        'address': net['addr']
                    } for net in inet_v6]
                if len(addresses) == 0:
                    continue

                mac = ifaddresses[netifaces.AF_LINK]
                ifaces.append({
                    'name': _next,
                    'mac': mac[0]['addr'],
                    'addresses': addresses
                })
            except Exception:
                if settings.is_client_reg_debug():
                    our_logger.exception("Error processing iface %s", _next)

        return ifaces

    def env_extra(self):
        env_dict = {}
        env_keys = os.environ.keys()
        for env_key in env_keys:
            if self.env_regex.match(env_key) is not None:
                continue
            val = os.environ[env_key]
            if len(val) > self.env_str_max:
                env_dict[env_key] = val[:self.env_str_max] + '...'
            else:
                env_dict[env_key] = val
        return env_dict

    @classmethod
    def language_extra(self):
        return {
            'name': platform.python_implementation(),
            'type': 'python',
            'version': platform.python_version(),
            'python_branch': platform.python_branch(),
            'python_build_name': platform.python_build()[0],
            'python_build_date': platform.python_build()[1],
            'python_compiler': platform.python_compiler(),
            'python_revision': platform.python_revision(),
        }

    def instance_extra(self):
        return {
            'start_ts': self.start,
            'name': self.name
        }

    @staticmethod
    def product_extra():
        return {
            "major_version": nerdvision.__version_major__,
            "minor_version": nerdvision.__version_minor__,
            "micro_version": nerdvision.__version_micro__,
            "path": nerdvision.__file__,
            "build": nerdvision.__props__['__Git_Commit_Id__'],
            "name": nerdvision.agent_name,
            "version": nerdvision.__version__,
            "properties": nerdvision.__props__
        }

    @staticmethod
    def os_extra():
        return {
            "timezone": ClientRegistration.run_with_catch('timezone', lambda: time.tzname[0]),
            "name": ClientRegistration.run_with_catch('os name', platform.system),
            "arch": ClientRegistration.run_with_catch('os arch', platform.machine),
            "time": int(round(time.time() * 1000)),
            "lang": ClientRegistration.run_with_catch('lang', lambda: locale.getdefaultlocale()[0][:2]),
            "locale": ClientRegistration.run_with_catch('locale', lambda: locale.getdefaultlocale()[0][-2:]),
            "version": ClientRegistration.run_with_catch('os version', platform.version),
            "start_ts": int(psutil.boot_time() * 1000)
        }

    @staticmethod
    def run_with_catch(name, _callable, default='unknown'):
        try:
            return _callable()
        except:
            our_logger.exception("Unable to load %s", name)
            return default
