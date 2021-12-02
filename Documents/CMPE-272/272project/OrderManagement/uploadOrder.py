import json
import boto3
import decimal
import uuid
from decimal import Decimal
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def upload_order(event, context):
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

    newOrder = body['newOrder']
    client = boto3.client('dynamodb')
    orderId = uuid.uuid1()
    response = client.put_item(
        TableName = 'PhotoPrinter-orderDB',
        Item={
            'orderId': str(orderId),
            'userId': newOrder['userId'],
            'storeId': newOrder['storeId'],
            'address': newOrder['address'],
            'orderdate': newOrder['orderdate'],
            'zipcode': newOrder['zipcode'],
            'city': newOrder['city'],
            'province': newOrder['province'],
            'imageurl': newOrder['imageurl'],
            'trackingurl': newOrder['trackingurl'],
            'phone': newOrder['phone'],
            'country': "The United States",
            'assigned':  "employee name",
            'statues': Decimal(str(0)),#0 initial, 1 in process, 2 finished
            'shipping': Decimal(str(0)),#0 Unkonw, 1 pre_transit, 2 transit 3 deliverd 4 returned 5 faliure
            'trackingNumber': "None",
            'orderTitle' : newOrder['orderTitle'],
            'orderDescription': newOrder['orderDescription']
        }
    )
    print(response)
    returnResponse(200, json.dumps(response['Item'], indent=4, cls=DecimalEncoder))
    
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
# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
