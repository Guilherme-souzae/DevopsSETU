import boto3
ec2 = boto3.resource('ec2')

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
print("CREATED INSTANCES:")
for inst in new_instances:
    inst.wait_until_running()
    inst.reload()
    print(f"Instance ID: {inst.id}")
    print(f"Instance IP: {inst.public_ip_address}")
quit()
