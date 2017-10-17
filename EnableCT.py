import boto3
import random
import json


AccountId = '947071601142'

# Creating an S3 bucket

s3 = boto3.client('s3')
S3Bucket = 'cloudtrail-' + str(random.randint(11111,99999))
s3.create_bucket(Bucket=S3Bucket, CreateBucketConfiguration={'LocationConstraint': 'us-west-2'}, )


# Create the bucket policy

bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AWSCloudTrailAclCheck20150319",
            "Effect": "Allow",
            "Principal": {"Service": "cloudtrail.amazonaws.com"},
            "Action": "s3:GetBucketAcl",
            "Resource": "arn:aws:s3:::%s" % S3Bucket
        },
        {
            "Sid": "AWSCloudTrailWrite20150319",
            "Effect": "Allow",
            "Principal": {"Service": "cloudtrail.amazonaws.com"},
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::%s/CT/AWSLogs/%s/*" % (S3Bucket, AccountId),
            "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
        }
    ]
}



# Convert the policy to a JSON string
bucket_policy = json.dumps(bucket_policy)

# Set the new policy on the given bucket
s3.put_bucket_policy(Bucket=S3Bucket, Policy=bucket_policy)

# Creating a new Trail

CloudTrailName = 'CloudTrail-TestBoto'
ct = boto3.client('cloudtrail')

res = ct.create_trail(
    Name=CloudTrailName,
    S3BucketName=S3Bucket,
	S3KeyPrefix='CT',
    IncludeGlobalServiceEvents=True,
    IsMultiRegionTrail=True,
    EnableLogFileValidation=False,

)

# Enable logging on the new trail
CloudTrailARN = res['TrailARN']
ct.start_logging(Name = CloudTrailARN)

print("Trail %s created with S3 bucket %s and ARN %s" %(CloudTrailName, S3Bucket, CloudTrailARN))