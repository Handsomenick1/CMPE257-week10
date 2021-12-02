import logging
import base64
import uuid
import json
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')
def upload_file(event, context):
    region = 'us-west-2'
    if 'orderId' not in event['body'] or 'userId' not in event['body']:
        return returnResponse(203, "please make sure you have orderId and userId fileds")
    orderId = event['body']['orderId']
    userId = event['body']['userId']
    if orderId == None or len(orderId) == 0 or userId == None or len(userId) == 0:
        return returnResponse(203, "orderId and userId can not be empty")
    data_type = event['body']['file'].split('.')[-1]
    name = str(uuid.uuid1()) + data_type
    file_content = base64.b64decode(event['body']['file'])
    file_path = userId + '/' + orderId + '/' + name

    bucket_name = "photoprinter-s3"
    url = 'https://' + bucket_name + '.s3' + region + 'amazonaws.com/' + file_path
    try:
        s3_response = s3_client.put_object(Bucket=bucket_name, Key=file_path, Body=file_content)   
        logger.info('S3 Response: {}'.format(s3_response))

        return returnResponse(200, json.dumps(url))

    except Exception as e:
        raise IOError(e)
            

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