from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)

minioClient = Minio('localhost:9000',
                  access_key='accessaccess',
                  secret_key='secretsecret',
                  secure=False)

def gallery_put(file_name, file_data, file_length):
    try:
        minioClient.make_bucket('gallery', location="us-east-1")
    except BucketAlreadyOwnedByYou as err:
        pass
    except BucketAlreadyExists as err:
        pass
    except ResponseError as err:
        raise
    finally:
        try:
            minioClient.put_object('gallery', file_name, file_data, file_length)
        except ResponseError as err:
            raise