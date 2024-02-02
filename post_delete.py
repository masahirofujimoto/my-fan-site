import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event, indent=2))
    table = dynamodb.Table('Posts')

    try:
        # pathParameters から postId を取得し、整数に変換
        postId = int(event['pathParameters']['postId'])

        # DynamoDBから対応する項目を削除
        response = table.delete_item(Key={'PostId': postId})
        logger.info("Delete response: " + json.dumps(response, indent=2))

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': 'https://oshikatuapp.s3.amazonaws.com',
                'Access-Control-Allow-Methods': 'DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps('Post deleted successfully')
        }

    except ValueError as ve:
        logger.error("Value Error: " + str(ve))
        return {
            'statusCode': 400,
            'body': json.dumps({'error': "Invalid input: " + str(ve)})
        }
    except Exception as e:
        logger.error("Error: " + str(e))
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': str(e)})
        }

