def get_local_file_path(filename):
    import os
    from app.settings import TEMP_FILE_PATH, BASE_DIR

    if str(filename).startswith('test/'):
        path = os.path.join(BASE_DIR, '../' + filename)
    else:
        path = os.path.join(TEMP_FILE_PATH, "/".join(str(filename).split('/')[-2:]).replace('/', '_'))
    return path


def open_local_temp_file(filename, open_type='rb', overwrite=True):
    import os
    path = get_local_file_path(filename=filename)
    if os.path.isfile(path=path) or 'w' in open_type:
        return open(path, open_type, )
    else:
        return None


def store_local_file(obj, key):
    write_type = 'wt'
    local_key = get_local_file_path(filename=key)
    if not isinstance(obj, str):
        write_type = 'wb'
    with open_local_temp_file(filename=key, open_type=write_type) as f:
        f.write(obj)
    return local_key


def delete_local_file(key):
    import os
    os.remove(get_local_file_path(filename=key))
    return True


def delete_local_folder(key):
    import os
    os.removedirs(get_local_file_path(filename=key))
    return True
