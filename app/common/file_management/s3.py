from botocore.exceptions import ClientError

from app.settings import S3


def get_bucket(key):
    from app.settings import BUCKETS
    key_pieces = key.split('/')
    bucket = BUCKETS.get(key_pieces[0])
    if bucket:
        key = "/".join(key_pieces[1:])
    else:
        bucket = BUCKETS['forge']
    return bucket, key


def store_obj_on_s3(obj, key):
    bucket, key = get_bucket(key=key)
    try:
        S3.Object(bucket, key).put(Body=obj)
        success = True
    except ClientError:
        success = False
    return success


def check_file_exists_on_s3(bucket, key):
    try:
        S3.meta.client.head_object(Bucket=bucket, Key=key)
    except ClientError:
        exists = False
    else:
        exists = True
    return exists


def get_file_from_s3(key):
    data = None
    bucket, key = get_bucket(key=key)
    if check_file_exists_on_s3(bucket=bucket, key=key):
        data = S3.Object(bucket, key).get()['Body'].read()
    return data


def store_file_on_s3(key):
    from boto3.s3.transfer import S3Transfer
    from common.file_management.local import get_local_file_path, delete_local_file
    from app.settings import S3_CLIENT
    bucket, new_key = get_bucket(key=key)
    transfer = S3Transfer(S3_CLIENT)
    path = get_local_file_path(filename=key)
    transfer.upload_file(path, bucket, new_key)
    delete_local_file(key)
    return key


def delete_file_on_s3(key):
    from app.settings import S3_CLIENT

    bucket, new_key = get_bucket(key=key)
    S3_CLIENT.delete_object(Bucket=bucket, Key=new_key)
    return True


def authenticate_external_s3_client(arn, service='s3', region='us-west-1'):
    import boto3
    import time
    sts_client = boto3.client('sts')
    assumed_role = sts_client.assume_role(
        RoleArn=arn,
        RoleSessionName="AssumeRoleSession{0}".format(int(time.mktime(time.gmtime())))
    )

    credentials = assumed_role['Credentials']

    s3_client = boto3.client(
        service, region,
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )
    return s3_client
