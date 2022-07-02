# AWS application developer - Use case 1
High Availability API cross region on EC2 using ASG, ALB and Route53 using API Gateway - DynamoDB as backend database

## Download Cloud Formation Templates
### ZIP
- Open in browser https://github.com/Rising-Minerva/AWS-Application-Developer 
- Click "clone or download" green button and click Download ZIP
- Unzip the file and remember the folder where you kept the unzipped file.
- Navigate to the directory. 
OR
### GIT
- Navigate to applications directory 
- git clone https://github.com/Rising-Minerva/AWS-Application-Developer

## Review the HA API templates
- Navigate to AWS-Application-Developer/Labs/USECASE1
- Open and review
    - CFT ha-api-multi-region.yml
    - Will be executed in both EAST and WEST regions
- Application code “ha-api-multi-region.py

## Changes to the CFT
- Update the Mapping section
    - In Mappings section, change AMIIDs to AMI id of Linux AMIs of your account (Each account has different values)
        - Would look similar to ami-0a887e401f7654935
    - In Mappings section, change RisingMinervaKeyName
        - Key Name of your account created while creating a new EC2 instance
- In the UserData section, MODIFY the below LINE to point to your bucket
    - aws s3 cp "s3://risingminervacodebase-rchaturvedi/ha-api-multi-region/ha-api-multi-region.py" app.py

## Changes to the Application Code
- Update the parameter username in line 11 to YOUR NAME

## Upload CFT and application to S3
- After making all the changes indicated above, upload the CFT and application code to S3 bucket
    - s3://risingminervacodebase-YOUR FIRST NAME-YOUR LAST NAME/ha-api-multi-region/ha-api-multi-region.yml
    - s3://risingminervacodebase-YOUR FIRST NAME-YOUR LAST NAME/ha-api-multi-region/ha-api-multi-region.py

## Spin up the ALB-ASG-EC2 stack (To be done in both EAST and WEST regions)
- Login to the AWS account.
- Go to CloudFormation
- Click on Create Stack
- Select “Template is Ready”
- Select “Amazon S3 URL”. Put the value of the PATH of S3 URL similar to (get it from your S3 bucket)
    - https://risingminervacodebase-rchaturvedi.s3.amazonaws.com/lambda-api/lambda-api.yml
    - https://risingminervacodebase-YOUR FIRST NAME-YOUR LAST NAME/ha-api-multi-region/ha-api-multi-region.yml
- Click Next
- Give Stack Name as risingminerva-ha-api on the console
- Provide appropriate parameter names
    - Cross check parameters LambdaCodeS3Bucket
    - VpcId to VPC id of your account
    - Subnets to minimum subnets of your account
    - IAMRole - Your role for USECASE1 created in the IAM section

## Try hitting the DNS of the ALB from the Browser, in both regions
- GET CALL

### GET Customer id
    
        GET {{R53NAME}}/getCustomer?customerid=6

************************************************************************************************************
## NOTE: The below steps need to be performed when you have a registered domain, otherwise a RisingMinerva associate will need to show you in Company’s account
************************************************************************************************************
- Modify Route53 Template
    - CFT ha-api-multi-region-Route53.yml
    - Will be executed once as it creates ROUTE53
    - Will be executed only when ha-api-multi-region.yml is successfully executed in both EAST and WEST regions
- Once both EAST and WEST stacks are created with the above step, we need to modify ROUTE53 CFT ha-api-multi-region-Route53.yml
    - Go to line 23 - ResourceRecords
    - Modify the value to the CNAME of the ALB created in WEST
        - Similar to risingminervaalb-1390876562.us-west-2.elb.amazonaws.com
- Upload Route53 CFT to S3
    - After making all the changes indicated above, upload the CFT and application code to S3 bucket
         - s3://risingminervacodebase-YOUR FIRST NAME-YOUR LAST NAME-/ha-api-multi-region/ha-api-multi-region-Route53.yml

## Spin Up Route 53 Stack
- Login to the AWS account.
- Go to CloudFormation
- Click on Create Stack
- Select “Template is Ready”
- Select “Amazon S3 URL”. Put the value of the PATH of S3 URL similar to (get it from your S3 bucket)
    - https://risingminervacodebase-rchaturvedi.s3.amazonaws.com/lambda-api/lambda-api.yml
    - https://risingminervacodebase-YOUR FIRST NAME-YOUR LAST NAME/ha-api-multi-region/ha-api-multi-region-Route53.yml
- Click Next
- Give Stack Name as risingminerva-ha-api-R53 on the console

### IMPORTANT NOTE - Create VPC endpoints in both regions
- To invoke DynamoDB from a VPC, you need to enable VPC endpoints to DYNAMODB service
- Go to VPC
- Click on your VPC
- Go to end points
- Add an endpoint to com.amazonaws.us-east-1.dynamodb to your VPC

## API Call
- You will be calling Route53 URL similar to below (We have provided this in OUTPUTs of this template)
- Route53 URL: haapi.risingminervaadminha.com

### POST Customer id
    
        POST {{R53NAME}}/addCustomer
        Headers::[{"key":"Content-Type","value":"application/json","description":""}
        Body: 
        {
        "customer_id":6,
        "customer_name":"Rising Minerva 6",
        "customer_email":"rising.minerva6@gmail.com"
        }

### GET Customer id
    
        GET {{R53NAME}}/getCustomer?customerid=6

### DELETE Customer id
        
        POST {{R53NAME}}/deleteCustomer
        Headers::[{"key":"Content-Type","value":"application/json","description":""}, {"key":"customerid","value":"1","description":""}]
