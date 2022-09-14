import boto3, json

s3_client = boto3.client("s3", region_name="us-west-1")
bucket_name = "my-bucket"


def create_bucket():
    resp = s3_client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={"LocationConstraint": "us-west-1"},
    )
    print(resp)


def list_buckets():
    resp = s3_client.list_buckets()
    print(f"Raw Response: {resp}")
    print("Buckets:")
    for bucket in resp["Buckets"]:
        print(bucket["Name"])


def upload_file():
    source_file = "test-file.txt"
    object_name = "test-file.txt"

    s3_client.upload_file(source_file, bucket_name, object_name)

    print("File uploaded")


def upload_file_as_obj():
    with open("test-file.txt", mode="rb") as file:
        resp = s3_client.upload_fileobj(file, bucket_name, "test-file.txt")
        print(resp)


def list_bucket_content():
    resp = s3_client.list_objects(Bucket=bucket_name)
    for content in resp.get("Contents", []):
        print(content["Key"], content["Size"], content["StorageClass"])


def download_file():
    s3_client.download_file(bucket_name, "test-file.txt", "test-file-from-s3.txt")
    print("File downloaded")


def download_file_as_obj():
    with open("test-file-obj-from-s3.txt", "wb") as file:
        s3_client.download_fileobj(bucket_name, "test-file.txt", file)
    print("File downloaded")


def create_presigned_url():
    resp = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": "test-file.txt"},
        ExpiresIn=300,
    )
    print(resp)


def set_bucket_policy():
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject"],
                "Principal": "*",
                "Resource": ["arn:aws:s3:::mtest-990/*"],
            }
        ],
    }
    resp = s3_client.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))
    print(resp)
    print("Policy set up")


def list_bucket_policy():
    resp = s3_client.get_bucket_policy(Bucket=bucket_name)
    print(resp["Policy"])


def delete_bucket_policy():
    resp = s3_client.delete_bucket_policy(Bucket=bucket_name)
    print(resp)


def set_cors_config():
    cors_config = {
        "CORSRules": [
            {
                "AllowedHeaders": ["Authorization"],
                "AllowedMethods": ["GET", "PUT"],
                "AllowedOrigins": ["*"],
                "ExposeHeaders": ["GET", "PUT"],
                "MaxAgeSeconds": 3000,
            }
        ]
    }
    s3_client.put_bucket_cors(Bucket=bucket_name, CORSConfiguration=cors_config)
    print("CORS Config set up")


def list_cors_config():
    resp = s3_client.get_bucket_cors(Bucket=bucket_name)
    for rule in resp["CORSRules"]:
        print(rule)


if __name__ == "__main__":
    # Uncoment method to execute it

    # create_bucket()
    # upload_file()
    # list_buckets()
    # upload_file_as_obj()
    # list_bucket_content()
    # download_file()
    # download_file_as_obj()
    # create_presigned_url()
    # set_bucket_policy()
    list_bucket_policy()
    # delete_bucket_policy()
    # set_cors_config()
    # list_cors_config()
