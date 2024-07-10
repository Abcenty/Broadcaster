import boto3
from config_data.config import settings

class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
        "aws_access_key_id": access_key,
        "aws_secret_access_key": secret_key,
        "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        
        
    def get_client(self):
        return boto3.client('s3',
                        aws_access_key_id=self.config.get("aws_access_key_id"),
                        aws_secret_access_key=self.config.get("aws_secret_access_key"),
                        endpoint_url=self.config.get("endpoint_url"),
                    )
        
    def upload_file(
            self,
            file_path: str,
            file,
    ):
        print(file_path)
        object_name = file_path.split("/")[-1]
        try:
            self.get_client().put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=file,
                )
        except:
            raise
         
s3_client = S3Client(
                access_key=settings.s3_client.access_key,
                secret_key=settings.s3_client.secret_key,
                endpoint_url=settings.s3_client.endpoint_url,
                bucket_name=settings.s3_client.bucket_name,
                )      
