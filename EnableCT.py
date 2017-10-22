import boto3
from botocore.exceptions import ClientError
import random
import json

aws_access_key_id = <access_key_id>
aws_secret_access_key = <secret_access_key>
Region_Name = 'us-east-2'


def enablecloudtrail(AccountId):

	session = boto3.Session(region_name=Region_Name,aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)

	# Creating an S3 bucket
	
	try:

		s3 = session.client('s3')
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
			
    
	except ClientError as e:
	
		print(e.response['Error']['Message'])
    

	

	# Creating a new Trail

	CloudTrailName = 'CloudTrail-Test1'
	ct = session.client('cloudtrail')
	
	try:

		res = ct.create_trail(
			Name=CloudTrailName,
			S3BucketName=S3Bucket,
			S3KeyPrefix='CT',
			IncludeGlobalServiceEvents=True,
			IsMultiRegionTrail=True,
			EnableLogFileValidation=False
			)
		# Enable logging on the new trail
		CloudTrailARN = res['TrailARN']
		ct.start_logging(Name = CloudTrailARN)

		
	except ClientError as e:

		print(e.response['Error']['Message'])
		
	else:

	    
		print("Trail created\nName:%s\nS3 bucket:%s\nARN:%s" %(CloudTrailName, S3Bucket, CloudTrailARN))

	
def main():
	enablecloudtrail(<Account_ID>) #Account ID of the root user
	

if __name__ == "__main__":
	main()