# AWS application developer - Use case 3
Lambda file splitter. This module will split the input file based on predefined # of records and create multiple output files

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

## Review the lambda file splitter template
- Navigate to AWS-Application-Developer/Labs/USECASE3
- Open and review the template "lambda-file-splitter.yml" and application code “lambda-file-splitter.py”

## Bundle application
- Windows: 
  - Zip the “lambda-file-splitter.py” application code, resulting in “lambda-file-splitter.zip”
- MAC from Terminal command line
  - cd to the directory contents of USECASE3 folder
  - Run the following command
    - zip -r lambda-file-splitter.zip  "lambda-file-splitter.py"

## Changes to the CFT
- Update the parameters
  - SplitterLambdaCodeS3Bucket to risingminervacodebase-<YOUR FIRST NAME><YOUR LAST NAME>
  - Check if your key would be SplitterLambdaCodeS3Key to filesplitter/lambda-file-splitter.zip (As provided in default value)
- Update Mapping section
  - Update IAMRole section in CFT Mappings to ARN of your role arn:aws:iam::<youraccountid>:role/LambdaIAMRoleUseCase3
  - Update LambdaSubnets section in CFT Mappings to subnets of your VPC
  - Update LambdaSecurityGroups section in CFT Mappings to your security groups

## Upload File Splitter AWS Resources to S3
- Login to the AWS account.
- Go to S3 service
- Upload lambda-file-splitter.yml and lambda-file-splitter.zip to 
  - risingminervacodebase-<YOUR FIRST NAME><YOUR LAST NAME>/filesplitter

## Spin up the stack
- Login to the AWS account.
- Go to CloudFormation
- Click on Create Stack
- Select “Template is Ready”
- Select “Amazon S3 URL”. Put the value of the PATH of S3 URL similar to (get it from your S3 bucket)
  - https://risingminervacodebase-rchaturvedi.s3.amazonaws.com/filesplitter/lambda-file-splitter.yml
  - https://risingminervacodebase-<YOUR FIRST NAME><YOUR LAST NAME>/filesplitter/lambda-file-splitter.yml
- Click Next
- Give Stack Name as risingminerva-file-splitter on the console
- Provide appropriate parameter names
- Cross check parameters
  - Change parameters RisingMinervaS3InputBucket for the input bucket
    - risingminervainputdata-<YOUR FIRST NAME><YOUR LAST NAME>

## IMPORTANT NOTE:
- To invoke S3 from within a VPC, you need to enable VPC endpoints to S3 service
- Go to VPC
- Click on your VPC
- Go to end points
- Add an endpoint to com.amazonaws.us-east-1.s3 to your VPC
- Select the checkbox in front of the route table
- This ensures that your communication to Lambda via VPC can happen

## Data Upload
- Once the CFT is completed, risingminervainputdata-<YOUR FIRST NAME><YOUR LAST NAME>-<environment> name will be created
- Create two folders in the above bucket - 
  - input 
  - processed	
- Upload a file ending in .txt into the “input” folder of your bucket

## Test
The output should be split records of the uploaded file in processed folder
