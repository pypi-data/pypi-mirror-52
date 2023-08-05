import platform

from typing import Dict, Any, Tuple

from arps.core.agent_id_manager import AgentID
from arps.core.communication_layer import (CommunicationLayer,
                                           CommunicableEntity)
from arps.core.real.agents_directory_helper import AgentsDirectoryHelperError


class RegistrationError(Exception):
    '''This exception is raised when a failure occur during the entity registration

    '''


class RealCommunicationLayer(CommunicationLayer):

    def __init__(self, port: int, agents_directory_helper):
        '''Initializes the communication layer

        Args:
        - port: port to list the requisitions
        - agents_directory_helper: helper with means to access the
        agents directory service

        '''

        self.port = port
        self.agents_directory_helper = agents_directory_helper

        # The clients are dependent on the implementation
        self.clients: Dict[Any, Any] = {}

        super().__init__()

    def register(self, entity: CommunicableEntity) -> None:
        '''Register the agent in the network to be discoverable

        Args:
        - entity: instance of the discoverable entity
        '''

        self.receive = entity.receive
        parameters = {'id': entity.identifier,
                      'address': platform.node(),
                      'port': self.port}

        try:
            result = self.agents_directory_helper.add(parameters=parameters)
        except AgentsDirectoryHelperError as err:
            raise RegistrationError(err)

        if result['result'] == 'failure':
            raise RegistrationError(result['message'])

        assert result['message'] == 'agent {} added'.format(entity.identifier), result['message']

    def unregister(self, entity_identifier: AgentID) -> None:
        '''Remove the agent from the network

        Args:
        - agent_dst: AgentID of the agent to removed from the network
        '''
        self.agents_directory_helper.remove(parameters={'id': entity_identifier})

    def agent_endpoint(self, agent_dst: AgentID) -> Tuple[str, str]:
        '''Finds the agent address and port based on its ID

        Args:
        - agent_dst: AgentID of the agent to be discovered

        Raises:
        - AgentsDirectoryHelperError: when the discovery service is not available
        - ValueError: when the discovery service don't find the agent

        Returns:
        - a tuple containing address and port of the agent, respectively

        '''
        result = self.agents_directory_helper.get(parameters={'id': str(agent_dst)})

        if result['result'] == 'failure':
            self.logger.warning(f'Agent provider {agent_dst} not available')
            raise ValueError(f'Agent provider {agent_dst} not available')

        server_agent = result['message']

        address = server_agent['address']
        port = server_agent['port']

        return address, port
