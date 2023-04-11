"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3, iam, ec2, lb

stack_name = pulumi.get_stack()
# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket(stack_name + '-my-bucket')

ec2_sg = ec2.SecurityGroup(stack_name + '_ec2_sg',
    ingress=[
        { "protocol": "tcp", "from_port": 80, "to_port": 80, "cidr_blocks": ["0.0.0.0/0"] },
        { "protocol": "tcp", "from_port": 443, "to_port": 443, "cidr_blocks": ["0.0.0.0/0"] },
    ],
    egress=[
        { 'protocol': '-1', 'from_port': 0, 'to_port': 0, 'cidr_blocks': ['0.0.0.0/0'] }
    ],
    description='access to ec2')
ami_id='ami-007855ac798b5175e'

ec2_instance = ec2.Instance(stack_name + '_myec2', 
    instance_type='t2.micro',
    vpc_security_group_ids=[ec2_sg.id],
    ami=ami_id,
    tags={
        'Name': stack_name + '_ec2_instance',
        'env': stack_name,
        'tool': 'pulumi'
    })


# Export the name of the bucket
pulumi.export('ec2_sg_id', ec2_sg.id)
pulumi.export('ec2_instance_id', ec2_instance.id)
pulumi.export('ec2_instance_public_ip', ec2_instance.public_ip)

pulumi.export('bucket_name', bucket.id)
