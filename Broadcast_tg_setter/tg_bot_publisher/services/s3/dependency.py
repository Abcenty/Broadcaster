import asyncio
from contextlib import asynccontextmanager
from aiobotocore.session import get_session


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
        self.session = get_session()
        
    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client
            
    async def upload_file(
            self,
            file_path: str,
    ):
        print(file_path)
        object_name = file_path.split("/")[-1]
        try:
            async with self.get_client() as client:
                with open(file_path, "rb") as file:
                    await client.put_object(
                        Bucket=self.bucket_name,
                        Key=object_name,
                        Body=file,
                    )
        except:
            raise
        
    async def download_file(
            self,
            file_path: str,
    ):
        print(file_path)
        object_name = file_path.split("/")[-1]
        try:
            async with self.get_client() as client:
                with open(file_path, "rb") as file:
                    object = await client.get_object(
                        Bucket=self.bucket_name,
                        Key=object_name,
                    )
                    print(object['Body'])
        except:
            raise
    async def delete_file(
            self,
            file_path: str,
    ):
        print(file_path)
        object_name = file_path.split("/")[-1]
        try:
            async with self.get_client() as client:
                with open(file_path, "rb") as file:
                    object = await client.delete_object(
                        Bucket=self.bucket_name,
                        Key=object_name,
                    )
        except:
            raise
        
async def main():
    s3_client = S3Client(
        access_key="bb64986a2262411580b42c9751c7358f",
        secret_key="91bcf8738a644512b6f364181dbe7416",
        endpoint_url="https://s3.storage.selcloud.ru", 
        bucket_name="broadcaster-bucket",
    )

    # Проверка, что мы можем загрузить, скачать и удалить файл
    await s3_client.delete_file("/Users/Andre/Desktop/Проекты/PycharmProjects/Broadcaster/text.txt")


if __name__ == "__main__":
    asyncio.run(main())