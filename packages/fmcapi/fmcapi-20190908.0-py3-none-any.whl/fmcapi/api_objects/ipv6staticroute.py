from .apiclasstemplate import APIClassTemplate
from .device import Device
from .ipaddresses import IPAddresses
from .iphost import IPHost
from .networkgroup import NetworkGroup
import logging


class IPv6StaticRoute(APIClassTemplate):
    """
    The IPv6StaticRoute Object in the FMC.
    """

    PREFIX_URL = '/devices/devicerecords'
    URL_SUFFIX = None
    REQUIRED_FOR_POST = ['interfaceName', 'selectedNetworks', 'gateway']
    REQUIRED_FOR_PUT = ['id', 'device_id']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for IPv6StaticRoute class.")
        self.type = 'IPv6StaticRoute'
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for IPv6StaticRoute class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'interfaceName' in self.__dict__:
            json_data['interfaceName'] = self.interfaceName
        if 'selectedNetworks' in self.__dict__:
            json_data['selectedNetworks'] = self.selectedNetworks
        if 'gateway' in self.__dict__:
            json_data['gateway'] = self.gateway
        if 'metricValue' in self.__dict__:
            json_data['metricValue'] = self.metricValue
        if 'isTunneled' in self.__dict__:
            json_data['isTunneled'] = self.isTunneled
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for IPv6StaticRoute class.")
        if 'device_name' in kwargs:
            self.device(device_name=kwargs['device_name'])
        if 'interfaceName' in kwargs:
            self.interfaceName = kwargs['interfaceName']
        if 'selectedNetworks' in kwargs:
            self.selectedNetworks = kwargs['selectedNetworks']
        if 'gateway' in kwargs:
            self.gateway = kwargs['gateway']
        if 'metricValue' in kwargs:
            self.metricValue = kwargs['metricValue']
        if 'isTunneled' in kwargs:
            self.isTunneled = kwargs['isTunneled']

    def device(self, device_name):
        logging.debug("In device() for IPv6StaticRoute class.")
        device1 = Device(fmc=self.fmc)
        device1.get(name=device_name)
        if 'id' in device1.__dict__:
            self.device_id = device1.id
            self.URL = f'{self.fmc.configuration_url}{self.PREFIX_URL}/{self.device_id}/routing/ipv6staticroutes'
            self.device_added_to_url = True
        else:
            logging.warning(f'Device {device_name} not found.  Cannot set up device for IPv6StaticRoute.')

    def networks(self, action, networks):
        logging.info("In networks() for IPv6StaticRoute class.")
        if action == 'add':
            # Valid objects are IPHost, IPNetwork and NetworkGroup.
            # Create a dictionary to contain all three object type.
            ipaddresses_json = IPAddresses(fmc=self.fmc).get()
            networkgroup_json = NetworkGroup(fmc=self.fmc).get()
            items = ipaddresses_json.get('items', []) + networkgroup_json.get('items', [])
            for network in networks:
                # Find the matching object name in the dictionary if it exists
                net1 = list(filter(lambda i: i['name'] == network, items))
                if len(net1) > 0:
                    if 'selectedNetworks' in self.__dict__:
                        # Check to see if network already exists
                        exists = list(filter(lambda i: i['id'] == net1[0]['id'], self.selectedNetworks))
                        if 'id' in exists:
                            logging.warning(f'Network "{network}" already exists in selectedNetworks.')
                        else:
                            self.selectedNetworks.append(
                                {"type": net1[0]['type'], "id": net1[0]['id'], "name": net1[0]['name']})
                    else:
                        self.selectedNetworks = [
                            {"type": net1[0]['type'], "id": net1[0]['id'], "name": net1[0]['name']}]
                else:
                    logging.warning(f'Network "{network}" not found.  Cannot set up device for IPv6StaticRoute.')
        elif action == 'remove':
            ipaddresses_json = IPAddresses(fmc=self.fmc).get()
            networkgroup_json = NetworkGroup(fmc=self.fmc).get()
            items = ipaddresses_json.get('items', []) + networkgroup_json.get('items', [])
            for network in networks:
                net1 = list(filter(lambda i: i['name'] == network, items))
                if len(net1) > 0:
                    if 'selectedNetworks' in self.__dict__:
                        new_net1 = list(filter(lambda i: i['id'] != net1[0]['id'], self.selectedNetworks))
                    else:
                        logging.warning("No selectedNetworks found for this Device's IPv6StaticRoute.")
                else:
                    logging.warning(f'Network "{network}" not found.  Cannot set up device for IPv6StaticRoute.')
        elif action == 'clear':
            if 'selectedNetworks' in self.__dict__:
                del self.selectedNetworks
                logging.info('All selectedNetworks removed from this IPv6StaticRoute object.')

    def gw(self, name):
        logging.info("In gw() for IPv6StaticRoute class.")
        gw1 = IPHost(fmc=self.fmc)
        gw1.get(name=name)
        if 'id' in gw1.__dict__:
            self.gateway = {
                "object": {
                    "type": gw1.type,
                    "id": gw1.id,
                    "name": gw1.name}}
        else:
            logging.warning(f'Network "{name}" not found.  Cannot set up device for IPv6StaticRoute.')
