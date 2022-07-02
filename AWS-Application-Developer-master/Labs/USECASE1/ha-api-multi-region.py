#!flask/bin/python
from flask import Flask, jsonify, request
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
from json import JSONEncoder
import decimal
from decimal import Decimal
import requests

username = "Rahul Chaturvedi"

response = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
currentInstanceId = response.text

response = requests.get('http://169.254.169.254/latest/meta-data/placement/availability-zone')
currentAZ = response.text
currentRegion = currentAZ[:-1]

dynamodb = boto3.resource('dynamodb', region_name=currentRegion)
table = dynamodb.Table('customers')

app = Flask(__name__)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)

@app.route('/', methods=['GET'])
def hello():
    return "Welcome to Rising Minerva - HA API with DynamoDB integration. Instance ID: " + currentInstanceId + " AZ: " + currentAZ + " USER: " + username
    
@app.route('/getCustomer', methods=['GET'])
def get_customer():        
    customerid = request.args.get('customerid')
    if customerid:
        print ("Customer id is present")
        customeridNumber = int(customerid)
        
        response = table.get_item(Key={"customer_id": customeridNumber})
        print (response)
        return json.dumps(response['Item'], cls=DecimalEncoder)
    else:
        return "Parameter customerid is mandatory for getting customer. Instance ID: " + currentInstanceId + " AZ: " + currentAZ + " USER: " + username
    
@app.route('/addCustomer', methods=['POST'])
def add_customer():
    payloadDict = json.loads(request.data.decode('utf-8'))
    print(payloadDict)
    
    if payloadDict:
        table.put_item(
                   Item=payloadDict
                )
        return "Customer added successfully. Instance ID: " + currentInstanceId + " AZ: " + currentAZ
    else:
        return "Payload including Item is mandatory for adding customer. Instance ID: " + currentInstanceId + " AZ: " + currentAZ + " USER: " + username
    
@app.route('/deleteCustomer', methods=['POST'])
def delete_customer():
    payloadDict = json.loads(request.data.decode('utf-8'))
    print(payloadDict)
    
    customerid = payloadDict['customerid']
    
    if payloadDict and customerid:
        print ("Customer id is present")
        table.delete_item(
                Key={
                    'customer_id':customerid
                }
            )  
        return "Customer deleted successfully. Instance ID: " + currentInstanceId + " AZ: " + currentAZ
    else:
        return "Payload customerid is mandatory for getting customer. Instance ID: " + currentInstanceId + " AZ: " + currentAZ + " USER: " + username
   
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
