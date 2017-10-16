def deserialize_file_to_model(key):
    from django.core import serializers
    from common.file_management.manager import read_file
    data = list()
    file = read_file(key=key, open_type='rt')
    if file:
        for i in serializers.deserialize('json', file):
            data.append(i.object)
    return data


def serialize_model_to_file(model, key):
    from django.core import serializers
    from common.file_management.manager import store_file
    data = serializers.serialize('json', model)
    store_file(obj=data, key=key)
    return key
