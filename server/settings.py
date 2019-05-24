from os import environ

MONGO_URI = environ.get(
    'MONGO_URI') or 'mongodb://127.0.0.1:27017/forge-python-starter'


# URL_PREFIX = '/api/did'

RESOURCE_METHODS = ['GET', 'POST']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'DELETE']

token = {
    'item_title': 'token',

    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST'],

    'schema': {
        'token': {
            'type': 'string',
        },
        'status': {
            'type': 'string',
        },
        'did': {
            'type': 'string',
            'unique': True,
        },
        'sessionToken': {
            'type': 'string',
        },
    }
}

DOMAIN = {'people': {}}
