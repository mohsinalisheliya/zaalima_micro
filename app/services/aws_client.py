import boto3
from app.core.config import settings

def get_s3_client():
    # We will configure credentials on Day 3
    return boto3.client('s3')

def generate_presigned_url(object_name: str):
    s3_client = get_s3_client()
    try:
        response = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': settings.AWS_BUCKET_NAME, 'Key': object_name},
            ExpiresIn=settings.PRESIGNED_URL_EXPIRE_SECONDS
        )
        return response
    except Exception as e:
        print(f"Error generating url: {e}")
        return None
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )
