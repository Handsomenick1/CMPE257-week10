import boto3
import json
import decimal
from botocore.exceptions import ClientError

def finish_order(event, context):
    orderId = event['queryStringParameters']['order_id']
    
    #update the order as finished in DynameDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PhotoPrinter-orderDB')
    response = table.update_item(
        Key={
            'orderId': orderId,
        },
        UpdateExpression="set statues=:sta",
        ExpressionAttributeValues={   
            ":sta": 1,
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