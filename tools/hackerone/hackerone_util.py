def getQueryParams(sort: str = None, state: str = None, **kwargs):
    query = {"filter": {}}
    for key, val in kwargs.items():
        query["filter"][key] = val
    if sort is not None:
        query["sort"] = sort
    if state is not None:
        query["filter"]["state"] = state
    return encode_params(query)


def encode_params(obj, keys=()):
    if isinstance(obj, dict):
        # When you have nested dict:
        #   Ex: key[bar]=1&key[baz]=2
        params = []
        for key, value in obj.items():
            params.append(encode_params(value, keys + (key,)))
        return "&".join(params)
    elif isinstance(obj, (list, tuple)):
        # When you have multiple values for a property.
        #   Ex: key[foo][]=1&key[foo][]=2
        params = []
        for value in obj:
            params.append(encode_params(value, keys + ("",)))
        return "&".join(params)
    else:
        # This is the last level, where the data is formatted as required by the request.
        # All the upper level keys needs to be nested, equating the value.
        #   Ex: `obj` is just a value, key=1
        #   All keys but top-level keys should be in brackets, i.e,
        #       `key[foo]=1`, not `[key][foo]=1`.
        encoded_keys = ""
        for depth, key in enumerate(keys):
            # All keys but top-level keys should be in brackets, i.e.
            # `key[foo]=1`, not `[key][foo]=1`
            if depth == 0:
                encoded_keys += key
            else:
                encoded_keys += "[" + key + "]"
        return encoded_keys + "=" + obj
