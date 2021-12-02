import boto3
import json
import decimal
from botocore.exceptions import ClientError
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def finish_order(event, context):
    logger.debug('[EVENT] event: {}'.format(event))
    logger.debug('[EVENT] body: {}'.format(event['body']))
    try:
        if "body" not in event.keys():
            body = event
        elif "newOrder" not in event['body']:
            raise Exception("newOrder not in event")
        else:
            body = event['body']
    except Exception as e:
        logger.debug('[EVENT BODY] reading : {}'.format(event))
        return returnResponse(205, "Event input is not formatted correctly")
    if type(body) == str:
        body = json.loads(body)

    updateOrder = body['updateOrder']
    
    #update the order as finished in DynameDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('arceus-orderdb')
    response = table.update_item(
        Key={
            'orderId': updateOrder['orderId'],
        },
        UpdateExpression="set shipping=:shp trackingNumber:=tra",
        ExpressionAttributeValues={   
            ":shp": 1,
            ":tra": updateOrder['trackingNumber']
            }
    )
    #send a request to notification
    
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