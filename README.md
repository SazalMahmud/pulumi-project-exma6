 # AWS Hands-On Exam – Pulumi Project

This repository contains the full Pulumi project for the AWS Hands-On Exam.  
It implements a secure VPC, public and private EC2 instances, MySQL installation, and end-to-end connectivity validation using **Pulumi (Python)**.

---

# Project Overview

This project covers the following tasks:

1. **Secure VPC**  
   - Create a VPC with CIDR `10.0.0.0/16`  
   - Public subnet: `10.0.1.0/24`  
   - Private subnet: `10.0.2.0/24`  
   - Internet Gateway (IGW) attached  
   - NAT Gateway in public subnet  
   - Public & Private Route Tables with proper routing  

2. **Bastion Host in Public Subnet**  
   - EC2 instance with public IPv4  
   - Security Group allowing inbound SSH from your public IP  
   - System hardening: non-root user `ops`, SSH key injected, root login disabled  

3. **Private EC2 Instance**  
   - EC2 in private subnet without public IP  
   - Security Group allows SSH only from Bastion SG  

4. **Install & Manage MySQL**  
   - MySQL installed via User Data  
   - Listen on `127.0.0.1` and private IP  
   - Database `appdb` and user `appuser` with password  
   - systemd ensures MySQL auto-start and survives reboot  

5. **End-to-End Connectivity Validation**  
   - SSH from bastion → private instance  
   - Private instance → Internet via NAT (`curl https://aws.amazon.com`)  
   - Bastion → MySQL on private instance (`SELECT 1;`)  

6. **Clean Infrastructure Teardown**  
   - `pulumi destroy` cleans all resources  
   - No orphaned resources remain  

---

##  Prerequisites

- AWS account with permissions to create VPC, EC2, S3, and related resources  
- AWS CLI configured with credentials  
- Python 3.6+  
- Pulumi CLI installed and logged in  


 ## Getting Started

 1. Generate a new project from this template:
    ```bash
    pulumi new aws-python
    ```
 2. Follow the prompts to set your project name and AWS region (default: `ap-southeast-1`).
 3. Change into your project directory:
    ```bash
    cd <project-name>
    ```
 4. Preview the planned changes:
    ```bash
    pulumi preview
    ```
 5. Deploy the stack:
    ```bash
    pulumi up
    ```
 6. Tear down when finished:
    ```bash
    pulumi destroy
    ```

This includes:

VPC ID

Subnet IDs

Bastion public IP

Private EC2 ID and private IP

Evidence / Screenshots: 

 Attached Module 6-7 Project Submissions.docx



 ## Project Layout

 After running `pulumi new`, your directory will look like:
 ```
 ├── __main__.py         # Entry point of the Pulumi program
 ├── Pulumi.yaml         # Project metadata and template configuration
 ├── requirements.txt    # Python dependencies
 └── Pulumi.<stack>.yaml # Stack-specific configuration (e.g., Pulumi.dev.yaml)
 └── Module 6-7 Project Submissions.docx
 ```

 ## Configuration

 This template defines the following config value:

 - `aws:region` (string)
   The AWS region to deploy resources into.
   Default: `us-east-1`

 View or update configuration with:
 ```bash
 pulumi config get aws:region
 pulumi config set aws:region ap-southeast-1

 ```

 ## Outputs

 Once deployed, the stack exports:

 - `bucket_name` — the ID of the created S3 bucket.

 Retrieve outputs with:
 ```bash
 pulumi stack output bucket_name
 ```

 ## Next Steps

 - Customize `__main__.py` to add or configure additional resources.
 - Explore the Pulumi AWS SDK: https://www.pulumi.com/registry/packages/aws/
 - Break your infrastructure into modules for better organization.
 - Integrate into CI/CD pipelines for automated deployments.

 ## Help and Community

 If you have questions or need assistance:
 - Pulumi Documentation: https://www.pulumi.com/docs/
 - Community Slack: https://slack.pulumi.com/
 - GitHub Issues: https://github.com/pulumi/pulumi/issues

 Contributions and feedback are always welcome!
