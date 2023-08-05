from .apiclasstemplate import APIClassTemplate
import logging


class Country(APIClassTemplate):
    """
    The Country Object in the FMC.
    """

    URL_SUFFIX = '/object/countries'
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    def __init__(self, fmc, **kwargs):
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Country class.")
        self.parse_kwargs(**kwargs)
        self.type = 'Country'

    def format_data(self):
        logging.debug("In format_data() for Country class.")
        json_data = {}
        if 'id' in self.__dict__:
            json_data['id'] = self.id
        if 'name' in self.__dict__:
            json_data['name'] = self.name
        if 'iso2' in self.__dict__:
            json_data['iso2'] = self.iso2
        if 'iso3' in self.__dict__:
            json_data['iso3'] = self.iso3
        return json_data

    def parse_kwargs(self, **kwargs):
        super().parse_kwargs(**kwargs)
        logging.debug("In parse_kwargs() for Country class.")
        if 'iso2' in kwargs:
            self.iso2 = kwargs['iso2']
        if 'iso3' in kwargs:
            self.iso3 = kwargs['iso3']

    def post(self):
        logging.info('POST method for API for Country not supported.')
        pass

    def put(self):
        logging.info('PUT method for API for Country not supported.')
        pass

    def delete(self):
        logging.info('DELETE method for API for Country not supported.')
        pass
