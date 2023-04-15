# Importando Python modules
import pulumi
from pulumi_aws import s3, iam, ec2, lb


# Security Group
ec2_sg = ec2.SecurityGroup('ec2_sg',
    ingress=[
      {
        "protocol": "tcp",
        "from_port": 80,
        "to_port": 80,
        "cidr_blocks": ["0.0.0.0/0"]
      },
    ],
    egress=[
      {
        'protocol': '-1',
        'from_port': 0,
        'to_port': 0,
        'cidr_blocks': ['0.0.0.0/0']
      }
    ],
    description='access to ec2')

# EC2 instance
ec2_instance = ec2.Instance('myec2', 
    instance_type               = 't2.micro',
    vpc_security_group_ids      = [ec2_sg.id], # referencia
    ami                         = 'ami-007855ac798b5175e',
    tags={
        'Name': 'ec2_demo',
        'tool': 'pulumi'
    })


# Imprimir en pantalla
pulumi.export('ec2_sg_id', ec2_sg.id)
pulumi.export('ec2_instance_id', ec2_instance.id)
pulumi.export('ec2_instance_public_ip', ec2_instance.public_ip)
