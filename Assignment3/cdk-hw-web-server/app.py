#!/usr/bin/env python3
import os

import aws_cdk as cdk
from cdk_hw_web_server.cdk_hw_network_stack import CdkHwNetworkStack
from cdk_hw_web_server.cdk_hw_web_server_stack import CdkHwWebServerStack


app = cdk.App()

# Create the Network Stack
network_stack = CdkHwNetworkStack(app, "CdkHwNetworkStack")

# Create the Web Server Stack and pass the VPC from the Network Stack
web_server_stack = CdkHwWebServerStack(app, "CdkHwWebServerStack", cdk_hw_vpc = network_stack.cdk_hw_vpc)

app.synth()
