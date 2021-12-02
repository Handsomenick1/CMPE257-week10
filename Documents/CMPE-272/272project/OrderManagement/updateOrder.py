import json
import boto3
import decimal
from decimal import Decimal
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def update_order(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('arceus-orderdb')
    logger.debug('[EVENT] event: {}'.format(event))
    body = None
    try:
        if "body" not in event.keys():
            body = event
        elif "updateOrder" not in event['body']:
            raise Exception("updateOrder not in event")
        else:
            body = event['body']
    except Exception as e:
        logger.debug('[EVENT BODY] reading : {}'.format(event))
        return returnResponse(406, "Event input is not formatted correctly")
    
    logger.debug('[BODY] body: {}'.format(body))
    logger.debug('[BODY] body type: {}'.format(type(body)))
    if type(body) == str:
        body = json.loads(body)
    updateOrder = body['updateOrder']
    response = table.update_item(
        Key={
            'orderId': updateOrder['orderId']
        },
        UpdateExpression="set #date=:da, address=:adr, city=:ci, zipcode=:zip, state=:sta, assign=:assi",
        ExpressionAttributeNames={
            "#date": "date",
        },
        ExpressionAttributeValues={
            ":adr": updateOrder['address'],
            ":da":  updateOrder['date'],
            ":ci":  updateOrder['city'],
            ":zip": updateOrder['zipcode'],
            ":sta": updateOrder['state'],   
            ":assi": 0,         
        })
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