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

def check_file_exists(object_name: str) -> bool:
    s3 = get_s3_client()
    try:
        s3.head_object(Bucket=settings.AWS_BUCKET_NAME, Key=object_name)
        return True
    except Exception:
        return False

def download_file_from_s3(object_name: str, local_download_path: str) -> bool:
    s3 = get_s3_client()
    try:
        s3.download_file(settings.AWS_BUCKET_NAME, object_name, local_download_path)
        return True
    except Exception as e:
        print(f"S3 Download Error: {e}")
        return False

def upload_file_to_s3(local_file_path: str, object_name: str) -> bool:
    s3 = get_s3_client()
    try:
        s3.upload_file(local_file_path, settings.AWS_BUCKET_NAME, object_name)
        return True
    except Exception as e:
        print(f"S3 Upload Error: {e}")
        return False