import boto3
import instrumentation
# from pprint import pprint

## boto3 list buckets client method
if __name__ == "__main__":
    s3 = boto3.client("s3")
    s3.region = "us-east-2"
    response = s3.list_buckets()

    print("Response: ", response)
