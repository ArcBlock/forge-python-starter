from server.endpoints import common
from server.endpoints.login import login
from server.endpoints.checkin import checkin

endpoints = [login,checkin]

operations = ['status', 'timeout']


def add_common_operation(endpoint, operation):
    endpoint.add_url_rule(f'/{operation}', operation,
                          getattr(common, operation))


for operation in operations:
    for endpoint in endpoints:
        add_common_operation(endpoint, operation)

