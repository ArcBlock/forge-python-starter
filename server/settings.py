from os import environ

MONGO_URI = environ.get(
    'MONGO_URI') or 'mongodb://127.0.0.1:27017/forge-python-starter'
# Let's just use the local mongod instance. Edit as needed.


RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

token = {
    'item_title': 'token',

    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST'],

    'schema': {
        'did': {
            'type': 'string',
            'unique': True,
        }
    }
}

DOMAIN = {'people': {}, 'token':token}
