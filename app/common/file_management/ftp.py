def get_new_files_on_ftp(ftp, folder):
    from django.utils.timezone import now
    timestamp = now()
    new_files = list()
    files = list()
    ftp.retrlines("MLSD " + folder, lambda s, l=files: l.append(s))

    for file in files:
        file_attributes = convert_mlsd_to_dict(line=file, path=folder)
        if file_attributes['Type'] == 'file':
            difference = timestamp - file_attributes['Modify']
            if difference.total_seconds() < 60 * 60 * 24:
                new_files.append(file_attributes['path'])
    return new_files


def convert_mlsd_to_dict(line, path):
    from datetime import datetime
    file_attributes = dict()
    split_line = line.split(';')
    for i in split_line:
        if '=' in i and i != split_line[-1]:
            key = i.split('=')[0]
            value = i.split('=')[1]
            file_attributes[key] = value.strip()
            if key in ['Create', 'Modify']:
                file_attributes[key] = datetime.strptime(file_attributes[key].split('.')[0] + '+0000', "%Y%m%d%H%M%S%z")
        else:
            file_attributes['path'] = path + i.strip()
    return file_attributes


def login_to_sftp(host, port, username, password):
    import paramiko
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)
    ftp = paramiko.SFTPClient.from_transport(transport)
    return ftp, transport


def login_to_ftp(host, username, password):
    from ftplib import FTP
    ftp = FTP(host=host)
    ftp.set_pasv(True)
    ftp.login(user=username, passwd=password)
    return ftp


def get_file_from_ftp(file_path, ftp):
    import io
    bytes_memory = io.BytesIO()
    if ftp:
        ftp.retrbinary("RETR " + file_path, bytes_memory.write)
    return bytes_memory.getvalue()


def upload_to_ftp(ftp, key, file_path):
    with open(file_path, 'rb') as f:
        ftp.storbinary('STOR ' + key, f)
    return True
