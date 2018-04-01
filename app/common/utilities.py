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


def get_file_url(file):
    from app.settings import BUCKETS
    if file.downloaded:
        key = '{0}.jpg'.format(str(file.id).replace('-', '/'))
        bucket = BUCKETS['default']
        return 'https://s3.amazonaws.com/{0}/{1}'.format(bucket, key)
    else:
        return file.url


def store_obj_on_s3(obj, key):
    from app.settings import S3, TASK_LOGGER, BUCKETS
    from botocore.exceptions import ClientError
    try:
        S3.Object(BUCKETS['default'], key).put(Body=obj)
        success = True
    except ClientError:
        TASK_LOGGER.error('file upload failed')
        success = False
    return success
