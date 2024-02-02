import json
import boto3
from datetime import datetime
from uuid import uuid4

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('Posts')
    
    try:
        PostId = int(datetime.now().timestamp())
        data = json.loads(event['body'])
        
        if 'content' not in data:
            raise ValueError("Missing 'content' in request body")
            
        item = {
            'PostId': PostId,
            'Content': data['content'],
            'CreatedAt': datetime.now().isoformat(),
            'Title': data.get('title', 'Default Title')
        }
        table.put_item(Item=item)
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # CORSの設定
                'Access-Control-Allow-Methods': 'POST, OPTIONS, GET',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Credentials': 'true'
            },
            'body': json.dumps({'message': '投稿成功', 'PostId': item['PostId']})
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # CORSの設定
                'Access-Control-Allow-Methods': 'POST, OPTIONS, GET',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Credentials': 'true'
            },
            'body': json.dumps({'error': '投稿に失敗しました', 'detail': str(e)})
        }

