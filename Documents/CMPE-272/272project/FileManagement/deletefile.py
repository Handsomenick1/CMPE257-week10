import logging
import json
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.resource('s3')
def delete_file(event, context):    
    if 'orderId' not in event['queryStringParameters'] or 'userId' not in event['queryStringParameters']:
        return returnResponse(203, "please make sure you have orderId and userId fileds")
    orderId = event['queryStringParameters']['orderId']
    userId = event['queryStringParameters']['userId']
    if orderId == None or len(orderId) == 0 or userId == None or len(userId) == 0:
        return returnResponse(203, "orderId and userId can not be empty")
    filename = event['queryStringParameters']['filename']
    file_path = userId+'/'+orderId+'/'+filename

    bucket_name = "photoprinter-s3"
    try:
        s3_response = s3.Object(bucket_name, file_path).delete()
        logger.info('S3 Response: {}'.format(s3_response))

        return returnResponse(200, "The file is deleted from s3!")

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