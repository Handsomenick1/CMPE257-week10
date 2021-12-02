import json
import boto3

s3 = boto3.resource('s3')
my_bucket = s3.Bucket('photoprinter-s3')

def getall_file(event, context):
    region = 'us-west-2'
    bucket_name = "photoprinter-s3"
    userId = event['queryStringParameters']['userId']
    orderId = event['queryStringParameters']['orderId']
    response = []
    for object_summary in my_bucket.objects.filter(Prefix=userId+'/'+orderId+'/'):
        url = 'https://' + bucket_name + '.s3' + region + 'amazonaws.com/' + userId+'/'+orderId+'/' + object_summary.key
        response.append(url)
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
