import pulumi
import pulumi_aws as aws


#  VPC
vpc = aws.ec2.Vpc("exam-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_support=True,
    enable_dns_hostnames=True,
    tags={"Name": "exam-vpc"}
)
pulumi.export("vpc_id", vpc.id)

#  Public Subnet
public_subnet = aws.ec2.Subnet("public-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="ap-southeast-1a",  
    map_public_ip_on_launch=True,
    tags={"Name": "subnet-public"}
)
pulumi.export("public_subnet_id", public_subnet.id)

#  Private Subnet
private_subnet = aws.ec2.Subnet("private-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
    availability_zone="ap-southeast-1a",  
    map_public_ip_on_launch=False,
    tags={"Name": "subnet-private"}
)
pulumi.export("private_subnet_id", private_subnet.id)

# Internet Gateway
igw = aws.ec2.InternetGateway("exam-igw",
    vpc_id=vpc.id,
    tags={"Name": "exam-igw"}
)
pulumi.export("igw_id", igw.id)

# Elastic IP for NAT
eip = aws.ec2.Eip(
    "exam-nat-eip",
    tags={
        "Name": "exam-nat-eip"
    }
)
pulumi.export("eip_id", eip.id)

#  NAT Gateway (must be in Public Subnet)
nat_gw = aws.ec2.NatGateway("exam-nat-gw",
    allocation_id=eip.id,
    subnet_id=public_subnet.id,
    tags={"Name": "exam-nat-gw"}
)
pulumi.export("nat_gateway_id", nat_gw.id)

#  Public Route Table (default route -> IGW)
public_rt = aws.ec2.RouteTable("exam-public-rt",
    vpc_id=vpc.id,
    routes=[aws.ec2.RouteTableRouteArgs(
        cidr_block="0.0.0.0/0",
        gateway_id=igw.id
    )],
    tags={"Name": "exam-public-rt"}
)
pulumi.export("public_rt_id", public_rt.id)

# Associate Public Subnet with Public RT
aws.ec2.RouteTableAssociation("exam-public-rt-assoc",
    subnet_id=public_subnet.id,
    route_table_id=public_rt.id
)

# Private Route Table (default route -> NAT GW)
private_rt = aws.ec2.RouteTable("exam-private-rt",
    vpc_id=vpc.id,
    routes=[aws.ec2.RouteTableRouteArgs(
        cidr_block="0.0.0.0/0",
        nat_gateway_id=nat_gw.id
    )],
    tags={"Name": "exam-private-rt"}
)
pulumi.export("private_rt_id", private_rt.id)

# Associate Private Subnet with Private RT
aws.ec2.RouteTableAssociation("exam-private-rt-assoc",
    subnet_id=private_subnet.id,
    route_table_id=private_rt.id
)




# Security Group for Bastion
bastion_sg = aws.ec2.SecurityGroup("bastion-sg",
    vpc_id=vpc.id,
    description="Allow SSH access to Bastion",
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        protocol="tcp",
        from_port=22,
        to_port=22,
        cidr_blocks=["0.0.0.0/0"]
    )],
    egress=[aws.ec2.SecurityGroupEgressArgs(
        protocol="-1",
        from_port=0,
        to_port=0,
        cidr_blocks=["0.0.0.0/0"]
    )],
    tags={"Name": "bastion-sg"}
)
pulumi.export("bastion_sg_id", bastion_sg.id)

# User Data Script for Bastion (System Hardening)
config = pulumi.Config()
ssh_public_key = config.require("sshPublicKey")

user_data = f"""#!/bin/bash
adduser --disabled-password --gecos "" ops
mkdir -p /home/ops/.ssh
echo "{ssh_public_key}" > /home/ops/.ssh/authorized_keys
chown -R ops:ops /home/ops/.ssh
chmod 700 /home/ops/.ssh
chmod 600 /home/ops/.ssh/authorized_keys
sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/^PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl restart sshd
"""

# Bastion EC2 Instance (Key Pair Integrated)
bastion = aws.ec2.Instance("bastion",
    instance_type="t2.micro",
    ami="ami-060e277c0d4cce553",  
    subnet_id=public_subnet.id,
    vpc_security_group_ids=[bastion_sg.id],
    associate_public_ip_address=True,
    key_name="MyKeyPair",  
    user_data=user_data,
    tags={"Name": "bastion"}
)
pulumi.export("bastion_public_ip", bastion.public_ip)


app_sg = aws.ec2.SecurityGroup("app-sg",
    vpc_id=vpc.id,
    description="Allow SSH only from Bastion",
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        protocol="tcp",
        from_port=22,
        to_port=22,
        security_groups=[bastion_sg.id]
    )],
    egress=[aws.ec2.SecurityGroupEgressArgs(
        protocol="-1",
        from_port=0,
        to_port=0,
        cidr_blocks=["0.0.0.0/0"]
    )],
    tags={"Name": "app-sg"}
)

private_ec2 = aws.ec2.Instance("private-ec2",
    instance_type="t2.micro",
    ami="ami-004a7732acfcc1e2d",
    subnet_id=private_subnet.id,
    vpc_security_group_ids=[app_sg.id],
    associate_public_ip_address=False,
    key_name="MyKeyPair",
    tags={"Name": "private-ec2"}
)

pulumi.export("private_instance_id", private_ec2.id)
pulumi.export("private_instance_private_ip", private_ec2.private_ip)




