from minio import Minio


class MinioStorage:
    def __init__(self, hostname, access_key, secret_key, secure=True):
        self.client = Minio(
            endpoint=hostname,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )

    def download(self, bucket: str, key: str, path: str):
        self.client.fget_object(bucket, key, path)

    def upload_bytes(self, bucket: str, key: str, data: bytes, content_type: str = "application/octet-stream") -> str:
        import io

        self.client.put_object(
            bucket,
            key,
            io.BytesIO(data),
            length=len(data),
            content_type=content_type
        )

        return f"https://minio.k8s.home.lehadnk.com/{bucket}/{key}"