from cornice import Service
from colander import MappingSchema, SchemaNode, String
from pyramid.httpexceptions import HTTPAccepted

from addonreg.tasks import record_new_hash

addon = Service(name='addon', path='/addon')
addon_hash = Service(name='hash', path='/hash')


class AddonSchema(MappingSchema):
    id = SchemaNode(String(), location='body', type='str')
    sha256 = SchemaNode(String(), location='body', type='str')


@addon.post(schema=AddonSchema)
def get_addon(request):
    """Checks if an addon with the given id and hash had been registered.

    The parameters should be passed in the body of the request::

        {'id': 'addonid@example.com',
         'sha256': 'the hash of the addon, to check'}

    The service will return the same keys, in addition with a new one named
    'registered', which will be set to True of False, depending if the addon
    was found registered or not.

    """
    addon_id = request.validated['id']
    sha256 = request.validated['sha256']
    response = {'id': addon_id, 'sha256': sha256}

    registered = request.backend.hash_exists(addon_id, sha256)
    response['registered'] = registered
    return response


@addon_hash.post(schema=AddonSchema)
def add_addon_hash(request):
    """Registers a new hash for a given addon.

    This call is async, meaning that it will be queued to avoid disturbing too
    much the other endpoints which are more critical.

    The parameters should be passed in the body of the request::

        {'id': 'addonid@example.com',
         'sha256': 'the hash of the addon, to check'}

    The server should answer with a 202 Accepted HTTP status code.
    """
    record_new_hash.delay(request.validated['id'], request.validated['sha256'])
    return HTTPAccepted()
