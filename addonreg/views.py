from cornice import Service
from colander import MappingSchema, SchemaNode, String

addon = Service(name='addon', path='/addon')
addon_hash = Service(name='hash', path='/hash')


class AddonSchema(MappingSchema):
    id = SchemaNode(String(), location='body', type='str')
    sha256 = SchemaNode(String(), location='body', type='str')


@addon.post(schema=AddonSchema)
def get_addon(request):
    """Checks that an addon with the given addon-id and hash exists."""
    addon_id = request.validated['id']
    sha256 = request.validated['sha256']
    response = {'id': addon_id, 'sha256': sha256}

    registered = request.backend.hash_exists(addon_id, sha256)
    response['registered'] = registered
    return response
