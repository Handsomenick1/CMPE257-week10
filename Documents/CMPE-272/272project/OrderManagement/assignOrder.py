import json
import boto3
from decimal import Decimal
import decimal
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def assign_order(event, context):
    logger.debug('[EVENT] event: {}'.format(event))
    logger.debug('[EVENT] body: {}'.format(event['body']))
    try:
        if "body" not in event.keys():
            body = event
        elif "assignOrder" not in event['body']:
            raise Exception("assignOrder not in event")
        else:
            body = event['body']
    except Exception as e:
        logger.debug('[EVENT BODY] reading : {}'.format(event))
        return returnResponse(205, "Event input is not formatted correctly")
    if type(body) == str:
        body = json.loads(body)
   
    assignOrder = event['assignOrder']
    #update the order as assigned in DynameDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PhotoPrinter-orderDB')
    response = table.update_item(
        Key={
            'orderId': assignOrder['orderId'],
        },
        UpdateExpression="set assigned=:assi",
        ExpressionAttributeValues={   
            ":assi": assignOrder['employee'],         
        }
    )
   
    return returnResponse(200, json.dumps(response, indent=4, cls=DecimalEncoder))

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

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