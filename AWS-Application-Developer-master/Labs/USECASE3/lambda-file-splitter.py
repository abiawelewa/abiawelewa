import boto3
import csv
 
def lambda_handler(event=None, context=None):
	if context:
		
		maxRecords = 3
		processedFolder = "processed/"
		
		s3 = boto3.client('s3')
		for record in event['Records']:
			print (event['Records'])
			s3bucket = record['s3']['bucket']['name']
			s3key = record['s3']['object']['key']
			
			response = s3.get_object(Bucket=s3bucket,Key=s3key)
			
			noOfFiles = 0
			lineCounter = 0
			
			chunkedBody = ""
			
			for line in response['Body'].read().splitlines():
				if len(chunkedBody) != 0:
					chunkedBody = "\n".join([chunkedBody, line.decode("utf-8")])
				else:
					chunkedBody = line.decode("utf-8")
					
				lineCounter = lineCounter + 1
				print("File counter: " + str(noOfFiles))
				if lineCounter%maxRecords == 0:
					print(chunkedBody + " Will be written in:" + processedFolder + str(noOfFiles) + "-" + s3key.split('/')[-1])
					s3.put_object(Body=chunkedBody, Bucket=s3bucket, Key=processedFolder + str(noOfFiles) + "-" + s3key.split('/')[-1])					
									
					lineCounter = 0
					noOfFiles = noOfFiles + 1
					chunkedBody = ""

			if len(chunkedBody) != 0:
				print(chunkedBody + " Will be written in:" + processedFolder + str(noOfFiles) + "-" + s3key.split('/')[-1])
				s3.put_object(Body=chunkedBody, Bucket=s3bucket, Key=processedFolder + str(noOfFiles) + "-" + s3key.split('/')[-1])					
			
			print ("Done")
