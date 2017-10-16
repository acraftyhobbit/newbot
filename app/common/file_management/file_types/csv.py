def open_csv_file(key, delimiter=','):
    import csv
    from common.file_management.manager import read_file
    text = read_file(key=key, open_type='rb')

    reader = list()
    if text:
        try:
            text = text.decode("utf-8")
        except Exception:
            text = text.decode('ISO-8859-1')
        reader = csv.DictReader(text.splitlines(), delimiter=delimiter)
    return reader


def store_csv_file(headers, rows, key, delimiter=',', s3=True):
    from common.file_management.manager import store_file
    from common.file_management.local import open_local_temp_file, get_local_file_path
    import csv
    output = open_local_temp_file(key, open_type='wt')
    if rows and (isinstance(rows[0], tuple) or isinstance(rows[0], list)):
        writer = csv.writer(output, delimiter=delimiter)
        writer.writerow(headers)
        for row in rows:
            writer.writerow([str(i) for i in row])
    elif rows and isinstance(rows[0], dict):
        writer = csv.DictWriter(output, fieldnames=headers, delimiter=delimiter, extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            try:
                writer.writerow({k: str(v) for k, v in row.items() if v is not None})
            except Exception as e:
                pass
    output.close()
    if s3:
        return store_file(key=key, obj=None, large=True)
    else:
        return get_local_file_path(key)
