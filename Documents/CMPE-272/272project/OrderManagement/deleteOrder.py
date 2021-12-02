import json
import boto3
from botocore.exceptions import ClientError
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def delete_order(event, context):
    # TODO implement
    client = boto3.client('dynamodb')
    if 'orderId' not in event['queryStringParameters']:
        return returnResponse(203, "Bad request, please correct the Query Strings to orderId")
        
    orderId = event['queryStringParameters']['orderId']
    if(orderId == None or len(orderId) == 0):
        return returnResponse(203, "please enter valid orderId")
    try:
        response = client.delete_item(
            TableName = 'PhotoPrinter-orderDB',
            Key={
                'orderId':{'S': orderId},
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            return returnResponse(400, json.dumps(e.response['Error']['Message']))
        else:
            return returnResponse(400, "error")
            
    else:
        print(response)
        return returnResponse(200, json.dumps(response))
        
def returnResponse(statusCode, message):
    return {
        'statusCode': statusCode,
        'body': message,
        'headers': {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            'Access-Control-Allow-Credentials': True
        }
    }