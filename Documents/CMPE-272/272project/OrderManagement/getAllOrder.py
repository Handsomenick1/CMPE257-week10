import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import decimal

def get_allOrder(event, context):
    dynamodb = boto3.resource('dynamodb')
    if 'userId' in event['queryStringParameters']:
        userId = event['queryStringParameters']['userId']
        if userId == None or len(userId) == 0:
            return returnResponse(400, "please enter userId!")
        userId = userIdEncoding(userId)
        print("userId is :" + userId)
        table = dynamodb.Table('PhotoPrinter-orderDB')
        response = table.scan(
            FilterExpression=Attr('userId').contains(userId)
        )
        if response['Items'] == None or len(response['Items']) == 0:
            return returnResponse(203, " The user does not have order")
        print(response)
    elif 'storeId' in event['queryStringParameters']:
        storeId = event['queryStringParameters']['storeId']
        if storeId == None or len(storeId) == 0:
            return returnResponse(400, "please enter storeId!")
        print("storeId is :" + storeId)
        table = dynamodb.Table('PhotoPrinter-orderDB')
        response = table.scan(
            FilterExpression=Attr('storeId').contains(storeId)
        )
        if response['Items'] == None or len(response['Items']) == 0:
            return returnResponse(203, " The store does not have order")
        print(response)
    return returnResponse(200, json.dumps(response['Items'], indent=4, cls=DecimalEncoder))
    
    

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

def userIdEncoding(userId):
    if "%2B" in userId:
        userId = userId.replace("%2B", "+")
    if " " in userId:
        userId = userId.replace(" ", "+")
    if "%21" in userId:
        userId = userId.replace("%21", "!")
    if "%24" in userId:
        userId = userId.replace("%24", "$")
    if "%25" in userId:
        userId = userId.replace("%25", "%")
    if "%26" in userId:
        userId = userId.replace("%26", "&")
    if "%2A" in userId:
        userId = userId.replace("%2A", "*")
    return userId