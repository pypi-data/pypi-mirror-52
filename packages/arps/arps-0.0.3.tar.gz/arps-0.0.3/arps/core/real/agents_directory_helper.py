import logging
import http.client
from typing import List, Tuple, Dict

import simplejson as json


class AgentsDirectoryHelperError(Exception):
    '''Exception to describe a problem during the execution of a request

    '''


class AgentsDirectoryHelper:

    def __init__(self, *, address: str, port: int) -> None:
        '''
        Initialize connection to the agents directory

        Args:
        - address: url to access the agents directory
        - port: port being listened by the agents directory
        '''
        self.port = port
        self.address = 'http://{}:{}'.format(address, self.port)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.conn = http.client.HTTPConnection(address, port)

    def get(self, *, parameters: List[str]) -> Tuple[bool, Dict]:
        '''Get info about agent in agents directory
        '''
        parameters = self.format_parameters(parameters)
        return self.request(f'/get?{parameters}')

    def add(self, *, parameters: List[str]) -> Tuple[bool, Dict]:
        '''Add info about agent in agents directory
        '''
        parameters = self.format_parameters(parameters)
        return self.request(f'/add?{parameters}')

    def remove(self, *, parameters: List[str]) -> Tuple[bool, Dict]:
        '''Remove agent from agents directory
        '''
        parameters = self.format_parameters(parameters)
        return self.request(f'/remove?{parameters}')

    def list(self) -> Tuple[bool, Dict]:
        '''List registered agents
        '''
        return self.request('/list')

    def about(self) -> Tuple[bool, Dict]:
        '''Get info about agents directory
        '''
        return self.request('/about')

    def available_commands(self) -> Tuple[bool, Dict]:
        '''Get available commands in agents directory
        '''
        return self.request('/')

    def format_parameters(self, parameters: List[str]) -> str:
        return '&'.join('{}={}'.format(parameter, value) for parameter, value in parameters.items())

    def request(self, url):
        self.logger.info('Accessing {}'.format(self.address + url))
        try:
            self.conn.request('GET', url)
            request = self.conn.getresponse()
            request_content = request.read()
            self.logger.debug(f'Request response content: {request_content}')
            return json.loads(request_content.decode())
        except json.JSONDecodeError as err:
            raise AgentsDirectoryHelperError(f'Error while decoding json {err}')
        except ConnectionError as err:
            self.logger.error(err)
            self.logger.error('Raise AgentsDirectoryHelperError')
            raise AgentsDirectoryHelperError(f'Error when accessing {url}')
