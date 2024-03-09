import os.path
from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_iam as iam,
    App,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct

dirname = os.path.dirname(__file__)

class CdkHwWebServerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, cdk_lab_vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        InstanceRole = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        InstanceRole.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        
        # Create Security Groups
        web_server_sg = ec2.SecurityGroup(
            self, "WebServerSG",
            vpc=cdk_lab_vpc,
            allow_all_outbound=True,
        )

        rds_sg = ec2.SecurityGroup(
            self, "RDSSG",
            vpc=cdk_lab_vpc,
            allow_all_outbound=True,
        )

        web_server_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="Allow incoming HTTP traffic",
        )

        rds_sg.add_ingress_rule(
            peer=web_server_sg,
            connection=ec2.Port.tcp(3306),
            description="Allow incoming MySQL traffic from Web Servers",
        )

        # Create EC2 Instances
        for i, subnet in cdk_lab_vpc.public_subnets:
            instance = ec2.Instance(
                self, f"WebServer-{i}",
                instance_type=ec2.InstanceType("t2.micro"),
                machine_image=ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2), 
                role=InstanceRole,
                vpc=cdk_lab_vpc,
                security_group=web_server_sg,
                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            )

        # Create RDS Instance
        rds_instance = rds.DatabaseInstance(
            self, "MyRDSInstance",
            engine=rds.DatabaseInstanceEngine.mysql(version=rds.MysqlEngineVersion.VER_8_0_25),
            instance_class=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            credentials= rds.Credentials.from_generated_secret("Admin"),
            vpc=cdk_lab_vpc,
            port=3306,
            removal_policy=RemovalPolicy.DESTROY,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
            security_groups=[rds_sg],
        )
        
        # Output the RDS Endpoint
        CfnOutput(
            self, "RDSEndpoint",
            value=rds_instance.db_instance_endpoint_address,
            description="RDS Endpoint",
        )
