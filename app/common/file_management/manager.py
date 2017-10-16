def read_file(key, open_type='rb', large=False):
    from common.file_management.s3 import get_file_from_s3
    from common.file_management.local import open_local_temp_file
    from app.settings import ENVIRONMENT

    file = None
    if ENVIRONMENT == 'production':
        if large:
            pass
        else:
            file = get_file_from_s3(key=key)
    else:
        f = open_local_temp_file(key, open_type=open_type)
        if f:
            file = f.read()
            f.close()
    return file


def store_file(key, obj=None, large=False, overwrite=True):
    from common.file_management.s3 import store_file_on_s3, store_obj_on_s3
    from common.file_management.local import store_local_file, delete_local_file
    from app.settings import ENVIRONMENT
    if overwrite or not read_file(key=key):
        local = ENVIRONMENT != 'production' or not obj or large
        if local and obj:
            store_local_file(obj=obj, key=key)
        if obj and not large and ENVIRONMENT == 'production':
            store_obj_on_s3(obj=obj, key=key)
        elif ENVIRONMENT == 'production' and local:
            store_file_on_s3(key=key)
    else:
        if not obj:
            delete_local_file(key=key)
    return key
