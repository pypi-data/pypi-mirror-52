from .apiclasstemplate import APIClassTemplate
from .devicehapairs import DeviceHAPairs
from .physicalinterface import PhysicalInterface
import logging


class DeviceHAFailoverMAC(APIClassTemplate):
    """
    The DeviceHAFailoverMAC Object in the FMC.
    """

    PREFIX_URL = '/devicehapairs/ftddevicehapairs'
    REQUIRED_FOR_POST = ['physicalInterface', 'failoverActiveMac', 'failoverStandbyMac']
    REQUIRED_FOR_PUT = ['id']

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for DeviceHAFailoverMAC class.")
        self.parse_kwargs(**kwargs)

    def format_data(self):
        logging.debug("In format_data() for DeviceHAFailoverMAC class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'physicalInterface' in self.__dict__:
            json_data['physicalInterface'] = self.physicalInterface
        if 'failoverActiveMac' in self.__dict__:
            json_data['failoverActiveMac'] = self.failoverActiveMac
        if 'failoverStandbyMac' in self.__dict__:
            json_data['failoverStandbyMac'] = self.failoverStandbyMac
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for DeviceHAFailoverMAC class.")
        if 'ha_name' in kwargs:
            self.device_ha(ha_name=kwargs['ha_name'])
        if 'physicalInterface' in kwargs:
            self.physicalInterface = kwargs['physicalInterface']
        if 'failoverActiveMac' in kwargs:
            self.failoverActiveMac = kwargs['failoverActiveMac']
        if 'failoverStandbyMac' in kwargs:
            self.failoverStandbyMac = kwargs['failoverStandbyMac']

    def device_ha(self, ha_name):
        logging.debug("In device_ha() for DeviceHAFailoverMAC class.")
        deviceha1 = DeviceHAPairs(fmc=self.fmc, name=ha_name)
        deviceha1.get()
        if 'id' in deviceha1.__dict__:
            self.deviceha_id = deviceha1.id
            self.URL = f'{self.fmc.configuration_url}{self.PREFIX_URL}/' \
                       f'{self.deviceha_id}/failoverinterfacemacaddressconfigs'
            self.deviceha_added_to_url = True
        else:
            logging.warning(f'Device HA {ha_name} not found.  Cannot set up device for DeviceHAFailoverMAC.')

    def p_interface(self, name, device_name):
        logging.debug("In p_interface() for DeviceHAFailoverMAC class.")
        intf1 = PhysicalInterface(fmc=self.fmc)
        intf1.get(name=name, device_name=device_name)
        if 'id' in intf1.__dict__:
            self.physicalInterface = {'name': intf1.name, 'id': intf1.id, 'type': intf1.type}
        else:
            logging.warning(f'PhysicalInterface, "{name}", not found.  Cannot add to DeviceHAFailoverMAC.')

    def edit(self, name, ha_name):
        logging.debug("In edit() for DeviceHAFailoverMAC class.")
        deviceha1 = DeviceHAPairs(fmc=self.fmc, name=ha_name)
        deviceha1.get()
        obj1 = DeviceHAFailoverMAC(fmc=self.fmc)
        obj1.device_ha(ha_name=ha_name)
        failovermac_json = obj1.get()
        items = failovermac_json.get('items', [])
        found = False
        for item in items:
            if item['physicalInterface']['name'] == name:
                found = True
                self.id = item['id']
                self.name = item['physicalInterface']['name']
                self.failoverActiveMac = item['failoverActiveMac']
                self.failoverStandbyMac = item['failoverStandbyMac']
                self.deviceha_id = deviceha1.id
                self.URL = f'{self.fmc.configuration_url}{self.PREFIX_URL}/' \
                           f'{self.deviceha_id}/failoverinterfacemacaddressconfigs'
                break
        if found is False:
            logging.warning(f'PhysicalInterface, "{name}", not found.  Cannot add to DeviceHAFailoverMAC.')
