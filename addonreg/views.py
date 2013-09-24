from cornice import Service

addon = Service(name='addon', path='/addon/{addon-id}/{hash}')


@addon.get()
def get_addon(request):
    """Checks that an addon with the given addon-id and hash exists."""
    addon_id = request.matchdict['addon-id']
    hash_ = request.matchdict['hash']

    response = {'addon-id': addon_id, 'sha256': hash_}

    registered = request.backend.hash_exists(addon_id, hash_)
    response['registered'] = registered
    return response
