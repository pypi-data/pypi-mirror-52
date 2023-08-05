import platform


class FakeAgentsDirectoryHelper:

    def __init__(self):
        self.registered = {}

    def get(self, *, parameters):
        if parameters['id'] not in self.registered:
            return {'message': None, 'result': 'failure'}

        return {'message':
                {'address': platform.node(),
                 'port': self.registered[parameters['id']]},
                'result': 'success'}

    def add(self, *, parameters):
        self.registered[str(parameters['id'])] = parameters['port']
        return {'message': 'agent {} added'.format(parameters['id']),
                'result': 'success'}

    def remove(self, *, parameters):
        return {'message': None, 'result': 'failure'}

    def list(self):
        return {'message': None, 'result': 'failure'}

    def about(self):
        return {'message': None, 'result': 'failure'}

    def available_commands(self):
        return {'message': None, 'result': 'failure'}
