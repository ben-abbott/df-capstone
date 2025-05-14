import boto3
import os


def load_to_bucket(file, object_name):
    # AWS_ACCESS_KEY = 'AKIAYQE7QM5IAUVFYXLF'
    # AWS_SECRET_KEY = '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'
    # AWS_S3_BUCKET_NAME = 'df-capstone-clean-data'
    # AWS_REGION = 'eu-west-2'

    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")
    AWS_REGION = os.getenv("AWS_REGION")

    s3_client = boto3.client(
        service_name='s3',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    try:
        res = s3_client.upload_file(file, AWS_S3_BUCKET_NAME, object_name)
        print(f'upload file response: {res}')
    except Exception as e:
        print(f'error when uploading to s3: {e}')
        return False
    return True
