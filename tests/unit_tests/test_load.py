import os
import pytest
from unittest.mock import patch, MagicMock
from etl.load.load import load_to_bucket


@patch('etl.load.load.boto3.client')
def test_load_to_bucket_success(mock_boto_client):
    os.environ['AWS_ACCESS_KEY'] = 'fake_access_key'
    os.environ['AWS_SECRET_KEY'] = '1234'
    os.environ['AWS_S3_BUCKET_NAME'] = 's3bucket'
    os.environ['AWS_REGION'] = 'us-east-1'

    test_s3_client = MagicMock()
    test_s3_client.upload_file.return_value = None
    mock_boto_client.return_value = test_s3_client

    result = load_to_bucket('test_file.csv', 'test_object.csv')

    assert result is True
    test_s3_client.upload_file.assert_called_once_with(
        'test_file.csv', 's3bucket', 'test_object.csv')
