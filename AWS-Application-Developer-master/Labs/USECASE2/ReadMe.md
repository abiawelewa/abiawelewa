# AWS application developer - Use case 2
Lambda API using API Gateway - DynamoDB as backend database

## Download Cloud Formation Templates
    - ZIP
        - Open in browser https://github.com/Rising-Minerva/AWS-Application-Developer 
        - Click "clone or download" green button and click Download ZIP
        - Unzip the file and remember the folder where you kept the unzipped file.
        - Navigate to the directory. 
      OR
    - GIT
        - Navigate to applications directory 
        - git clone https://github.com/Rising-Minerva/AWS-Application-Developer 

## Review the lambda file splitter template.
- Navigate to AWS-Application-Developer/Labs/USECASE2
- Open and review the template "lambda-api.yml" and application code “lambda-api.py”

## Bundle application, needed for LAMBDA
  - Windows: 
      - Zip the “lambda-api.py” application code, resulting in “lambda-api.zip”
  - MAC from Terminal command line
      - cd to the directory contents of USECASE3 folder
      - Run the following command
        zip -r lambda-api.zip  "lambda-api.py"

## Changes to the CFT
- Update Parameters section
    - LambdaCodeS3Bucket to risingminervacodebase-<YOUR FIRST NAME><YOUR LAST NAME>
    - LambdaCodeS3Key to lambda-api/lambda-api.zip
- Update Mappings section
    - Update IAMRole section in CFT Mappings to ARN of your role arn:aws:iam::<youraccountid>:role/LambdaIAMRoleUseCase2
    - Update LambdaSubnets section in CFT Mappings to subnets of your VPC
    - Update LambdaSecurityGroups section in CFT Mappings to your security groups

## Upload CFT and application to S3
- After making all the changes indicated above, upload the CFT and application code to S3 bucket
  - s3://risingminervacodebase-<YOUR FIRST NAME><YOUR LAST NAME>/lambda-api/lambda-api.yml
  - s3://risingminervacodebase-<YOUR FIRST NAME><YOUR LAST NAME>/lambda-api/lambda-api.zip

## Spin up the stack
- Login to the AWS account.
- Go to CloudFormation
- Click on Create Stack
- Select “Template is Ready”
- Select “Amazon S3 URL”. Put the value of the PATH of S3 URL similar to (get it from your S3 bucket)
  - https://risingminervacodebase-rchaturvedi.s3.amazonaws.com/lambda-api/lambda-api.yml
  - https://risingminervacodebase-<YOUR FIRST NAME><YOUR LAST NAME>/lambda-api/lambda-api.yml
- Click Next
- Give Stack Name as risingminerva-lambda-api on the console
- Provide appropriate parameter names
  - Cross check parameters LambdaCodeS3Bucket
  - risingminervacodebase-<YOUR FIRST NAME><YOUR LAST NAME>
  
## IMPORTANT NOTE:
- To invoke DynamoDB from a VPC, you need to enable VPC endpoints to DYNAMODB service
- Go to VPC
- Click on your VPC
- Go to end points
- Add an endpoint to com.amazonaws.us-east-1.dynamodb to your VPC

## API Call
- You will be calling API Gateway URL of the stage/environment you chose silimar to below (We have provided this in OUTPUTs of this template)
  - GatewayURL: https://xuvrjm4wd1.execute-api.us-east-1.amazonaws.com/dev

### POST Customer id
  
    POST {{GatewayURL}}
    Headers::[{"key":"Content-Type","value":"application/json","description":""}]
    Body: 
    {	
    "operation": "insert", 
      "payload": 
     {
      "Item": 
        {
          "customer_id": 1, 
          "email": "rahul.0920@gmail.com", 
          "customer_name": "RC", 
          "customer_address": "2000 RFD 23112"
        }
     }
    }

### Get Customer id
  
    POST {{GatewayURL}}
    Headers::[{"key":"Content-Type","value":"application/json","description":""}]
    Body: 
    {
      "operation":"get",
      "payload" :{
        "customer_id":1
      }
    }

### DELETE Customer id
  
    POST {{GatewayURL}}
    Headers::[{"key":"Content-Type","value":"application/json","description":""}]
    Body: 
    {
      "operation":"delete",
      "payload" :{
        "customer_id":1
      }
    }
