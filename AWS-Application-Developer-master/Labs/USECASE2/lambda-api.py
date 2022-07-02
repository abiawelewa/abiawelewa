import json
import ast
import boto3
from botocore.exceptions import ClientError

def handler(event,context):
  if event['body']:
    postbody = json.loads(event["body"])
    print (postbody)
    operation = postbody["operation"].lower()
    payload = postbody["payload"]
    
    if operation and payload:
      try:
          dynamodb = boto3.resource('dynamodb')
          table = dynamodb.Table('customers')
      
          if operation == "get":
            customerid = postbody["payload"]["customer_id"]

            response = table.get_item(
                Key={
                    'customer_id':customerid
                }
            )
            print (response)
            item = response['Item']
            print(item)
            
            responseToClient = item
          elif operation == "insert":
            table.put_item(
               Item=payload["Item"]
            )
            
            responseToClient = "Inserted Item successfully"
          elif operation == "delete":
            customerid = postbody["payload"]["customer_id"]

            response = table.delete_item(
                Key={
                    'customer_id':customerid
                }
            )    
            
            responseToClient = "Deleted Item successfully"
          else:
            return {
              'body': 'Error: Operation is Invalid {0}'.format(operation),
              'headers': {
                'Content-Type': 'text/plain'
              },
              'statusCode': 501
            }
          
          return {
            'body': 'Welcome to Rising Minerva. {0}'.format(responseToClient),
            'headers': {
              'Content-Type': 'text/plain'
            },
            'statusCode': 200
          }
      except ClientError as e:
        responseToClient = "An exception occurred" + e.response['Error']['Message']
        return {
          'body': 'Welcome to Rising Minerva. {0}'.format(responseToClient),
          'headers': {
            'Content-Type': 'text/plain'
          },
          'statusCode': 200
        }
        
    else:
      return {
        'body': 'Error: Operation and Payload are mandatory',
        'headers': {
          'Content-Type': 'text/plain'
        },
        'statusCode': 501
      }      
  else:
    return {
      'body': 'Error: Body is needed {0}'.format(event['requestContext']['identity']['sourceIp']),
      'headers': {
        'Content-Type': 'text/plain'
      },
      'statusCode': 501
    }
