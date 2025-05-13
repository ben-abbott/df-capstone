import boto3

bucket = boto3.client('s3')


def load_to_bucket(file, bucket, object_name=None):
    pass
