import boto3

def get_s3_client():
    # We will configure credentials on Day 3
    return boto3.client('s3')