import boto3
import instrumentation
from time import sleep
# from pprint import pprint

# boto3 listBuckets client method
if __name__ == "__main__":
    s3 = boto3.client("s3")
    s3.region = "us-east-2"
    response = s3.list_buckets()

    print("Response: ", response)

# # DynamoDB listTables client method
# if __name__ == "__main__":
#     client = boto3.client("dynamodb")
#     client.region = "us-east-2"

#     for i in range(20):
#         response = client.list_tables()
#         sleep(1)

#         print("Response: ", response)