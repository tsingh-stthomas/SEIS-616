import os.path

from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    CfnOutput
    # aws_sqs as sqs,
    )
from constructs import Construct

class CdkHwNetworkStack(Stack):
                        
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        @property
        def vpc(self):
            return self.cdk_lab_vpc

        # Create a VPC. CDK by default creates and attaches internet gateway for VPC
        cdk_lab_vpc = ec2.Vpc(self, "MyVPC", 
                        max_azs = 2,
                        subnet_configuration=[
                            ec2.SubnetConfiguration(
                                name="PublicSubnet1",
                                subnet_type=ec2.SubnetType.PUBLIC,
                            ),
                            ec2.SubnetConfiguration(
                                name="PrivateSubnet1",
                                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                            ),
                            ec2.SubnetConfiguration(
                                name="PublicSubnet2",
                                subnet_type=ec2.SubnetType.PUBLIC,
                            ),
                            ec2.SubnetConfiguration(
                                name="PrivateSubnet2",
                                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                            ),
                        ],
                    )
        
        # Output the VPC ID
        CfnOutput(
            self, "VpcId",
            value = cdk_lab_vpc.vpc_id,
            description="VPC ID",
        )