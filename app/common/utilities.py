def chunkify(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def generate_unique_key(*properties):
    return create_unique_hash([str(i) for i in properties])


def django_strptime(datetime_string):
    from datetime import datetime
    return datetime.strptime(datetime_string.replace("+00:00", "+0000"), "%Y-%m-%d %H:%M:%S.%f%z")


def create_unique_hash(attributes):
    import uuid
    import hashlib
    import json

    hashed = hashlib.md5()
    hashed.update(json.dumps(attributes, sort_keys=True).encode('utf-8'))
    return uuid.UUID(str(hashed.hexdigest()))
