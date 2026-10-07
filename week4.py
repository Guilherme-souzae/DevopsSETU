import boto3
import uuid

ec2 = boto3.resource('ec2')
s3 = boto3.resource("s3")

# WAITER PART, EC2 Exercise
bashScript = """#!/bin/bash
sudo yum install httpd -y
sudo systemctl enable httpd
sudo systemctl start httpd"""

new_instances = ec2.create_instances(
    ImageId='ami-0fef201115eefe936',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.nano',
    UserData=bashScript,
    KeyName="linukis",
    SecurityGroupIds=["sg-0794f9045eb7197f9"],
    TagSpecifications=[{'ResourceType': 'instance','Tags': [{'Key': 'Name','Value': 'HTTP_WS'}]}]
)
print("INSTANCE CREATED")

inst = new_instances[0]

inst.wait_until_running()
inst.reload()
print("INSTANCE RUNNING")

# BUCKET SITE PART, S3 Exercise

bucket_name = f"website-bucket-{uuid.uuid4().hex[:12]}"

s3.create_bucket(Bucket=bucket_name)
bucket_website = s3.BucketWebsite(bucket_name)

website_configuration = {'ErrorDocument': {'Key': 'error.html'},'IndexDocument': {'Suffix': 'index.html'},}
response = bucket_website.put(WebsiteConfiguration=website_configuration)

print(f"{bucket_name} Upload an index.html file to test it works!")

quit()
