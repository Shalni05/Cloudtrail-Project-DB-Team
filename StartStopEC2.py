import boto3

# specify AWS keys
aws_access_key_id = <AWS ACCESS KEY>
aws_secret_access_key = <AWS SECRET KEY>
region = "us-east-1"
instance_ids = ["<EC2 Instance Id>"]

def processInstance(action = "check_all"):
    if action == "check_all":
        #Create connection with ec2
        ec2 = boto3.resource('ec2',region_name = region, aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)

        # Check what instances are running
        print("Checking for running instances...")
        
        try:
            running_instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        except Exception as e1:
            error1 = "Error1: %s" % str(e1)
            print(error1)
            return
        else:
            for instance in running_instances:
                print(instance.id, instance.instance_type)
                
    elif action == "start" or action == "stop":

        #Create connection with ec2
        ec2 = boto3.client('ec2', region_name = region, aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)
        
        # Dry run first to see if the instance is there
        try:
            if action == "start":
                ec2.start_instances(InstanceIds=instance_ids, DryRun = True)
            else:
                ec2.stop_instances(InstanceIds=instance_ids, DryRun = True)
        except Exception as e2:
            if 'DryRunOperation' not in str(e2):
                error2 = "Error2: %s" % str(e2)
                print(error2)
                return
    
        # Dry run succeeded, run start_instances without dryrun
        if action == "start":
            print("Starting the instance...")
        else:
            print("Stopping the instance...")
        
        try:
            if action == "start":
                response = ec2.start_instances(InstanceIds=instance_ids, DryRun=False)
            else:
                response = ec2.stop_instances(InstanceIds=instance_ids, DryRun=False)
            
            print(response)
        except Exception as e3:
            error3 = "Error1: %s" % str(e3)
            print(error3)
            return
        
    elif action == "status":

        #Create connection with ec2
        ec2 = boto3.resource('ec2',region_name = region, aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)
        
        # Dry run first to see if the instance is there
        try:
            status = ec2.meta.client.describe_instance_status()['InstanceStatuses']
        except Exception as e4:
            error4 = "Error1: %s" % str(e4)
            print(error4)
            return
        else:
            print(status)
            
    else:
        print("Usage: python aws.py {start|stop|check_all|status}\n")
        
def main():
    action = "status"
    processInstance(action)


        
