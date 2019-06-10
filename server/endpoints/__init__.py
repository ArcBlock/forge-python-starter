from server.endpoints.auth import common
from server.endpoints.auth.checkin import checkin
from server.endpoints.auth.login import login
from server.endpoints.auth.payment import payment

endpoints = [checkin, payment]

operations = ['status', 'timeout']


def add_common_operation(endpoint, operation):
    endpoint.add_url_rule(f'/{operation}', operation,
                          getattr(common, operation))


for operation in operations:
    for endpoint in endpoints:
        add_common_operation(endpoint, operation)
